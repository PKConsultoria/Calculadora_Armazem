import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Bibliotecas para Exportar PDF ---
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.flowables import PageBreak
import pytz
from datetime import datetime

# --- Configuração inicial da página ---
st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="wide")

# --- Título principal e subtítulo ---
st.title("🏭 Calculadora de Receitas e Custos - Armazém")
st.markdown("Open Beta V0.3 - Versão Corrigida")

# --- Barra Lateral para informações e métricas ---
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
    
    st.subheader("💰 Estratégia de Preço")
    custo_pbr = st.number_input("Custo PBR (R$)", min_value=0.0, value=1.32, step=0.01, format="%.2f")
    advalorem_percent = st.slider("Ad Valorem (%)", min_value=0.0, max_value=3.0, value=0.1, step=0.01, format="%.2f%%")
    markup_percent = st.slider("Markup (%)", min_value=0.0, max_value=100.0, value=30.0, step=0.5, format="%.1f%%")
    

# --- Container principal para o corpo da aplicação ---
with st.container(border=True):
    st.header("🏗️ Detalhes da Operação")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
        qtd_pallets = st.number_input("Quantidade de Pallets por Container", min_value=0, value=30, step=1)
   
    with col2:
        qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1)
        peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f")

    # --- Campo para embalagem e quantidade de caixas/outros ---
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

    # Validação para garantir que a soma de pallets e caixas não seja zero.
    if qtd_containers > 0 and qtd_pallets == 0 and qtd_caixas_outros == 0:
        st.warning("A soma da quantidade de pallets e caixas/outros por container deve ser maior que 0 para o cálculo.")

    # --- Detalhes adicionais da carga em um expansor ---
    with st.expander("➕ Outros Detalhes da Carga"):
        produto_opcoes = [
            "01 - Animais vivos.", "02 - Carnes e miudezas, comestíveis.", "03 - Peixes e crustáceos, moluscos e outros invertebrados aquáticos.",
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
            "47 - Pastas de madeira ou de outras matérias celulósicas; papel ou cartão para reciclar (desperdícios e resíduos).",
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
        # O st.number_input permanece o mesmo
        valor_carga = st.number_input("Valor da Carga (R$)", min_value=0.0, step=100.0, format="%.2f")

        st.subheader("📦 Dimensões da Carga")
        col_dim1, col_dim2, col_dim3, col_dim4 = st.columns(4)
        with col_dim1:
            comprimento = st.number_input("Comprimento (m)", min_value=0.0, step=0.1, format="%.2f")
        with col_dim2:
            largura = st.number_input("Largura (m)", min_value=0.0, step=0.1, format="%.2f")
        with col_dim3:
            altura = st.number_input("Altura (m)", min_value=0.0, step=0.1, format="%.2f")
        with col_dim4:
            peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.2f")


# --- Container de Serviços ---
with st.container(border=True):
    st.header("🛠️ Serviços")
    
    # tempo médio de execução
    tempos_execucao = {"Batida": 120, "Palletizada": 30}
    tempo_exec = tempos_execucao.get(tipo_carga, 0)
    st.info(f"⏱️ Tempo estimado de execução por operação: **{tempo_exec} minutos**")
    
    # Valores de tempo para Descarga/Carregamento
    tempo_descarga_min = tempos_execucao.get(tipo_carga)
    tempo_carregamento_min = tempos_execucao.get(tipo_carga)
    
    # Serviços por tipo de carga
    servicos = {
        "Recebimento": {
            # REMOÇÃO DO STRETCH PARA PALLETIZADA
            "Batida": ["Descarga Batida", "Etiquetagem Batida", "TFA", "Stretch"],
            "Palletizada": ["Descarga Palletizada", "Etiquetagem Palletizada", "TFA"]
        },
        "Expedição": {
            "Batida": ["Separação Batida", "Carregamento Batido", "Etiquetagem Batida"],
            "Palletizada": ["Separação Palletizada", "Carregamento Palletizado", "Etiquetagem Palletizada"]
        },
        "Armazenagem": ["Diária", "Pico Quinzenal", "Pico Mensal"]
    }
    
    # Valores de cada serviço (não alterados)
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
        "Diária": 0.0,
        "Pico Quinzenal": 0.0,
        "Pico Mensal": 0.0
    }
    
    servicos_selecionados = []
    custos_por_servico = {}
    discriminacao = []
    custo_servicos = 0.0
    receita_total = 0.0 # Inicializa a variável de receita total

    # --- Expansores para cada tipo de serviço ---
    with st.expander("📥 Recebimento"):
        for nome in servicos["Recebimento"][tipo_carga]:
            if st.checkbox(nome, key=f"rec_{nome}"):
                servicos_selecionados.append(nome)
                
                # -----------------------------
                # Descarga
                # -----------------------------
                if "Descarga" in nome:
                    
                    # Funções base com tempo para carga Batida (120 min) ou tempos menores
                    funcoes_base = [
                        {"nome": "Conferente", "salario": 4052.17, "tempo": 120}, 
                        {"nome": "Analista", "salario": 4780.41, "tempo": 10},
                        {"nome": "Supervisor", "salario": 6775.58, "tempo": 45},
                        {"nome": "Mão de Obra de Terceiros", "salario": 330, "tempo": 120},
                        {"nome": "Máquina Elétrica", "salario": 47.6, "tempo": 120},
                    ]
                    
                    funcoes = []
                    
                    # CORREÇÃO: Lógica para filtrar Mão de Obra de Terceiros e ajustar tempo para 30 minutos
                    for func in funcoes_base:
                        if tipo_carga == "Palletizada":
                            # 1. REMOVE APENAS 'Mão de Obra de Terceiros'
                            if func["nome"] == "Mão de Obra de Terceiros":
                                continue
                            
                            # 2. AJUSTA TEMPO para 30 min (se o tempo base for 120)
                            novo_tempo = func["tempo"] if func["tempo"] != 120 else 30
                            funcoes.append({**func, "tempo": novo_tempo})
                            
                        else: # Batida (120 min)
                            # 1. MANTÉM TODOS
                            # 2. TEMPO permanece 120 min (ou o tempo original)
                            funcoes.append(func)
                    
                    unidades_totais = qtd_pallets + qtd_caixas_outros
                    
                    for func in funcoes:
                        tempo_horas_total = 0
                        custo = 0
                        
                        headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                        
                        if func["nome"] == "Mão de Obra de Terceiros":
                            # O custo de Mão de Obra de Terceiros é um custo fixo por container
                            custo = func["salario"] * qtd_containers
                        elif func["nome"] == "Máquina Elétrica":
                            # Custo da Máquina por hora efetiva
                            tempo_horas = func["tempo"] / 60
                            demanda_horas = tempo_horas * qtd_containers
                            headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                            # CORREÇÃO: Custo da máquina é rateado pela taxa de ocupação do recurso no mês
                            taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                            custo = func["salario"] * taxa_ocupacao * demanda_horas # Correção na fórmula de custo da máquina
                        else: # Mão de obra (Conferente, Analista, Supervisor)
                            tempo_por_container_h = func["tempo"] / 60
                            tempo_horas_total = tempo_por_container_h * qtd_containers
                            taxa_ocupacao = (tempo_horas_total / headcount_val) if headcount_val > 0 else 0
                            # Custo da Mão de Obra é o salário rateado pela taxa de ocupação do recurso no mês
                            custo = func["salario"] * taxa_ocupacao

                        custo_servicos += custo
                        if nome not in custos_por_servico:
                             custos_por_servico[nome] = 0
                        custos_por_servico[nome] += custo
                        discriminacao.append({
                            "Serviço": nome, "Função": func["nome"], "Custo (R$)": custo,
                            "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                            "Tempo/Container (h)": func["tempo"] / 60 if func["tempo"] > 0 else 0,
                            "Demanda (h)": tempo_horas_total if tempo_horas_total > 0 or func["nome"] not in ["Mão de Obra de Terceiros", "Máquina Elétrica"] else (func["tempo"] / 60) * qtd_containers if func["nome"] == "Máquina Elétrica" else 0,
                            "HeadCount (h disponível)": headcount_val if headcount_val > 0 and func["nome"] not in ["Mão de Obra de Terceiros"] else 0,
                            "Taxa Ocupação": taxa_ocupacao if 'taxa_ocupacao' in locals() and func["nome"] not in ["Mão de Obra de Terceiros"] else 0
                        })
                
                # -----------------------------
                # Etiquetagem e Custo de Etiqueta (CORREÇÃO DE CATEGORIA)
                # -----------------------------
                elif "Etiquetagem" in nome:
                    unidades_para_etiquetagem = qtd_pallets + qtd_caixas_outros

                    # NOVO: Diferenciação do nome do serviço para Recebimento
                    nome_rec = f"{nome} (Recebimento)"
                    
                    # Custo do Assistente de Etiquetagem
                    tempo_pallet_h = 1 / 3600
                    salario_assistente = 3713.31
                    tempo_por_unidade_h = 1 / 3600
                    demanda_horas = tempo_pallet_h * qtd_containers * qtd_pallets
                    headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                    taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                    custo_assistente = salario_assistente * taxa_ocupacao * demanda_horas

                    custo_servicos += custo_assistente
                    if nome_rec not in custos_por_servico:
                         custos_por_servico[nome_rec] = 0
                    custos_por_servico[nome_rec] += custo_assistente
                    discriminacao.append({
                        "Serviço": nome_rec, # USANDO NOME DIFERENCIADO
                        "Função": "Assistente", "Custo (R$)": custo_assistente,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": tempo_por_unidade_h * unidades_para_etiquetagem, "Demanda (h)": demanda_horas,
                        "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao
                    })

                    # Custo da Etiqueta
                    custo_etiqueta_unitario = 0.06
                    custo_etiquetas = custo_etiqueta_unitario * qtd_containers * qtd_pallets
                    custo_servicos += custo_etiquetas
                    if nome_rec not in custos_por_servico:
                         custos_por_servico[nome_rec] = 0
                    custos_por_servico[nome_rec] += custo_etiquetas
                    discriminacao.append({
                        "Serviço": nome_rec, # USANDO NOME DIFERENCIADO
                        "Função": "Etiqueta", "Custo (R$)": custo_etiquetas,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": 0, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0
                    })

                # -----------------------------
                # TFA (sem alteração)
                # -----------------------------
                elif nome == "TFA":
                    salario_conferente_tfa = 4052.17
                    tempo_conferente_tfa_min = 120
                    tempo_conferente_tfa_h = tempo_conferente_tfa_min / 60
                    demanda_horas_tfa = tempo_conferente_tfa_h * qtd_containers
                    headcount_tfa_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                    taxa_ocupacao_tfa = (demanda_horas_tfa / headcount_tfa_val) if headcount_tfa_val > 0 else 0
                    custo_conferente_tfa = salario_conferente_tfa * taxa_ocupacao_tfa

                    custo_servicos += custo_conferente_tfa
                    if nome not in custos_por_servico:
                         custos_por_servico[nome] = 0
                    custos_por_servico[nome] += custo_conferente_tfa
                    discriminacao.append({
                        "Serviço": nome, "Função": "Conferente", "Custo (R$)": custo_conferente_tfa,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": tempo_conferente_tfa_h, "Demanda (h)": demanda_horas_tfa,
                        "HeadCount (h disponível)": headcount_tfa_val, "Taxa Ocupação": taxa_ocupacao_tfa
                    })
                
                # -----------------------------
                # Stretch (agora só aparece para Batida)
                # -----------------------------
                elif nome == "Stretch":
                    custo_unitario_stretch = 6.85
                    custo_total_stretch = custo_unitario_stretch * qtd_pallets * qtd_containers

                    custo_servicos += custo_total_stretch
                    if nome not in custos_por_servico:
                        custos_por_servico[nome] = 0
                    custos_por_servico[nome] += custo_total_stretch
                    discriminacao.append({
                        "Serviço": nome, "Função": "Material", "Custo (R$)": custo_total_stretch,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": 0, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0
                    })


    with st.expander("📦 Expedição"):
        for nome in servicos["Expedição"][tipo_carga]:
            if st.checkbox(nome, key=f"exp_{nome}"):
                servicos_selecionados.append(nome)
                
                # --- Separação (sem alteração) ---
                if "Separação" in nome:
                    funcoes_separacao = [
                        {"nome": "Conferente", "salario": 4052.17, "tempo": 10}, # 10s
                        {"nome": "Máquina Elétrica", "salario": 47.6, "tempo": 10} # 10s
                    ]
                    unidades_demanda = qtd_containers * qtd_caixas_outros
                    
                    for func in funcoes_separacao:
                        custo = 0.0
                        taxa_ocupacao = 0.0
                        demanda_horas = 0.0
                        
                        headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)

                        demanda_horas = (func["tempo"] / 3600) * unidades_demanda
                        taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                        
                        if func["nome"] == "Máquina Elétrica":
                            # CORREÇÃO: Custo da máquina é rateado pela taxa de ocupação do recurso no mês
                            custo = func["salario"] * taxa_ocupacao * demanda_horas # Correção na fórmula de custo da máquina
                        else: # Mão de obra
                            custo = func["salario"] * taxa_ocupacao
                        
                        custo_servicos += custo
                        if nome not in custos_por_servico:
                            custos_por_servico[nome] = 0
                        custos_por_servico[nome] += custo
                        discriminacao.append({
                            "Serviço": nome, "Função": func["nome"], "Custo (R$)": custo,
                            "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                            "Tempo/Container (h)": func["tempo"] / 3600, "Demanda (h)": demanda_horas,
                            "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao
                        })
                
                # --- Carregamento ---
                elif "Carregamento" in nome:
                    
                    # Funções base com tempo para carga Batida (120 min) ou tempos menores
                    funcoes_carregamento_base = [
                        {"nome": "Conferente", "salario": 4052.17, "tempo": 120}, 
                        {"nome": "Analista", "salario": 4780.41, "tempo": 10},
                        {"nome": "Coordenador", "salario": 7774.15, "tempo": 45},
                        {"nome": "Mão de Obra de Terceiros", "salario": 330, "tempo": 120},
                        {"nome": "Máquina GLP", "salario": 64.72, "tempo": 120},
                    ]
                    
                    funcoes_carregamento = []
                    
                    # CORREÇÃO: Lógica para filtrar Mão de Obra de Terceiros e ajustar tempo para 30 minutos
                    for func in funcoes_carregamento_base:
                        if tipo_carga == "Palletizada":
                            # 1. REMOVE APENAS 'Mão de Obra de Terceiros'
                            if func["nome"] == "Mão de Obra de Terceiros":
                                continue
                            
                            # 2. AJUSTA TEMPO para 30 min (se o tempo base for 120)
                            novo_tempo = func["tempo"] if func["tempo"] != 120 else 30
                            funcoes_carregamento.append({**func, "tempo": novo_tempo})
                            
                        else: # Batida (120 min)
                            # 1. MANTÉM TODOS
                            # 2. TEMPO permanece 120 min (ou o tempo original)
                            funcoes_carregamento.append(func)
                    
                    headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                    
                    for func in funcoes_carregamento:
                        custo = 0.0
                        tempo_horas_total = 0
                        taxa_ocupacao = 0
                        
                        if func["nome"] == "Mão de Obra de Terceiros":
                            custo = func["salario"] * qtd_containers
                        elif func["nome"] == "Máquina GLP":
                            tempo_horas = func["tempo"] / 60
                            demanda_horas = tempo_horas * qtd_containers
                            taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                            # CORREÇÃO: Custo da máquina é rateado pela taxa de ocupação do recurso no mês
                            custo = func["salario"] * taxa_ocupacao * demanda_horas # Correção na fórmula de custo da máquina
                        else: # Mão de obra
                            tempo_por_container_h = func["tempo"] / 60
                            tempo_horas_total = tempo_por_container_h * qtd_containers
                            taxa_ocupacao = (tempo_horas_total / headcount_val) if headcount_val > 0 else 0
                            custo = func["salario"] * taxa_ocupacao
                        
                        custo_servicos += custo
                        if nome not in custos_por_servico:
                             custos_por_servico[nome] = 0
                        custos_por_servico[nome] += custo
                        discriminacao.append({
                            "Serviço": nome, "Função": func["nome"], "Custo (R$)": custo,
                            "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                            "Tempo/Container (h)": func["tempo"] / 60 if func["tempo"] > 0 else 0,
                            "Demanda (h)": tempo_horas_total if tempo_horas_total > 0 or func["nome"] not in ["Mão de Obra de Terceiros", "Máquina GLP"] else (func["tempo"] / 60) * qtd_containers if func["nome"] == "Máquina GLP" else 0,
                            "HeadCount (h disponível)": headcount_val if headcount_val > 0 and func["nome"] not in ["Mão de Obra de Terceiros"] else 0,
                            "Taxa Ocupação": taxa_ocupacao if 'taxa_ocupacao' in locals() and func["nome"] not in ["Mão de Obra de Terceiros"] else 0
                        })
                
                # --- Etiquetagem de Expedição (CORREÇÃO DE CATEGORIA) ---
                elif "Etiquetagem" in nome:
                    
                    # NOVO: Diferenciação do nome do serviço para Expedição
                    nome_exp = f"{nome} (Expedição)"
                    
                    salario_assistente = 3713.31
                    unidades_para_etiquetagem_exp = qtd_caixas_outros if tipo_carga == "Batida" else qtd_pallets
                    tempo_por_unidade_h = 1 / 3600
                    demanda_horas = tempo_por_unidade_h * unidades_para_etiquetagem_exp * qtd_containers
                    headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
                    taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                    custo_assistente = salario_assistente * taxa_ocupacao * demanda_horas
                    
                    custo_servicos += custo_assistente
                    if nome_exp not in custos_por_servico:
                         custos_por_servico[nome_exp] = 0
                    custos_por_servico[nome_exp] += custo_assistente
                    discriminacao.append({
                        "Serviço": nome_exp, # USANDO NOME DIFERENCIADO
                        "Função": "Assistente", "Custo (R$)": custo_assistente,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": tempo_por_unidade_h * unidades_para_etiquetagem_exp, "Demanda (h)": demanda_horas,
                        "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao
                    })

                    # Custo da Etiqueta
                    custo_etiqueta_unitario = 0.06
                    custo_etiquetas = custo_etiqueta_unitario * qtd_containers * qtd_caixas_outros
                    custo_servicos += custo_etiquetas
                    if nome_exp not in custos_por_servico:
                         custos_por_servico[nome_exp] = 0
                    custos_por_servico[nome_exp] += custo_etiquetas
                    discriminacao.append({
                        "Serviço": nome_exp, # USANDO NOME DIFERENCIADO
                        "Função": "Etiqueta", "Custo (R$)": custo_etiquetas,
                        "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                        "Tempo/Container (h)": 0, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0
                    })
    
    with st.expander("🏢 Armazenagem"):
        for nome in servicos["Armazenagem"]:
            if st.checkbox(nome, key=f"arm_{nome}"):
                servicos_selecionados.append(nome)
                custo = custo_pbr * 30 * qtd_pallets * qtd_containers
                custo_servicos += custo
                if nome not in custos_por_servico:
                     custos_por_servico[nome] = 0
                custos_por_servico[nome] += custo
                discriminacao.append({
                    "Serviço": nome, "Função": "Armazenagem", "Custo (R$)": custo,
                    "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                    "Tempo/Container (h)": 0, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0
                })

        # NOVO CÓDIGO: Adicionando a receita de Ad Valorem
        if st.checkbox("Ad Valorem", key="arm_advalorem"):
            servicos_selecionados.append("Ad Valorem")
            receita_ad_valorem = (advalorem_percent / 100) * valor_carga * qtd_containers
            receita_total += receita_ad_valorem
            
            # Adicionando a receita como uma entrada negativa para o gráfico de custos
            custos_por_servico["Ad Valorem (Receita)"] = -receita_ad_valorem

            discriminacao.append({
                "Serviço": "Ad Valorem", "Função": "Receita", "Custo (R$)": 0.0,
                "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros,
                "Tempo/Container (h)": 0, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0
            })


# --- Painel de Resultados (apenas se houver serviços selecionados) ---
if servicos_selecionados:
    st.markdown("---")
    st.header("📈 Resumo dos Resultados")
    
    col_metricas, col_grafico = st.columns([1, 1.5])

    markup_decimal = markup_percent / 100
    # A receita total agora é a soma do custo com markup + a receita de Ad Valorem
    receita_total += custo_servicos * (1 + markup_decimal)
    lucro_total = receita_total - custo_servicos

    with col_metricas:
        st.metric("💰 **Custo Total dos Serviços**", f"R$ {custo_servicos:,.2f}")
        
        st.metric("💲 **Receita Total (com markup)**", f"R$ {receita_total:,.2f}")
        st.metric("📊 **Lucro Bruto**", f"R$ {lucro_total:,.2f}")

        total_containers = qtd_containers
        total_pallets = qtd_containers * qtd_pallets
        total_caixas_outros = qtd_containers * qtd_caixas_outros

        st.markdown("---")
        st.subheader("Totais da Operação")
    
        st.metric("🧊 **Total de Containers**", f"{total_containers:,.0f}")
        if total_pallets > 0:
            st.metric("🧱 **Total de Pallets**", f"{total_pallets:,.0f}")
        if total_caixas_outros > 0:
            st.metric(f"🛍️ **Total de {embalagem}**", f"{total_caixas_outros:,.0f}")
        

    with col_grafico:
        st.subheader("Distribuição de Custos")
        df_custos = pd.DataFrame(list(custos_por_servico.items()), columns=['Serviço', 'Custo'])
        if not df_custos.empty:
            # Filtra apenas os custos positivos para o gráfico de pizza
            df_custos_final = df_custos[df_custos['Custo'] > 0]
            if not df_custos_final.empty:
                fig, ax = plt.subplots(figsize=(2, 2))
                ax.pie(df_custos_final['Custo'], labels=df_custos_final['Serviço'], autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
                ax.axis('equal') # Garante que o gráfico de pizza seja um círculo.
                st.pyplot(fig)
            else:
                st.info("Nenhum serviço com custo selecionado para o gráfico de pizza.")
        else:
            st.info("Nenhum serviço selecionado para calcular a distribuição de custos.")

    # --- Tabela de discriminação detalhada ---
    with st.expander("📋 Ver Discriminação Detalhada dos Custos e Receitas"):
        if discriminacao:
            df_discriminacao = pd.DataFrame(discriminacao)
            df_discriminacao = df_discriminacao.fillna(0)
            df_discriminacao.index += 1
            
            # Dicionário de mapeamento Categoria-Serviço
            categoria_map = {}
            for categoria, tipos in servicos.items():
                if isinstance(tipos, dict):
                    # Para Recebimento e Expedição, que têm subtipos por tipo_carga
                    for sub_servico in tipos[tipo_carga]:
                        # Se o serviço for "Etiquetagem", ele será tratado manualmente abaixo
                        if "Etiquetagem" not in sub_servico:
                            categoria_map[sub_servico] = categoria # Mapeia os serviços únicos (Descarga, TFA, Separação, Carregamento, Stretch)
                elif isinstance(tipos, list):
                    # Para Armazenagem
                    for sub_servico in tipos:
                        categoria_map[sub_servico] = categoria
            
            # CORREÇÃO: Mapeamento manual para os serviços de Etiquetagem para evitar sobrescrita
            # Os serviços de Etiquetagem agora têm "(Recebimento)" ou "(Expedição)" no nome na tabela 'discriminacao'
            if tipo_carga == "Batida":
                categoria_map["Etiquetagem Batida R"] = "Recebimento"
                categoria_map["Etiquetagem Batida E"] = "Expedição"
            elif tipo_carga == "Palletizada":
                categoria_map["Etiquetagem Palletizada R"] = "Recebimento"
                categoria_map["Etiquetagem Palletizada E"] = "Expedição"
            
            # Adiciona Ad Valorem (que é um serviço de receita)
            categoria_map["Ad Valorem"] = "Armazenagem"
            # Adiciona a nova coluna 'Categoria'
            df_discriminacao['Categoria'] = df_discriminacao['Serviço'].map(categoria_map)
            
            # NOVO CÓDIGO: Calcula a receita para cada item da discriminação, incluindo Ad Valorem
            def calcular_receita(row):
                if row['Serviço'] == 'Ad Valorem':
                    return (advalorem_percent / 100) * valor_carga * qtd_containers
                else:
                    # Verifica se é um custo (Custo > 0) para aplicar o markup. Se for Ad Valorem (Custo=0.0), retorna o custo * (1+markup) que é 0
                    return row['Custo (R$)'] * (1 + markup_decimal)
            
            df_discriminacao['Receita (R$)'] = df_discriminacao.apply(calcular_receita, axis=1)

            # ATUALIZADO: Inclui a coluna 'Categoria'
            df_discriminacao = df_discriminacao[[
                "Categoria", "Serviço", "Função", "Qtd Containers", "Qtd Pallets", "Qtd Caixas/Outros",
                "Demanda (h)", "HeadCount (h disponível)", "Taxa Ocupação", "Custo (R$)", "Receita (R$)"
            ]]
            
            st.dataframe(df_discriminacao.style.format({
                "Demanda (h)": "{:.2f}",
                "HeadCount (h disponível)": "{:.2f}",
                "Taxa Ocupação": "{:.2f}",
                "Custo (R$)": "R$ {:,.2f}",
                "Receita (R$)": "R$ {:,.2f}",
                "Qtd Containers": "{:.0f}",
                "Qtd Pallets": "{:.0f}",
                "Qtd Caixas/Outros": "{:.0f}"
            }))
        else:
            st.info("Nenhuma discriminação de custos e receitas disponível.")
            
    # --- Exportar para PDF ---
    with st.container(border=True):
        st.subheader("📥 Exportar Relatório")
        st.markdown("Clique no botão abaixo para baixar o seu relatório em formato PDF, com todos os detalhes e métricas calculados.")
        
        buffer = BytesIO()

        # Documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elementos = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Heading3Bold', fontName='Helvetica-Bold', fontSize=14, leading=16))
        styles.add(ParagraphStyle(name='NormalBold', fontName='Helvetica-Bold', fontSize=10))

        # Título do Relatório
        elementos.append(Paragraph("Relatório - Calculadora Armazém", styles['Title']))
        elementos.append(Spacer(1, 18))

        # Seção de Informações Básicas
        elementos.append(Paragraph("<b>Informações da Operação:</b>", styles['Heading2']))
        elementos.append(Spacer(1, 6))
        elementos.append(Paragraph(f"<b>Armazém:</b> {armazem}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Vendedor:</b> {vendedor}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Tipo de Produto:</b> {produto}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Peso por Container:</b> {peso_por_container:,.2f} toneladas", styles['Normal']))
        elementos.append(Paragraph(f"<b>Valor da Carga:</b> R$ {valor_carga:,.2f}", styles['Normal']))
        elementos.append(Spacer(1, 12))

        # Seção de Métricas Principais
        elementos.append(Paragraph("<b>Métricas Financeiras:</b>", styles['Heading2']))
        elementos.append(Spacer(1, 6))
        elementos.append(Paragraph(f"<b>Custo Total:</b> R$ {custo_servicos:,.2f}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Receita Total:</b> R$ {receita_total:,.2f}", styles['Normal']))
        elementos.append(Paragraph(f"<b>Lucro Bruto:</b> R$ {lucro_total:,.2f}", styles['Normal']))
        elementos.append(Spacer(1, 12))

        # Seção de Totais da Operação
        elementos.append(Paragraph("<b>Totais da Operação:</b>", styles['Heading2']))
        elementos.append(Spacer(1, 6))
        elementos.append(Paragraph(f"Containers: {total_containers:,.0f}", styles['Normal']))
        if total_pallets > 0:
            elementos.append(Paragraph(f"Pallets: {total_pallets:,.0f}", styles['Normal']))
        if total_caixas_outros > 0:
            elementos.append(Paragraph(f"{embalagem}: {total_caixas_outros:,.0f}", styles['Normal']))
        elementos.append(Spacer(1, 12))

        # Seção de Discriminação Detalhada
        elementos.append(Paragraph("<b>Discriminação de Custos e Receitas por Serviço:</b>", styles['Heading2']))
        elementos.append(Spacer(1, 6))

        if 'df_discriminacao' in locals() and not df_discriminacao.empty:
            # Formata os dados para a tabela
            df_formatado = df_discriminacao.copy()

            # ATUALIZADO: Inclui a coluna 'Categoria'
            cols_to_display = ["Categoria", "Serviço", "Função", "Demanda (h)", "Custo (R$)", "Receita (R$)"]
            
            # CORREÇÃO: Cria uma cópia explícita do DataFrame para evitar o SettingWithCopyWarning
            df_display = df_formatado[cols_to_display].copy()

            # Formata as colunas para strings
            df_display["Demanda (h)"] = df_display["Demanda (h)"].apply(lambda x: f"{x:.2f}")
            df_display["Custo (R$)"] = df_display["Custo (R$)"].apply(lambda x: f"R$ {x:,.2f}")
            df_display["Receita (R$)"] = df_display["Receita (R$)"].apply(lambda x: f"R$ {x:,.2f}")

            tabela_dados = [df_display.columns.tolist()] + df_display.values.tolist()

            tabela = Table(tabela_dados)
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')), # Azul escuro para o cabeçalho
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f2f2f2')), # Cor de fundo alternada
            ]))
            elementos.append(tabela)

        # NOVO: Adiciona a data e hora de impressão no final do PDF com fuso horário de Brasília
        elementos.append(Spacer(1, 24))
        try:
            fuso_brasilia = pytz.timezone('America/Sao_Paulo')
            data_impressao = datetime.now(fuso_brasilia).strftime("Relatório gerado em: %d/%m/%Y às %H:%M:%S")
        except NameError:
            # Se pytz não estiver importado (embora esteja no início do script)
            data_impressao = datetime.now().strftime("Relatório gerado em: %d/%m/%Y às %H:%M:%S (Hora Local)")

        elementos.append(Paragraph(data_impressao, styles['Normal']))

        # Construir o PDF
        doc.build(elementos)

        # Botão de download
        st.download_button(
            label="📥 **Baixar Relatório em PDF**",
            data=buffer.getvalue(),
            file_name=f"relatorio_armazem_{cliente or 'sem_cliente'}.pdf",
            mime="application/pdf"
        )