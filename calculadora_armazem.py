import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# --- Adicionando a nova variável 'qtd_pallets' ---
if embalagem == "Palletizada":
    qtd_pallets = st.number_input("Quantidade de Pallets por Container", min_value=1, step=1)
else:
    qtd_pallets = 0 # Define como 0 para os outros tipos

# --- Atualizando a variável 'qtd_caixas' com base na embalagem ---
qtd_caixas = 0
if embalagem == "Caixaria":
    qtd_caixas = st.number_input("Quantidade de Caixas por Container", min_value=1, step=1)
if embalagem == "Sacaria":
    qtd_caixas = st.number_input("Quantidade de Sacos por Container", min_value=1, step=1)
if embalagem == "Rolo":
    qtd_caixas = st.number_input("Quantidade de Rolos por Container", min_value=1, step=1)
if embalagem == "Fardo":
    qtd_caixas = st.number_input("Quantidade de Fardos por Container", min_value=1, step=1)
if embalagem == "Outros":
    qtd_outros = st.number_input("Quantidade de Outros Produtos", min_value=1, step=1)
    qtd_caixas = qtd_outros # Usando qtd_caixas como uma variável genérica para a quantidade de itens

# ===============================
# Dimensões da Carga
# ===============================
st.header("📦 Dimensões da Carga")

col1, col2, col3, col4 = st.columns(4)
with col1:
    comprimento = st.number_input("Comprimento (m)", min_value=0.0, step=0.1, format="%.2f")
with col2:
    largura = st.number_input("Largura (m)", min_value=0.0, step=0.1, format="%.2f")
with col3:
    altura = st.number_input("Altura (m)", min_value=0.0, step=0.1, format="%.2f")
with col4:
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")

# ===============================
# Métricas Adotadas
# ===============================
st.header("📊 Métricas Adotadas")

col1, col2, col3 = st.columns(3)

with col1:
    dias_trabalhados = st.number_input(
        "Dias Trabalhados", 
        min_value=0, 
        value=22, 
        step=1
    )
with col2:
    horas_trabalhadas_dia = st.number_input(
        "Horas Trabalhadas por Dia", 
        min_value=0.0, 
        value=8.8, 
        step=0.1, 
        format="%.2f"
    )
with col3:
    eficiencia = st.number_input(
        "Eficiência (%)", 
        min_value=0, 
        max_value=100, 
        value=75, 
        step=1
    )


# ===============================
# Serviços
# ===============================
st.header("🛠️ Serviços")

# tempo médio de execução
tempos_execucao = {"Batida": 120, "Palletizada": 30}
tempo_exec = tempos_execucao[tipo_carga]

st.info(f"⏱️ Tempo estimado de execução por operação: **{tempo_exec} minutos**")

# Serviços por tipo de carga
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

# Valores de cada serviço
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

            # -----------------------------
            # Descarga
            # -----------------------------
            if "Descarga" in nome:
                # Lista de funções/subitens
                funcoes = [
                    {"nome": "Conferente", "salario": 4052.17, "tempo": 120},
                    {"nome": "Analista", "salario": 4780.41, "tempo": 10},
                    {"nome": "Supervisor", "salario": 6775.58, "tempo": 45},
                    {"nome": "Mão de Obra de Terceiros", "salario": 330, "tempo": 120},
                    {"nome": "Máquina Elétrica", "salario": 47.6, "tempo": 120},
                    {"nome": "Stretch", "salario": 6.85, "tempo": 0}
                ]

                # Variável para o cálculo de custo do stretch
                if embalagem == "Palletizada":
                    unidades_para_stretch = qtd_pallets
                else:
                    unidades_para_stretch = qtd_caixas

                for func in funcoes:
                    if func["nome"] == "Stretch":
                        # Stretch = R$ 6,85 * qtd_unidades * qtd_containers (independente do tempo)
                        custo = 6.85 * unidades_para_stretch * qtd_containers
                        tempo_horas = 0
                        demanda_horas = 0
                        taxa_ocupacao = 0
                        headcount_val = ""

                    elif func["nome"] == "Mão de Obra de Terceiros":
                        # Custo fixo por container, sem headcount/tempo
                        custo = 330 * qtd_containers
                        tempo_horas = 0
                        demanda_horas = 0
                        headcount_val = ""
                        taxa_ocupacao = 0

                    elif func["nome"] == "Máquina Elétrica":
                        # Mesmo padrão: salário x taxa de ocupação x demanda
                        tempo_horas = func["tempo"] / 60 
                        demanda_horas = tempo_horas * qtd_containers
                        headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                        taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val else 0
                        custo = func["salario"] * taxa_ocupacao * demanda_horas

                    else:  # Conferente, Analista, Supervisor
                        tempo_horas = func["tempo"] / 60
                        demanda_horas = tempo_horas * qtd_containers
                        headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                        taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val else 0
                        custo = func["salario"] * taxa_ocupacao

                    custo_servicos += custo
                    discriminacao.append({
                        "Serviço": nome,
                        "Função": func["nome"],
                        "Qtd Containers": qtd_containers,
                        "Qtd Pallets/Caixas": qtd_pallets if embalagem == "Palletizada" else qtd_caixas,
                        "Tempo/Container (h)": tempo_horas,
                        "Demanda (h)": demanda_horas,
                        "HeadCount (h disponível)": headcount_val,
                        "Taxa Ocupação": taxa_ocupacao,
                        "Custo (R$)": custo
                    })

            # -----------------------------
            # Etiquetagem e Custo de Etiqueta
            # -----------------------------
            elif "Etiquetagem" in nome:
                # Variável para o cálculo da etiquetagem
                if embalagem == "Palletizada":
                    unidades_para_etiquetagem = qtd_pallets
                else:
                    unidades_para_etiquetagem = qtd_caixas

                # Custo do Assistente de Etiquetagem
                salario_assistente = 3713.31
                tempo_pallet_h = 1 / 3600  # 1 segundo por pallet
                demanda_horas = tempo_pallet_h * qtd_containers * unidades_para_etiquetagem
                headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val else 0
                custo_assistente = salario_assistente * taxa_ocupacao * demanda_horas

                custo_servicos += custo_assistente
                discriminacao.append({
                    "Serviço": nome,
                    "Função": "Assistente",
                    "Qtd Containers": qtd_containers,
                    "Qtd Pallets/Caixas": unidades_para_etiquetagem,
                    "Tempo/Container (h)": tempo_pallet_h,
                    "Demanda (h)": demanda_horas,
                    "HeadCount (h disponível)": headcount_val,
                    "Taxa Ocupação": taxa_ocupacao,
                    "Custo (R$)": custo_assistente
                })

                # Custo da Etiqueta
                custo_etiqueta_unitario = 0.06
                custo_etiquetas = custo_etiqueta_unitario * unidades_para_etiquetagem * qtd_containers
                custo_servicos += custo_etiquetas
                
                discriminacao.append({
                    "Serviço": nome,
                    "Função": "Etiqueta",
                    "Qtd Containers": qtd_containers,
                    "Qtd Pallets/Caixas": unidades_para_etiquetagem,
                    "Tempo/Container (h)": "",
                    "Demanda (h)": "",
                    "HeadCount (h disponível)": "",
                    "Taxa Ocupação": "",
                    "Custo (R$)": custo_etiquetas
                })

            # -----------------------------
            # TFA
            # -----------------------------
            elif nome == "TFA":
                # Custo do Conferente para TFA
                salario_conferente_tfa = 4052.17
                tempo_conferente_tfa_min = 120
                tempo_conferente_tfa_h = tempo_conferente_tfa_min / 60
                demanda_horas_tfa = tempo_conferente_tfa_h * qtd_containers
                headcount_tfa_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                taxa_ocupacao_tfa = (demanda_horas_tfa / headcount_tfa_val) if headcount_tfa_val else 0
                custo_conferente_tfa = salario_conferente_tfa * taxa_ocupacao_tfa

                custo_servicos += custo_conferente_tfa
                discriminacao.append({
                    "Serviço": nome,
                    "Função": "Conferente",
                    "Qtd Containers": qtd_containers,
                    "Qtd Pallets/Caixas": "",
                    "Tempo/Container (h)": tempo_conferente_tfa_h,
                    "Demanda (h)": demanda_horas_tfa,
                    "HeadCount (h disponível)": headcount_tfa_val,
                    "Taxa Ocupação": taxa_ocupacao_tfa,
                    "Custo (R$)": custo_conferente_tfa
                })


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
                # Usar qtd_pallets ou qtd_caixas dependendo do tipo
                if embalagem == "Palletizada":
                    unidades_expedicao = qtd_pallets
                else:
                    unidades_expedicao = qtd_caixas
                custo_servicos += valores_servicos[nome] * unidades_expedicao * qtd_containers
            elif "Carregamento" in nome:
                custo_servicos += valores_servicos[nome] * qtd_containers

# -----------------------------
# Armazenagem (sempre aparece)
# -----------------------------
with st.expander("🏢 Armazenagem"):
    # Usar qtd_pallets ou qtd_caixas dependendo do tipo
    if embalagem == "Palletizada":
        unidades_armazenagem = qtd_pallets
    else:
        unidades_armazenagem = qtd_caixas

    for nome in servicos["Armazenagem"]:
        if st.checkbox(nome, key=f"arm_{nome}"):
            servicos_selecionados.append(nome)
            if nome == "Diária":
                dias = st.number_input("Dias de armazenagem", min_value=1, step=1, value=1)
                custo_servicos += valores_servicos[nome] * unidades_armazenagem * qtd_containers * dias
            else:
                custo_servicos += valores_servicos[nome]

# -----------------------------
# Custo total
# -----------------------------
st.metric("💰 Custo Total Serviços", f"R$ {custo_servicos:,.2f}")