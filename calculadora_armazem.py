import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# Configuração da Página
# ===============================
st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="centered")

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

tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1)

qtd_pallets = 0
qtd_caixas_outros = 0

if tipo_carga == "Palletizada":
    qtd_pallets = st.number_input("Quantidade de Pallets por Container", min_value=0, step=1)
else: # Batida
    embalagem = st.selectbox("Distribuição da Carga", ["Caixaria", "Sacaria", "Rolo", "Fardo", "Outros"])
    if embalagem == "Caixaria":
        qtd_caixas_outros = st.number_input("Quantidade de Caixas por Container", min_value=0, step=1)
    elif embalagem == "Sacaria":
        qtd_caixas_outros = st.number_input("Quantidade de Sacos por Container", min_value=0, step=1)
    elif embalagem == "Rolo":
        qtd_caixas_outros = st.number_input("Quantidade de Rolos por Container", min_value=0, step=1)
    elif embalagem == "Fardo":
        qtd_caixas_outros = st.number_input("Quantidade de Fardos por Container", min_value=0, step=1)
    elif embalagem == "Outros":
        qtd_caixas_outros = st.number_input("Quantidade de Outros Produtos por Container", min_value=0, step=1)

peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f")

produto_opcoes = [
    "01 - Animais vivos.", "02 - Carnes e miudezas, comestíveis.", "03 - Peixes e crustáceos, moluscos e outros invertebrados aquáticos.", "04 - Leite e laticínios; ovos de aves; mel natural; produtos comestíveis de origem animal, não especificados nem compreendidos noutros Capítulos.", "05 - Outros produtos de origem animal, não especificados nem compreendidos noutros Capítulos.", "06 - Plantas vivas e produtos de floricultura.", "07 - Produtos hortícolas, plantas, raízes e tubérculos, comestíveis.", "08 - Fruta; cascas de citros (citrinos) e de melões.", "09 - Café, chá, mate e especiarias.", "10 - Cereais.", "11 - Produtos da indústria de moagem; malte; amidos e féculas; inulina; glúten de trigo.", "12 - Sementes e frutos oleaginosos; grãos, sementes e frutos diversos; plantas industriais ou medicinais; palhas e forragens.", "13 - Gomas, resinas e outros sucos e extratos vegetais.", "14 - Matérias para entrançar e outros produtos de origem vegetal, não especificados nem compreendidos noutros Capítulos.", "15 - Gorduras e óleos animais, vegetais ou de origem microbiana e produtos da sua dissociação; gorduras alimentícias elaboradas; ceras de origem animal ou vegetal.", "16 - Preparações de carne, peixes, crustáceos, moluscos, outros invertebrados aquáticos ou de insetos.", "17 - Açúcares e produtos de confeitaria.", "18 - Cacau e suas preparações.", "19 - Preparações à base de cereais, farinhas, amidos, féculas ou leite; produtos de pastelaria.", "20 - Preparações de produtos hortícolas, fruta ou de outras partes de plantas.", "21 - Preparações alimentícias diversas.", "22 - Bebidas, líquidos alcoólicos e vinagres.", "23 - Resíduos e desperdícios das indústrias alimentares; alimentos preparados para animais.", "24 - Tabaco e seus sucedâneos manufaturados; produtos, mesmo com nicotina, destinados à inalação sem combustão; outros produtos que contenham nicotina destinados à absorção da nicotina pelo corpo humano.", "25 - Sal; enxofre; terras e pedras; gesso, cal e cimento.", "26 - Minérios, escórias e cinzas.", "27 - Combustíveis minerais, óleos minerais e produtos da sua destilação; matérias betuminosas; ceras minerais.", "28 - Produtos químicos inorgânicos; compostos inorgânicos ou orgânicos de metais preciosos, de elementos radioativos, de metais das terras raras ou de isótopos.", "29 - Produtos químicos orgânicos.", "30 - Produtos farmacêuticos.", "31 - Adubos (fertilizantes).", "32 - Extratos tanantes e tintoriais; taninos e seus derivados; pigmentos e outras matérias corantes; tintas e vernizes; mástiques; tintas de escrever.", "33 - Óleos essenciais e resinoides; produtos de perfumaria ou de toucador preparados e preparações cosméticas.", "34 - Sabões, agentes orgânicos de superfície, preparações para lavagem, preparações lubrificantes, ceras artificiais, ceras preparadas, produtos de conservação e limpeza, velas e artigos semelhantes, massas ou pastas para modelar, \"ceras para odontologia\" e composições para odontologia à base de gesso.", "35 - Matérias albuminoides; produtos à base de amidos ou de féculas modificados; colas; enzimas.", "36 - Pólvoras e explosivos; artigos de pirotecnia; fósforos; ligas pirofóricas; matérias inflamáveis.", "37 - Produtos para fotografia e cinematografia.", "38 - Produtos diversos das indústrias químicas.", "39 - Plástico e suas obras.", "40 - Borracha e suas obras.", "41 - Peles, exceto as peles com pelo, e couros.", "42 - Obras de couro; artigos de correeiro ou de seleiro; artigos de viagem, bolsas e artigos semelhantes; obras de tripa.", "43 - Peles com pelo e suas obras; peles com pelo artificiais.", "44 - Madeira, carvão vegetal e obras de madeira.", "45 - Cortiça e suas obras.", "46 - Obras de espartaria ou de cestaria.", "47 - Pastas de madeira ou de outras matérias celulósicas; papel ou cartão para reciclar (desperdícios e resíduos).", "48 - Papel e cartão; obras de pasta de celulose, papel ou de cartão.", "49 - Livros, jornais, gravuras e outros produtos das indústrias gráficas; textos manuscritos ou datilografados, planos e plantas.", "50 - Seda.", "51 - Lã, pelos finos ou grosseiros; fios e tecidos de crina.", "52 - Algodão.", "53 - Outras fibras têxteis vegetais; fios de papel e tecidos de fios de papel.", "54 - Filamentos sintéticos ou artificiais; lâminas e formas semelhantes de matérias têxteis sintéticas ou artificiais.", "55 - Fibras sintéticas ou artificiais, descontínuas.", "56 - Pastas (ouates), feltros e falsos tecidos (tecidos não tecidos); fios especiais; cordéis, cordas e cabos; artigos de cordoaria.", "57 - Tapetes e outros revestimentos para pisos (pavimentos), de matérias têxteis.", "58 - Tecidos especiais; tecidos tufados; rendas; tapeçarias; passamanarias; bordados.", "59 - Tecidos impregnados, revestidos, recobertos ou estratificados; artigos para usos técnicos de matérias têxteis.", "60 - Tecidos de malha.", "61 - Vestuário e seus acessórios, de malha.", "62 - Vestuário e seus acessórios, exceto de malha.", "63 - Outros artigos têxteis confeccionados; sortidos; artigos de matérias têxteis e artigos de uso semelhante, usados; trapos.", "64 - Calçado, polainas e artigos semelhantes; suas partes.", "65 - Chapéus e artigos de uso semelhante, e suas partes.", "66 - Guarda-chuvas, sombrinhas, guarda-sóis, bengalas, bengalas-assentos, chicotes, pingalins, e suas partes.", "67 - Penas e penugem preparadas e suas obras; flores artificiais; obras de cabelo.", "68 - Obras de pedra, gesso, cimento, amianto, mica ou de matérias semelhantes.", "69 - Produtos cerâmicos.", "70 - Vidro e suas obras.", "71 - Pérolas naturais ou cultivadas, pedras preciosas ou semipreciosas e semelhantes, metais preciosos, metais folheados ou chapeados de metais preciosos (plaquê), e suas obras; bijuterias; moedas.", "72 - Ferro fundido, ferro e aço.", "73 - Obras de ferro fundido, ferro ou aço.", "74 - Cobre e suas obras.", "75 - Níquel e suas obras.", "76 - Alumínio e suas obras.", "78 - Chumbo e suas obras.", "79 - Zinco e suas obras.", "80 - Estanho e suas obras.", "81 - Outros metais comuns; cermets; obras dessas matérias.", "82 - Ferramentas, artigos de cutelaria e talheres, e suas partes, de metais comuns.", "83 - Obras diversas de metais comuns.", "84 - Reatores nucleares, caldeiras, máquinas, aparelhos e instrumentos mecânicos, e suas partes.", "85 - Máquinas, aparelhos e materiais elétricos, e suas partes; aparelhos de gravação ou de reprodução de som, aparelhos de gravação ou de reprodução de imagens e de som em televisão, e suas partes e acessórios.", "86 - Veículos e material para vias férreas ou semelhantes, e suas partes; aparelhos mecânicos (incluindo os eletromecânicos) de sinalização para vias de comunicação.", "87 - Veículos automóveis, tratores, ciclos e outros veículos terrestres, suas partes e acessórios.", "88 - Aeronaves e aparelhos espaciais, e suas partes.", "89 - Embarcações e estruturas flutuantes.", "90 - Instrumentos e aparelhos de óptica, de fotografia, de cinematografia, de medida, de controle ou de precisão; instrumentos e aparelhos médico-cirúrgicos; suas partes e acessórios.", "91 - Artigos de relojoaria.", "92 - Instrumentos musicais; suas partes e acessórios.", "93 - Armas e munições; suas partes e acessórios.", "94 - Móveis; mobiliário médico-cirúrgico; colchões, almofadas e semelhantes; luminárias e aparelhos de iluminação não especificados nem compreendidos noutros Capítulos; anúncios, cartazes ou tabuletas e placas indicadoras, luminosos e artigos semelhantes; construções pré-fabricadas.", "95 - Brinquedos, jogos, artigos para divertimento ou para esporte; suas partes e acessórios.", "96 - Obras diversas.", "97 - Objetos de arte, de coleção e antiguidades."
]
produto = st.selectbox("Tipo de Produto", produto_opcoes)
valor_carga = st.number_input("Valor da Carga (R$)", min_value=0.0, step=100.0, format="%.2f")

if tipo_carga == "Batida" and qtd_caixas_outros == 0 and qtd_containers > 0:
    st.warning("A quantidade de caixas/outros por container deve ser maior que 0 para o cálculo.")
elif tipo_carga == "Palletizada" and qtd_pallets == 0 and qtd_containers > 0:
    st.warning("A quantidade de pallets por container deve ser maior que 0 para o cálculo.")

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

tempos_execucao = {"Batida": 120, "Palletizada": 30}
tempo_exec = tempos_execucao[tipo_carga]
st.info(f"⏱️ Tempo estimado de execução por operação: **{tempo_exec} minutos**")

servicos_selecionados = []
custo_servicos = 0.0
discriminacao = []

# Funções de custo
def calcular_custo(funcao, demanda_h, headcount_h):
    taxa_ocupacao = (demanda_h / headcount_h) if headcount_h > 0 else 0
    custo_total = funcao["salario"] * taxa_ocupacao
    return custo_total, taxa_ocupacao

def adicionar_discriminacao(servico, funcao, qtd_containers, qtd_pallets, qtd_caixas, tempo_h, demanda_h, headcount_h, taxa_ocupacao, custo):
    discriminacao.append({
        "Serviço": servico,
        "Função": funcao,
        "Qtd Containers": qtd_containers,
        "Qtd Pallets": qtd_pallets,
        "Qtd Caixas/Outros": qtd_caixas,
        "Tempo/Container (h)": tempo_h,
        "Demanda (h)": demanda_h,
        "HeadCount (h disponível)": headcount_h,
        "Taxa Ocupação": taxa_ocupacao,
        "Custo (R$)": custo
    })

headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)

# Dados de salários e tempos
SALARIOS = {
    "Conferente": 4052.17,
    "Analista": 4780.41,
    "Supervisor": 6775.58,
    "Coordenador": 7774.15,
    "Assistente": 3713.31,
    "Mão de Obra de Terceiros": 330,
    "Máquina Elétrica": 47.6,
    "Máquina GLP": 64.72,
    "Stretch": 6.85,
    "Etiqueta": 0.06
}

TEMPOS = {
    "Descarga": {"Conferente": 120, "Analista": 10, "Supervisor": 45},
    "TFA": {"Conferente": 120},
    "Separação": {"Conferente": 10},
    "Carregamento": {"Conferente": 120, "Analista": 10, "Coordenador": 45},
    "Etiquetagem": {"Assistente": 1}
}

# ===============================
# Recebimento
# ===============================
with st.expander("📥 Recebimento"):
    if st.checkbox("Descarga", key="rec_descarga"):
        servicos_selecionados.append("Descarga")
        
        # Mão de Obra e Máquinas
        funcoes = ["Conferente", "Analista", "Supervisor"]
        for nome_funcao in funcoes:
            tempo_min = TEMPOS["Descarga"][nome_funcao]
            tempo_h = tempo_min / 60
            demanda_h = tempo_h * qtd_containers
            
            custo, taxa_ocupacao = calcular_custo({"salario": SALARIOS[nome_funcao]}, demanda_h, headcount_val)
            custo_servicos += custo
            adicionar_discriminacao("Descarga", nome_funcao, qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_h, demanda_h, headcount_val, taxa_ocupacao, custo)
        
        # Custo de Terceiros e Máquinas (cálculo por container)
        if st.checkbox("Incluir Mão de Obra de Terceiros", key="rec_terceiros"):
            custo_terceiros = SALARIOS["Mão de Obra de Terceiros"] * qtd_containers
            custo_servicos += custo_terceiros
            adicionar_discriminacao("Descarga", "Mão de Obra de Terceiros", qtd_containers, qtd_pallets, qtd_caixas_outros, TEMPOS["Descarga"]["Conferente"] / 60, TEMPOS["Descarga"]["Conferente"] / 60 * qtd_containers, 0, 0, custo_terceiros)

        if st.checkbox("Incluir Máquina Elétrica", key="rec_maquina"):
            tempo_maquina_h = TEMPOS["Descarga"]["Conferente"] / 60
            demanda_maquina_h = tempo_maquina_h * qtd_containers
            custo_maquina = SALARIOS["Máquina Elétrica"] * demanda_maquina_h
            custo_servicos += custo_maquina
            adicionar_discriminacao("Descarga", "Máquina Elétrica", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_maquina_h, demanda_maquina_h, 0, 0, custo_maquina)
        
    if st.checkbox("Etiquetagem", key="rec_etiquetagem"):
        servicos_selecionados.append("Etiquetagem")
        unidades_para_etiquetagem = qtd_pallets + qtd_caixas_outros
        if unidades_para_etiquetagem > 0:
            tempo_assistente_h = TEMPOS["Etiquetagem"]["Assistente"] / 3600
            demanda_assistente_h = tempo_assistente_h * unidades_para_etiquetagem * qtd_containers
            custo_assistente, taxa_ocupacao = calcular_custo({"salario": SALARIOS["Assistente"]}, demanda_assistente_h, headcount_val)
            custo_servicos += custo_assistente
            adicionar_discriminacao("Etiquetagem", "Assistente", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_assistente_h * unidades_para_etiquetagem, demanda_assistente_h, headcount_val, taxa_ocupacao, custo_assistente)
            
            custo_etiquetas = SALARIOS["Etiqueta"] * unidades_para_etiquetagem * qtd_containers
            custo_servicos += custo_etiquetas
            adicionar_discriminacao("Etiquetagem", "Etiqueta", qtd_containers, qtd_pallets, qtd_caixas_outros, 0, 0, 0, 0, custo_etiquetas)
            
    if st.checkbox("TFA", key="rec_tfa"):
        servicos_selecionados.append("TFA")
        tempo_conferente_h = TEMPOS["TFA"]["Conferente"] / 60
        demanda_h = tempo_conferente_h * qtd_containers
        custo, taxa_ocupacao = calcular_custo({"salario": SALARIOS["Conferente"]}, demanda_h, headcount_val)
        custo_servicos += custo
        adicionar_discriminacao("TFA", "Conferente", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_conferente_h, demanda_h, headcount_val, taxa_ocupacao, custo)

# ===============================
# Expedição
# ===============================
with st.expander("📦 Expedição"):
    if st.checkbox("Separação", key="exp_separacao"):
        servicos_selecionados.append("Separação")
        unidades_demanda = qtd_caixas_outros
        tempo_conferente_h = TEMPOS["Separação"]["Conferente"] / 3600
        demanda_h = tempo_conferente_h * unidades_demanda * qtd_containers
        custo_conferente, taxa_ocupacao = calcular_custo({"salario": SALARIOS["Conferente"]}, demanda_h, headcount_val)
        custo_servicos += custo_conferente
        adicionar_discriminacao("Separação", "Conferente", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_conferente_h * unidades_demanda, demanda_h, headcount_val, taxa_ocupacao, custo_conferente)

        if st.checkbox("Incluir Máquina Elétrica na Separação", key="exp_maquina_sep"):
            custo_maquina = SALARIOS["Máquina Elétrica"] * demanda_h
            custo_servicos += custo_maquina
            adicionar_discriminacao("Separação", "Máquina Elétrica", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_conferente_h * unidades_demanda, demanda_h, 0, 0, custo_maquina)
            
    if st.checkbox("Carregamento", key="exp_carregamento"):
        servicos_selecionados.append("Carregamento")
        funcoes = ["Conferente", "Analista", "Coordenador"]
        for nome_funcao in funcoes:
            tempo_min = TEMPOS["Carregamento"][nome_funcao]
            tempo_h = tempo_min / 60
            demanda_h = tempo_h * qtd_containers
            custo, taxa_ocupacao = calcular_custo({"salario": SALARIOS[nome_funcao]}, demanda_h, headcount_val)
            custo_servicos += custo
            adicionar_discriminacao("Carregamento", nome_funcao, qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_h, demanda_h, headcount_val, taxa_ocupacao, custo)
        
        if st.checkbox("Incluir Mão de Obra de Terceiros", key="exp_terceiros"):
            custo_terceiros = SALARIOS["Mão de Obra de Terceiros"] * qtd_containers
            custo_servicos += custo_terceiros
            adicionar_discriminacao("Carregamento", "Mão de Obra de Terceiros", qtd_containers, qtd_pallets, qtd_caixas_outros, TEMPOS["Carregamento"]["Conferente"] / 60, TEMPOS["Carregamento"]["Conferente"] / 60 * qtd_containers, 0, 0, custo_terceiros)

        if st.checkbox("Incluir Máquina GLP", key="exp_maquina_glp"):
            tempo_maquina_h = TEMPOS["Carregamento"]["Conferente"] / 60
            demanda_maquina_h = tempo_maquina_h * qtd_containers
            custo_maquina = SALARIOS["Máquina GLP"] * demanda_maquina_h
            custo_servicos += custo_maquina
            adicionar_discriminacao("Carregamento", "Máquina GLP", qtd_containers, qtd_pallets, qtd_caixas_outros, tempo_maquina_h, demanda_maquina_h, 0, 0, custo_maquina)

# ===============================
# Armazenagem
# ===============================
with st.expander("🏢 Armazenagem"):
    tipo_armazenagem = st.selectbox("Tipo de Armazenagem", ["Diária", "Quinzenal", "Mensal"])
    
    custo_pallet = 1.32
    if tipo_armazenagem == "Diária":
        dias = st.number_input("Dias de armazenagem", min_value=1, step=1, value=1)
        if qtd_pallets > 0:
            custo_armazenagem = custo_pallet * qtd_pallets * qtd_containers * dias
            custo_servicos += custo_armazenagem
            adicionar_discriminacao("Armazenagem", "Diária (por pallet)", qtd_containers, qtd_pallets, qtd_caixas_outros, 0, 0, 0, 0, custo_armazenagem)
    elif tipo_armazenagem == "Quinzenal":
        if qtd_pallets > 0:
            custo_armazenagem = custo_pallet * 15 * qtd_pallets * qtd_containers
            custo_servicos += custo_armazenagem
            adicionar_discriminacao("Armazenagem", "Quinzenal (por pallet)", qtd_containers, qtd_pallets, qtd_caixas_outros, 0, 0, 0, 0, custo_armazenagem)
    elif tipo_armazenagem == "Mensal":
        if qtd_pallets > 0:
            custo_armazenagem = custo_pallet * 30 * qtd_pallets * qtd_containers
            custo_servicos += custo_armazenagem
            adicionar_discriminacao("Armazenagem", "Mensal (por pallet)", qtd_containers, qtd_pallets, qtd_caixas_outros, 0, 0, 0, 0, custo_armazenagem)

# ===============================
# Mostrar discriminação
# ===============================
if discriminacao:
    st.subheader("📋 Discriminação de Custos")
    df_discriminacao = pd.DataFrame(discriminacao)
    df_discriminacao.index += 1
    st.dataframe(df_discriminacao.fillna(0).style.format({
        "Custo (R$)": "R$ {:,.2f}",
        "Tempo/Container (h)": "{:.4f}",
        "Demanda (h)": "{:.4f}",
        "HeadCount (h disponível)": "{:.4f}",
        "Taxa Ocupação": "{:.4f}",
        "Qtd Containers": "{:.0f}",
        "Qtd Pallets": "{:.0f}",
        "Qtd Caixas/Outros": "{:.0f}"
    }))

# ===============================
# Custo total
# ===============================
st.metric("💰 Custo Total Serviços", f"R$ {custo_servicos:,.2f}")