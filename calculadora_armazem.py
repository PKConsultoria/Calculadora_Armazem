import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuração inicial da página ---
st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="wide")

# --- CSS customizado ---
st.markdown("""
    <style>
        .big-metric {
            font-size:28px !important;
            font-weight:700 !important;
            color:#2E86C1;
        }
        .card {
            padding: 20px;
            border-radius: 12px;
            background-color: #f8f9fa;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.title("🏭 Calculadora de Receitas e Custos - Armazém")
st.markdown("Calcule de forma rápida e intuitiva os custos e receitas de uma operação logística.")

# ===============================
# Barra lateral - Configurações
# ===============================
with st.sidebar:
    st.header("⚙️ Configurações Gerais")
    st.subheader("ℹ️ Informações Básicas")
    armazem = st.selectbox("Armazém", ["Espinheiros", "Garuva"])
    cliente = st.text_input("Cliente", placeholder="Nome do Cliente")
    vendedor = st.text_input("Vendedor", placeholder="Nome do Vendedor")
    
    st.subheader("📊 Métricas Adotadas")
    dias_trabalhados = st.number_input("Dias Trabalhados", min_value=1, value=22, step=1)
    horas_trabalhadas_dia = st.number_input("Horas Trabalhadas por Dia", min_value=0.0, value=8.8, step=0.1, format="%.2f")
    eficiencia = st.number_input("Eficiência (%)", min_value=0, max_value=100, value=75, step=1)

# ===============================
# Detalhes da Operação
# ===============================
with st.container():
    st.header("🏗️ Detalhes da Operação")

    col1, col2 = st.columns(2)
    with col1:
        tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
        qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1)
    with col2:
        qtd_pallets = st.number_input("Quantidade de Pallets por Container", min_value=0, step=1)
        peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f")

    # Embalagem
    embalagem = st.selectbox("Distribuição da Carga", ["Palletizada", "Caixaria", "Sacaria", "Rolo", "Fardo", "Outros"])
    qtd_caixas_outros = 0
    if embalagem in ["Caixaria", "Sacaria", "Rolo", "Fardo", "Outros"]:
        label_map = {
            "Caixaria": "Quantidade de Caixas por Container",
            "Sacaria": "Quantidade de Sacos por Container",
            "Rolo": "Quantidade de Rolos por Container",
            "Fardo": "Quantidade de Fardos por Container",
            "Outros": "Quantidade de Outros Produtos por Container"
        }
        qtd_caixas_outros = st.number_input(label_map[embalagem], min_value=0, step=1)

    if qtd_containers > 0 and qtd_pallets == 0 and qtd_caixas_outros == 0:
        st.warning("⚠️ A soma de pallets e caixas/outros por container deve ser maior que 0 para o cálculo.")

# ===============================
# Serviços e custos
# ===============================
st.header("🛠️ Serviços")

# tempo médio de execução (horas por container/pallet/etc.)
tempos_execucao = {
    "Descarga": 1.5,
    "Etiquetagem": 0.5,
    "Paletização": 0.7,
    "Conferência": 0.3,
    "Armazenagem": 0.8,
    "Expedição": 0.6,
}

# custo por hora (exemplo fictício)
custo_hora = 25.0

servicos_selecionados = st.multiselect("Selecione os Serviços:", list(tempos_execucao.keys()))

custo_servicos = 0.0
custos_por_servico = {}
discriminacao = []

for nome in servicos_selecionados:
    tempo_unitario = tempos_execucao[nome]

    if "Descarga" in nome:
        demanda = qtd_containers * tempo_unitario
    elif "Etiquetagem" in nome:
        demanda = (qtd_containers * qtd_pallets + qtd_containers * qtd_caixas_outros) * tempo_unitario
    elif "Paletização" in nome:
        demanda = qtd_containers * qtd_caixas_outros * tempo_unitario
    else:
        demanda = qtd_containers * tempo_unitario

    headcount = (dias_trabalhados * horas_trabalhadas_dia) * (eficiencia / 100)
    taxa_ocupacao = demanda / headcount if headcount else 0
    custo = demanda * custo_hora

    custos_por_servico[nome] = custo
    custo_servicos += custo

    discriminacao.append({
        "Serviço": nome,
        "Demanda (h)": demanda,
        "HeadCount (h disponível)": headcount,
        "Taxa Ocupação": taxa_ocupacao,
        "Custo (R$)": custo
    })

# ===============================
# Resultados
# ===============================
if servicos_selecionados:
    st.markdown("---")
    st.header("📈 Resumo dos Resultados")

    # Cards
    total_containers = qtd_containers
    total_pallets = qtd_containers * qtd_pallets
    total_caixas_outros = qtd_containers * qtd_caixas_outros

    col_cards = st.columns(4)
    with col_cards[0]:
        st.markdown(f"<div class='card'><div class='big-metric'>R$ {custo_servicos:,.2f}</div><div>💰 Custo Total</div></div>", unsafe_allow_html=True)
    with col_cards[1]:
        st.markdown(f"<div class='card'><div class='big-metric'>{total_containers:,}</div><div>🧊 Containers</div></div>", unsafe_allow_html=True)
    with col_cards[2]:
        st.markdown(f"<div class='card'><div class='big-metric'>{total_pallets:,}</div><div>🧱 Pallets</div></div>", unsafe_allow_html=True)
    with col_cards[3]:
        if total_caixas_outros > 0:
            st.markdown(f"<div class='card'><div class='big-metric'>{total_caixas_outros:,}</div><div>🛍️ {embalagem}</div></div>", unsafe_allow_html=True)

    st.markdown("### 📊 Distribuição de Custos")
    df_custos = pd.DataFrame(list(custos_por_servico.items()), columns=['Serviço', 'Custo'])

    if not df_custos.empty:
        col_pie, col_bar = st.columns(2)

        with col_pie:
            st.write("**Gráfico de Pizza**")
            fig, ax = plt.subplots(figsize=(3, 3))
            df_custos_final = df_custos[df_custos['Custo'] > 0]
            ax.pie(df_custos_final['Custo'], labels=df_custos_final['Serviço'], autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax.axis('equal')
            st.pyplot(fig)

        with col_bar:
            st.write("**Gráfico de Barras**")
            fig, ax = plt.subplots(figsize=(4, 3))
            df_custos_final.sort_values("Custo", ascending=True).plot.barh(x="Serviço", y="Custo", ax=ax, legend=False)
            st.pyplot(fig)
    else:
        st.info("Nenhum serviço selecionado para calcular a distribuição de custos.")

    with st.expander("📋 Ver Discriminação Detalhada dos Custos"):
        if discriminacao:
            df_discriminacao = pd.DataFrame(discriminacao).fillna(0)
            df_discriminacao.index += 1
            st.dataframe(df_discriminacao.style.format({
                "Demanda (h)": "{:.2f}",
                "HeadCount (h disponível)": "{:.2f}",
                "Taxa Ocupação": "{:.2f}",
                "Custo (R$)": "R$ {:,.2f}"
            }))
        else:
            st.info("Nenhuma discriminação de custos disponível.")