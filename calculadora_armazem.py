import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="wide")

st.title("🏭 Calculadora de Receitas e Custos - Armazém")

# ===============================
# Informações básicas
# ===============================
st.header("ℹ️ Informações Básicas")

col1, col2, col3 = st.columns(3)
with col1:
    armazem = st.selectbox("Armazém", ["Espinheiros", "Garuva"])
with col2:
    cliente = st.text_input("Cliente")
with col3:
    vendedor = st.text_input("Vendedor")

# ===============================
# Detalhes da operação
# ===============================
st.header("🏗️ Detalhes da Operação")

col_op_1, col_op_2, col_op_3 = st.columns(3)
with col_op_1:
    tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
    qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1, value=1)
with col_op_2:
    peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f", value=25.0)
    valor_carga = st.number_input("Valor da Carga (R$)", min_value=0.0, step=100.0, format="%.2f", value=50000.0)
with col_op_3:
    embalagem = st.selectbox("Distribuição da Carga", ["Palletizada", "Caixaria", "Sacaria", "Rolo", "Fardo", "Outros"])
    if embalagem == "Palletizada":
        qtd_caixas = st.number_input("Quantidade de Pallets por Container", min_value=1, step=1, value=26)
    else:
        qtd_caixas = st.number_input(f"Quantidade de {embalagem} por Container", min_value=1, step=1, value=500)

# ===============================
# Métricas Adotadas
# ===============================
st.header("📊 Métricas Operacionais")

col_met_1, col_met_2, col_met_3 = st.columns(3)
with col_met_1:
    dias_trabalhados = st.number_input("Dias Trabalhados", min_value=0, value=22, step=1)
with col_met_2:
    horas_trabalhadas_dia = st.number_input("Horas Trabalhadas por Dia", min_value=0.0, value=8.8, step=0.1, format="%.2f")
with col_met_3:
    eficiencia = st.number_input("Eficiência (%)", min_value=0, max_value=100, value=75, step=1)

# ===============================
# Serviços e Cálculos
# ===============================
st.header("🛠️ Serviços e Cálculos")

# Dicionário de serviços
servicos_config = {
    "Descarga Batida": {
        "funcoes": [
            {"nome": "Conferente", "salario": 4052.17, "tempo_min_container": 120},
            {"nome": "Analista", "salario": 4780.41, "tempo_min_container": 10},
            {"nome": "Supervisor", "salario": 6775.58, "tempo_min_container": 45},
            {"nome": "Mão de Obra de Terceiros", "custo_por_container": 330},
            {"nome": "Máquina Elétrica", "salario": 47.6, "tempo_min_container": 120},
            {"nome": "Stretch", "custo_por_unidade": 6.85}
        ]
    },
    "Descarga Palletizada": {
        "funcoes": [
            {"nome": "Conferente", "salario": 4052.17, "tempo_min_container": 30},
            {"nome": "Analista", "salario": 4780.41, "tempo_min_container": 5},
            {"nome": "Supervisor", "salario": 6775.58, "tempo_min_container": 15},
            {"nome": "Mão de Obra de Terceiros", "custo_por_container": 100},
            {"nome": "Máquina Elétrica", "salario": 47.6, "tempo_min_container": 30},
            {"nome": "Stretch", "custo_por_unidade": 6.85}
        ]
    },
    "Etiquetagem Batida": {
        "funcoes": [
            {"nome": "Assistente", "salario": 3713.31, "tempo_min_caixa": 0.0167},  # 1s/caixa
            {"nome": "Etiqueta", "custo_por_unidade": 0.06}
        ]
    },
    "Etiquetagem Palletizada": {
        "funcoes": [
            {"nome": "Assistente", "salario": 3713.31, "tempo_min_caixa": 0.0167},
            {"nome": "Etiqueta", "custo_por_unidade": 0.06}
        ]
    },
    "TFA": {
        "funcoes": [
            {"nome": "Conferente", "salario": 4052.17, "tempo_min_container": 120}
        ]
    },
    "Diária": {"custo_por_unidade": 2.0},
    "Pico Quinzenal": {"custo_fixo": 500.0},
    "Pico Mensal": {"custo_fixo": 900.0}
}


servicos_recebimento = {
    "Batida": ["Descarga Batida", "Etiquetagem Batida", "TFA"],
    "Palletizada": ["Descarga Palletizada", "Etiquetagem Palletizada", "TFA"]
}

servicos_expedicao = {
    "Batida": ["Separação Batida", "Carregamento Batido", "Etiquetagem Batida"],
    "Palletizada": ["Separação Palletizada", "Carregamento Palletizado", "Etiquetagem Palletizada"]
}

servicos_armazenagem = ["Diária", "Pico Quinzenal", "Pico Mensal"]

# Armazenagem
st.subheader("Selecione os serviços contratados:")
custos_por_categoria = {}
discriminacao_custos = []

def calcular_custo_humano(salario, tempo_min, qtd):
    tempo_horas = tempo_min / 60
    demanda_horas = tempo_horas * qtd
    horas_disponiveis = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
    taxa_ocupacao = (demanda_horas / horas_disponiveis) if horas_disponiveis else 0
    custo = salario * taxa_ocupacao if salario < 1000 else salario * taxa_ocupacao * (demanda_horas / horas_disponiveis) # Apenas um exemplo de calculo diferente
    return custo, tempo_horas, demanda_horas, horas_disponiveis, taxa_ocupacao

def adicionar_disc_custo(servico, funcao, qtd_containers, qtd_caixas, tempo_h, demanda_h, headcount_h, taxa_ocup, custo):
    discriminacao_custos.append({
        "Serviço": servico,
        "Função": funcao,
        "Qtd Containers": qtd_containers,
        "Qtd Caixas": qtd_caixas,
        "Tempo/Container (h)": tempo_h,
        "Demanda (h)": demanda_h,
        "HeadCount (h disponível)": headcount_h,
        "Taxa Ocupação": f"{taxa_ocup:.2%}" if isinstance(taxa_ocup, (int, float)) else taxa_ocup,
        "Custo (R$)": custo
    })

# -----------------------------
# Recebimento
# -----------------------------
with st.expander("📥 Recebimento", expanded=True):
    total_recebimento = 0
    for nome in servicos_recebimento[tipo_carga]:
        if st.checkbox(nome, key=f"rec_{nome}"):
            custo_servico = 0
            config = servicos_config.get(nome, {})
            funcoes = config.get("funcoes", [])
            for func in funcoes:
                custo = 0
                tempo_h = ""
                demanda_h = ""
                headcount_h = ""
                taxa_ocup = ""

                if "salario" in func:  # Funções com base em salário
                    qtd = qtd_containers
                    if "tempo_min_caixa" in func:
                        qtd = qtd_containers * qtd_caixas
                    
                    custo, tempo_h, demanda_h, headcount_h, taxa_ocup = calcular_custo_humano(
                        func["salario"], 
                        func.get("tempo_min_container", func.get("tempo_min_caixa")), 
                        qtd
                    )
                elif "custo_por_container" in func:
                    custo = func["custo_por_container"] * qtd_containers
                elif "custo_por_unidade" in func:
                    custo = func["custo_por_unidade"] * qtd_containers * qtd_caixas
                
                custo_servico += custo
                adicionar_disc_custo(nome, func["nome"], qtd_containers, qtd_caixas, tempo_h, demanda_h, headcount_h, taxa_ocup, custo)

            st.metric(f"Custo de {nome}", f"R$ {custo_servico:,.2f}")
            total_recebimento += custo_servico
    custos_por_categoria["Recebimento"] = total_recebimento

# -----------------------------
# Expedição
# -----------------------------
with st.expander("📦 Expedição"):
    total_expedicao = 0
    st.info("⚠️ Funcionalidade em desenvolvimento...")
    custos_por_categoria["Expedição"] = total_expedicao

# -----------------------------
# Armazenagem
# -----------------------------
with st.expander("🏢 Armazenagem"):
    total_armazenagem = 0
    if st.checkbox("Diária", key="arm_diaria"):
        dias = st.number_input("Dias de armazenagem", min_value=1, step=1, value=30)
        custo = servicos_config["Diária"]["custo_por_unidade"] * qtd_caixas * qtd_containers * dias
        st.metric("Custo de Diária", f"R$ {custo:,.2f}")
        total_armazenagem += custo
        discriminacao_custos.append({
            "Serviço": "Diária",
            "Função": "Armazenagem",
            "Qtd Containers": qtd_containers,
            "Qtd Caixas": qtd_caixas,
            "Tempo/Container (h)": "",
            "Demanda (h)": "",
            "HeadCount (h disponível)": "",
            "Taxa Ocupação": "",
            "Custo (R$)": custo
        })

    if st.checkbox("Pico Quinzenal", key="arm_quinzenal"):
        custo = servicos_config["Pico Quinzenal"]["custo_fixo"]
        st.metric("Custo de Pico Quinzenal", f"R$ {custo:,.2f}")
        total_armazenagem += custo
        discriminacao_custos.append({"Serviço": "Pico Quinzenal", "Função": "Armazenagem", "Custo (R$)": custo})

    if st.checkbox("Pico Mensal", key="arm_mensal"):
        custo = servicos_config["Pico Mensal"]["custo_fixo"]
        st.metric("Custo de Pico Mensal", f"R$ {custo:,.2f}")
        total_armazenagem += custo
        discriminacao_custos.append({"Serviço": "Pico Mensal", "Função": "Armazenagem", "Custo (R$)": custo})
    
    custos_por_categoria["Armazenagem"] = total_armazenagem

# Totalização
custo_total = sum(custos_por_categoria.values())

# ===============================
# Resumo Financeiro
# ===============================
st.subheader("📈 Resumo Financeiro")
margem_lucro = st.slider("Margem de Lucro (%)", min_value=0, max_value=100, value=20, step=1)
receita_total = custo_total * (1 + margem_lucro / 100)
lucro = receita_total - custo_total

col_res_1, col_res_2, col_res_3 = st.columns(3)
col_res_1.metric("💰 Custo Total", f"R$ {custo_total:,.2f}")
col_res_2.metric("💵 Receita Total", f"R$ {receita_total:,.2f}")
col_res_3.metric("📈 Lucro Estimado", f"R$ {lucro:,.2f}")

# ===============================
# Análise Detalhada
# ===============================
with st.expander("📊 Análise Detalhada", expanded=True):
    st.subheader("📋 Discriminação de Custos")
    if discriminacao_custos:
        df_discriminacao = pd.DataFrame(discriminacao_custos)
        df_discriminacao.index += 1
        df_discriminacao.set_index("Serviço", inplace=True)
        st.dataframe(df_discriminacao.style.format({"Custo (R$)": "R$ {:,.2f}"}))
    else:
        st.info("Nenhum serviço selecionado para calcular os custos.")

    st.subheader("Gráfico de Participação de Custos")
    if custo_total > 0:
        labels = list(custos_por_categoria.keys())
        sizes = list(custos_por_categoria.values())
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)