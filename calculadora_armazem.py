import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora Armazém", page_icon="📦", layout="centered")

st.title("📦 Calculadora de Receitas e Custos - Armazém")


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

produto_opcoes = [
    "01 - Animais vivos.",
    "02 - Carnes e miudezas, comestíveis.",
    "03 - Peixes e crustáceos, moluscos e outros invertebrados aquáticos.",
    "04 - Leite e laticínios; ovos de aves; mel natural; produtos comestíveis de origem animal, não especificados nem compreendidos noutros Capítulos.",
    "05 - Outros produtos de origem animal, não especificados nem compreendidos noutros Capítulos.",
    "06 - Plantas vivas e produtos de floricultura.",
    "07 - Produtos hortícolas, plantas, raízes e tubérculos, comestíveis.",
    "08 - Fruta; cascas de citros (citrinos) e de melões.",
    "09 - Café, chá, mate e especiarias.",
    "10 - Cereais.",
    "11 - Produtos da indústria de moagem; malte; amidos e féculas; inulina; glúten de trigo.",
    "12 - Sementes e frutos oleaginosos; grãos, sementes e frutos diversos; plantas industriais ou medicinais; palhas e forragens.",
    "13 - Gomas, resinas e outros sucos e extratos vegetais.",
    "14 - Matérias para entrançar e outros produtos de origem vegetal, não especificados nem compreendidos noutros Capítulos.",
    "15 - Gorduras e óleos animais, vegetais ou de origem microbiana e produtos da sua dissociação; gorduras alimentícias elaboradas; ceras de origem animal ou vegetal.",
    "16 - Preparações de carne, peixes, crustáceos, moluscos, outros invertebrados aquáticos ou de insetos.",
    "17 - Açúcares e produtos de confeitaria.",
    "18 - Cacau e suas preparações.",
    "19 - Preparações à base de cereais, farinhas, amidos, féculas ou leite; produtos de pastelaria.",
    "20 - Preparações de produtos hortícolas, fruta ou de outras partes de plantas.",
    "21 - Preparações alimentícias diversas.",
    "22 - Bebidas, líquidos alcoólicos e vinagres.",
    "23 - Resíduos e desperdícios das indústrias alimentares; alimentos preparados para animais.",
    "24 - Tabaco e seus sucedâneos manufaturados; produtos, mesmo com nicotina, destinados à inalação sem combustão; outros produtos que contenham nicotina destinados à absorção da nicotina pelo corpo humano.",
    "25 - Sal; enxofre; terras e pedras; gesso, cal e cimento.",
    "26 - Minérios, escórias e cinzas.",
    "27 - Combustíveis minerais, óleos minerais e produtos da sua destilação; matérias betuminosas; ceras minerais.",
    "28 - Produtos químicos inorgânicos; compostos inorgânicos ou orgânicos de metais preciosos, de elementos radioativos, de metais das terras raras ou de isótopos.",
    "29 - Produtos químicos orgânicos.",
    "30 - Produtos farmacêuticos.",
    "31 - Adubos (fertilizantes).",
    "32 - Extratos tanantes e tintoriais; taninos e seus derivados; pigmentos e outras matérias corantes; tintas e vernizes; mástiques; tintas de escrever.",
    "33 - Óleos essenciais e resinoides; produtos de perfumaria ou de toucador preparados e preparações cosméticas.",
    "34 - Sabões, agentes orgânicos de superfície, preparações para lavagem, preparações lubrificantes, ceras artificiais, ceras preparadas, produtos de conservação e limpeza, velas e artigos semelhantes, massas ou pastas para modelar, \"ceras para odontologia\" e composições para odontologia à base de gesso.",
    "35 - Matérias albuminoides; produtos à base de amidos ou de féculas modificados; colas; enzimas.",
    "36 - Pólvoras e explosivos; artigos de pirotecnia; fósforos; ligas pirofóricas; matérias inflamáveis.",
    "37 - Produtos para fotografia e cinematografia.",
    "38 - Produtos diversos das indústrias químicas.",
    "39 - Plástico e suas obras.",
    "40 - Borracha e suas obras.",
    "41 - Peles, exceto as peles com pelo, e couros.",
    "42 - Obras de couro; artigos de correeiro ou de seleiro; artigos de viagem, bolsas e artigos semelhantes; obras de tripa.",
    "43 - Peles com pelo e suas obras; peles com pelo artificiais.",
    "44 - Madeira, carvão vegetal e obras de madeira.",
    "45 - Cortiça e suas obras.",
    "46 - Obras de espartaria ou de cestaria.",
    "47 - Pastas de madeira ou de outras matérias fibrosas celulósicas; papel ou cartão para reciclar (desperdícios e resíduos).",
    "48 - Papel e cartão; obras de pasta de celulose, papel ou de cartão.",
    "49 - Livros, jornais, gravuras e outros produtos das indústrias gráficas; textos manuscritos ou datilografados, planos e plantas.",
    "50 - Seda.",
    "51 - Lã, pelos finos ou grosseiros; fios e tecidos de crina.",
    "52 - Algodão.",
    "53 - Outras fibras têxteis vegetais; fios de papel e tecidos de fios de papel.",
    "54 - Filamentos sintéticos ou artificiais; lâminas e formas semelhantes de matérias têxteis sintéticas ou artificiais.",
    "55 - Fibras sintéticas ou artificiais, descontínuas.",
    "56 - Pastas (ouates), feltros e falsos tecidos (tecidos não tecidos); fios especiais; cordéis, cordas e cabos; artigos de cordoaria.",
    "57 - Tapetes e outros revestimentos para pisos (pavimentos), de matérias têxteis.",
    "58 - Tecidos especiais; tecidos tufados; rendas; tapeçarias; passamanarias; bordados.",
    "59 - Tecidos impregnados, revestidos, recobertos ou estratificados; artigos para usos técnicos de matérias têxteis.",
    "60 - Tecidos de malha.",
    "61 - Vestuário e seus acessórios, de malha.",
    "62 - Vestuário e seus acessórios, exceto de malha.",
    "63 - Outros artigos têxteis confeccionados; sortidos; artigos de matérias têxteis e artigos de uso semelhante, usados; trapos.",
    "64 - Calçado, polainas e artigos semelhantes; suas partes.",
    "65 - Chapéus e artigos de uso semelhante, e suas partes.",
    "66 - Guarda-chuvas, sombrinhas, guarda-sóis, bengalas, bengalas-assentos, chicotes, pingalins, e suas partes.",
    "67 - Penas e penugem preparadas e suas obras; flores artificiais; obras de cabelo.",
    "68 - Obras de pedra, gesso, cimento, amianto, mica ou de matérias semelhantes.",
    "69 - Produtos cerâmicos.",
    "70 - Vidro e suas obras.",
    "71 - Pérolas naturais ou cultivadas, pedras preciosas ou semipreciosas e semelhantes, metais preciosos, metais folheados ou chapeados de metais preciosos (plaquê), e suas obras; bijuterias; moedas.",
    "72 - Ferro fundido, ferro e aço.",
    "73 - Obras de ferro fundido, ferro ou aço.",
    "74 - Cobre e suas obras.",
    "75 - Níquel e suas obras.",
    "76 - Alumínio e suas obras.",
    "78 - Chumbo e suas obras.",
    "79 - Zinco e suas obras.",
    "80 - Estanho e suas obras.",
    "81 - Outros metais comuns; cermets; obras dessas matérias.",
    "82 - Ferramentas, artigos de cutelaria e talheres, e suas partes, de metais comuns.",
    "83 - Obras diversas de metais comuns.",
    "84 - Reatores nucleares, caldeiras, máquinas, aparelhos e instrumentos mecânicos, e suas partes.",
    "85 - Máquinas, aparelhos e materiais elétricos, e suas partes; aparelhos de gravação ou de reprodução de som, aparelhos de gravação ou de reprodução de imagens e de som em televisão, e suas partes e acessórios.",
    "86 - Veículos e material para vias férreas ou semelhantes, e suas partes; aparelhos mecânicos (incluindo os eletromecânicos) de sinalização para vias de comunicação.",
    "87 - Veículos automóveis, tratores, ciclos e outros veículos terrestres, suas partes e acessórios.",
    "88 - Aeronaves e aparelhos espaciais, e suas partes.",
    "89 - Embarcações e estruturas flutuantes.",
    "90 - Instrumentos e aparelhos de óptica, de fotografia, de cinematografia, de medida, de controle ou de precisão; instrumentos e aparelhos médico-cirúrgicos; suas partes e acessórios.",
    "91 - Artigos de relojoaria.",
    "92 - Instrumentos musicais; suas partes e acessórios.",
    "93 - Armas e munições; suas partes e acessórios.",
    "94 - Móveis; mobiliário médico-cirúrgico; colchões, almofadas e semelhantes; luminárias e aparelhos de iluminação não especificados nem compreendidos noutros Capítulos; anúncios, cartazes ou tabuletas e placas indicadoras, luminosos e artigos semelhantes; construções pré-fabricadas.",
    "95 - Brinquedos, jogos, artigos para divertimento ou para esporte; suas partes e acessórios.",
    "96 - Obras diversas.",
    "97 - Objetos de arte, de coleção e antiguidades."
]
produto = st.selectbox("Tipo de Produto", produto_opcoes)
valor_carga = st.number_input("Valor da Carga (R$)", min_value=0.0, step=100.0, format="%.2f")
embalagem = st.selectbox("Distribuição da Carga", ["Palletizada", "Caixaria", "Sacaria", "Rolo", "Fardo", "Outros"])
if embalagem == "Palletizada":
    qtd_caixas = st.number_input("Quantidade de Pallets por Container", min_value=1, step=1)
if embalagem == "Caixaria":
    qtd_caixas = st.number_input("Quantidade de Caixas por Container", min_value=1, step=1)
if embalagem == "Sacaria":
    qtd_caixas = st.number_input("Quantidade de Sacos por Container", min_value=1, step=1)
if embalagem == "Rolo":
    qtd_caixas = st.number_input("Quantidade de Rolos por Container", min_value=1, step=1)
if embalagem == "Fardo":
    qtd_caixas = st.number_input("Quantidade de Fardos por Container", min_value=1, step=1)
elif embalagem == "Outros":
    qtd_rolos = st.number_input("Quantidade de Outros Produtos", min_value=1, step=1)

# ===============================
# Dados financeiros
# ===============================
st.header("📑 Dados Financeiros")
receita = st.number_input("Receita Bruta (R$)", min_value=0.0, step=100.0, format="%.2f")
custos_fixos = st.number_input("Custos Fixos (R$)", min_value=0.0, step=100.0, format="%.2f")
custos_variaveis = st.number_input("Custos Variáveis (R$)", min_value=0.0, step=100.0, format="%.2f")
volume = st.number_input("Volume Movimentado (unidades)", min_value=1, step=1)

# ===============================
# Cálculos 🧮
# ===============================
lucro_bruto = receita - custos_variaveis
lucro_liquido = lucro_bruto - custos_fixos
margem = (lucro_liquido / receita * 100) if receita > 0 else 0
custo_unitario = (custos_fixos + custos_variaveis) / volume
peso_total_t = qtd_containers * peso_por_container
valor_medio_por_ton = (valor_carga / peso_total_t) if peso_total_t > 0 else 0.0

# ===============================
# Resultados
# ===============================
st.subheader("📊 Resultados")
col1, col2 = st.columns(2)
with col1:
    st.metric("Lucro Bruto", f"R$ {lucro_bruto:,.2f}")
    st.metric("Margem de Lucro", f"{margem:.2f}%")
    st.metric("Custo por Unidade", f"R$ {custo_unitario:,.2f}")
with col2:
    st.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
    st.metric("Peso Total (t)", f"{peso_total_t:,.2f}")
    st.metric("R$/ton (médio)", f"R$ {valor_medio_por_ton:,.2f}")

# Gráfico (Receita x Custos)
st.subheader("📈 Comparativo Receita x Custos")
fig, ax = plt.subplots()
ax.bar(["Receita", "Custos Fixos", "Custos Variáveis"], [receita, custos_fixos, custos_variaveis])
ax.set_ylabel("R$")
st.pyplot(fig)

# ===============================
# Exportar resultados
# ===============================
dados = {
    "Armazém": [armazem],
    "Cliente": [cliente],
    "Vendedor": [vendedor],
    "Tipo de Carga": [tipo_carga],
    "Qtd Containers": [qtd_containers],
    "Peso por Container (t)": [peso_por_container],
    "Peso Total (t)": [peso_total_t],
    "Tipo de Produto": [produto],
    "Valor da Carga (R$)": [valor_carga],
    "Embalagem": [embalagem],
    "Receita Bruta (R$)": [receita],
    "Custos Fixos (R$)": [custos_fixos],
    "Custos Variáveis (R$)": [custos_variaveis],
    "Lucro Bruto (R$)": [lucro_bruto],
    "Lucro Líquido (R$)": [lucro_liquido],
    "Margem (%)": [margem],
    "Custo por Unidade (R$)": [custo_unitario],
    "R$/ton (médio)": [valor_medio_por_ton],
}

df = pd.DataFrame(dados)

st.download_button(
    label="📥 Baixar resultados em CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="resultados_armazem.csv",
    mime="text/csv"
)
