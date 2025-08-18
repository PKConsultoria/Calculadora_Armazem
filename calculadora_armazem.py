
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="centered")

st.title("🏭Calculadora de Receitas e Custos - Armazém")

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

tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1)
peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f")
qtd_caixas = st.number_input("Quantidade de Itens por Container", min_value=1, step=1)

# ===============================
# Métricas Adotadas
# ===============================
st.header("📊 Métricas Adotadas")

dias_trabalhados = st.number_input("Dias Trabalhados", min_value=0, value=22, step=1)
horas_trabalhadas_dia = st.number_input("Horas Trabalhadas por Dia", min_value=0.0, value=8.8, step=0.1, format="%.2f")
eficiencia = st.number_input("Eficiência (%)", min_value=0, max_value=100, value=75, step=1)

# ===============================
# Serviços
# ===============================
st.header("🛠️ Serviços")

tempos_execucao = {"Batida": 120, "Palletizada": 30}
tempo_exec = tempos_execucao[tipo_carga]
st.info(f"⏱️ Tempo estimado de execução por operação: **{tempo_exec} minutos**")

servicos = {
    "Recebimento": {
        "Batida": ["Descarga Batida", "Etiquetagem Batida", "TFA"],
        "Palletizada": ["Descarga Palletizada", "Etiquetagem Palletizada", "TFA"]
    },
    "Expedição": {
        "Batida": ["Separação Batida", "Carregamento Batido", "Etiquetagem Batida"],
        "Palletizada": ["Separação Palletizada", "Carregamento Palletizado", "Etiquetagem Palletizada"]
    },
    "Armazenagem": ["Diária", "Pico Quinzenal", "Pico Mensal"]
}

valores_servicos = {
    "Descarga Batida": 100.0,
    "Descarga Palletizada": 80.0,
    "Etiquetagem Batida": 0.50,
    "Etiquetagem Palletizada": 0.30,
    "TFA": 200.0,
    "Separação Batida": 1.20,
    "Separação Palletizada": 5.0,
    "Carregamento Batido": 90.0,
    "Carregamento Palletizado": 70.0,
    "Diária": 2.0,
    "Pico Quinzenal": 500.0,
    "Pico Mensal": 900.0
}

st.subheader("Selecione os serviços contratados:")

servicos_selecionados = []
custo_servicos = 0.0
discriminacao = []

# -----------------------------
# Recebimento
# -----------------------------
with st.expander("📥 Recebimento"):
    for nome in servicos["Recebimento"][tipo_carga]:
        if st.checkbox(nome, key=f"rec_{nome}"):
            servicos_selecionados.append(nome)
            # Aqui você pode incluir lógica detalhada por serviço

# -----------------------------
# Mostrar discriminação
# -----------------------------
if discriminacao:
    st.subheader("📋 Discriminação de Custos - Recebimento")
    df_discriminacao = pd.DataFrame(discriminacao)
    df_discriminacao.index += 1
    st.dataframe(df_discriminacao.style.format({"Custo (R$)": "R$ {:,.2f}"}))

# -----------------------------
# Expedição
# -----------------------------
with st.expander("📦 Expedição"):
    for nome in servicos["Expedição"][tipo_carga]:
        if st.checkbox(nome, key=f"exp_{nome}"):
            servicos_selecionados.append(nome)
            if "Separação" in nome or "Etiquetagem" in nome:
                custo_servicos += valores_servicos[nome] * qtd_caixas * qtd_containers
            elif "Carregamento" in nome:
                custo_servicos += valores_servicos[nome] * qtd_containers

# -----------------------------
# Armazenagem (sempre aparece)
# -----------------------------
with st.expander("🏢 Armazenagem"):
    for nome in servicos["Armazenagem"]:
        if st.checkbox(nome, key=f"arm_{nome}"):
            servicos_selecionados.append(nome)
            if nome == "Diária":
                dias = st.number_input("Dias de armazenagem", min_value=1, step=1, value=1)
                custo_servicos += valores_servicos[nome] * qtd_caixas * qtd_containers * dias
            else:
                custo_servicos += valores_servicos[nome]

# -----------------------------
# Custo total
# -----------------------------
st.metric("💰 Custo Total Serviços", f"R$ {custo_servicos:,.2f}")
