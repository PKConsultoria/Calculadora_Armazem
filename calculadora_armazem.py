
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora Armazém", page_icon="📦", layout="centered")

st.title("📦 Calculadora de Receitas e Custos - Armazém")

# Entrada de dados
receita = st.number_input("Receita Bruta (R$)", min_value=0.0, step=100.0, format="%.2f")
custos_fixos = st.number_input("Custos Fixos (R$)", min_value=0.0, step=100.0, format="%.2f")
custos_variaveis = st.number_input("Custos Variáveis (R$)", min_value=0.0, step=100.0, format="%.2f")
volume = st.number_input("Volume Movimentado (unidades)", min_value=1, step=1)

# Cálculos
lucro_bruto = receita - custos_variaveis
lucro_liquido = lucro_bruto - custos_fixos
margem = (lucro_liquido / receita * 100) if receita > 0 else 0
custo_unitario = (custos_fixos + custos_variaveis) / volume

# Resultados
st.subheader("📊 Resultados")
st.metric("Lucro Bruto", f"R$ {lucro_bruto:,.2f}")
st.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
st.metric("Margem de Lucro", f"{margem:.2f}%")
st.metric("Custo por Unidade", f"R$ {custo_unitario:,.2f}")

# Gráfico
st.subheader("📈 Comparativo Receita x Custos")
fig, ax = plt.subplots()
ax.bar(["Receita", "Custos Fixos", "Custos Variáveis"], 
       [receita, custos_fixos, custos_variaveis], color=["green", "red", "orange"])
ax.set_ylabel("R$")
st.pyplot(fig)

# Exportar resultados
dados = {
    "Receita Bruta": [receita],
    "Custos Fixos": [custos_fixos],
    "Custos Variáveis": [custos_variaveis],
    "Lucro Bruto": [lucro_bruto],
    "Lucro Líquido": [lucro_liquido],
    "Margem (%)": [margem],
    "Custo por Unidade": [custo_unitario]
}
df = pd.DataFrame(dados)

st.download_button(
    label="📥 Baixar resultados em CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="resultados_armazem.csv",
    mime="text/csv"
)
