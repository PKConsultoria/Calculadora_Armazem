import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuração inicial da página ---
st.set_page_config(page_title="Calculadora Armazém", page_icon="🏭", layout="wide")

# --- Título principal e subtítulo ---
st.title("🏭 Calculadora de Receitas e Custos - Armazém")
st.markdown("Calcule de forma rápida e intuitiva os custos e receitas de uma operação logística.")

# Dicionários de dados para facilitar a manutenção
VALORES_SERVICOS = {
    "Descarga Batida": 100.0, "Descarga Palletizada": 80.0,
    "Etiquetagem Batida": 0.50, "Etiquetagem Palletizada": 0.30,
    "TFA": 200.0, "Separação Batida": 1.20,
    "Separação Palletizada": 5.0, "Carregamento Batido": 90.0,
    "Carregamento Palletizado": 70.0, "Diária": 2.0,
    "Pico Quinzenal": 500.0, "Pico Mensal": 900.0
}

FUNCOES_CUSTOS = {
    "Descarga": [
        {"nome": "Conferente", "salario": 4052.17, "tempo": 120},
        {"nome": "Analista", "salario": 4780.41, "tempo": 10},
        {"nome": "Supervisor", "salario": 6775.58, "tempo": 45},
        {"nome": "Mão de Obra de Terceiros", "salario": 330, "tempo": 120},
        {"nome": "Máquina Elétrica", "salario": 47.6, "tempo": 120},
        {"nome": "Stretch", "salario": 6.85, "tempo": 0}
    ],
    "Etiquetagem": [
        {"nome": "Assistente", "salario": 3713.31, "tempo": 1 / 3600},
        {"nome": "Etiqueta", "salario": 0.06, "tempo": 0}
    ],
    "TFA": [{"nome": "Conferente", "salario": 4052.17, "tempo": 120}],
    "Separação": [
        {"nome": "Conferente", "salario": 4052.17, "tempo": 10},
        {"nome": "Máquina Elétrica", "salario": 47.6, "tempo": 10}
    ],
    "Carregamento": [
        {"nome": "Conferente", "salario": 4052.17, "tempo": 120},
        {"nome": "Analista", "salario": 4780.41, "tempo": 10},
        {"nome": "Coordenador", "salario": 7774.15, "tempo": 45},
        {"nome": "Mão de Obra de Terceiros", "salario": 330, "tempo": 120},
        {"nome": "Máquina GLP", "salario": 64.72, "tempo": 120},
    ]
}

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

# Usando um formulário para agrupar as entradas e acionar o cálculo com um botão
with st.form("main_form"):
    st.header("🏗️ Detalhes da Operação")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_carga = st.selectbox("Tipo de Carga", ["Batida", "Palletizada"])
        qtd_containers = st.number_input("Quantidade de Containers", min_value=0, step=1)
    
    with col2:
        qtd_pallets = st.number_input("Quantidade de Pallets por Container", min_value=0, step=1)
        peso_por_container = st.number_input("Peso (toneladas) de 1 Container", min_value=0.0, step=0.1, format="%.2f")

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
    
    st.markdown("---")
    st.header("🛠️ Serviços")
    
    servicos_selecionados = []
    
    st.info(f"⏱️ Tempo estimado de execução por operação: **{120 if tipo_carga == 'Batida' else 30} minutos**")

    # Checkbox para Recebimento
    if st.checkbox("📥 Incluir Recebimento"):
        servicos_selecionados.extend([f"Descarga {tipo_carga}", "Etiquetagem Batida" if tipo_carga == "Batida" else "Etiquetagem Palletizada", "TFA"])
    
    # Checkbox para Expedição
    if st.checkbox("📦 Incluir Expedição"):
        servicos_selecionados.extend([f"Separação {tipo_carga}", f"Carregamento {tipo_carga}", f"Etiquetagem {tipo_carga}"])
        
    # Checkbox para Armazenagem
    if st.checkbox("🏢 Incluir Armazenagem"):
        servicos_selecionados.extend(["Diária", "Pico Quinzenal", "Pico Mensal"])

    st.markdown("---")
    st.header("💰 Receitas")
    
    receitas_por_servico = {}
    for servico in servicos_selecionados:
        receita_unit = st.number_input(f"Receita por {servico} (R$)", min_value=0.0, step=1.0, format="%.2f", key=f"receita_{servico}")
        receitas_por_servico[servico] = receita_unit
    
    submitted = st.form_submit_button("Calcular Custos e Lucros")


if submitted:
    # Validação
    if qtd_containers > 0 and qtd_pallets == 0 and qtd_caixas_outros == 0:
        st.warning("A soma da quantidade de pallets e caixas/outros por container deve ser maior que 0 para o cálculo.")
        st.stop()

    def calcular_custo(nome_servico, qtd_containers, qtd_pallets, qtd_caixas_outros, dias_trabalhados, horas_trabalhadas_dia, eficiencia):
        custo_total = 0.0
        discriminacao_detalhada = []
        headcount_val = dias_trabalhados * horas_trabalhadas_dia * (eficiencia / 100)
        unidades_totais = qtd_pallets if "Palletizada" in nome_servico or "Etiquetagem Palletizada" in nome_servico else qtd_caixas_outros

        if "Descarga" in nome_servico:
            funcoes = FUNCOES_CUSTOS["Descarga"]
            for func in funcoes:
                custo = 0
                tempo_horas_total = 0
                taxa_ocupacao = 0
                
                if func["nome"] == "Stretch":
                    custo = func["salario"] * qtd_pallets * qtd_containers
                elif func["nome"] == "Mão de Obra de Terceiros":
                    custo = func["salario"] * qtd_containers
                elif func["nome"] == "Máquina Elétrica":
                    demanda_horas = (func["tempo"] / 60) * qtd_containers
                    taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                    custo = func["salario"] * taxa_ocupacao * demanda_horas
                else: # Mão de obra (Conferente, Analista, Supervisor)
                    tempo_horas_total = (func["tempo"] / 60) * qtd_containers
                    taxa_ocupacao = (tempo_horas_total / headcount_val) if headcount_val > 0 else 0
                    custo = func["salario"] * taxa_ocupacao
                
                custo_total += custo
                discriminacao_detalhada.append({"Serviço": nome_servico, "Função": func["nome"], "Custo (R$)": custo, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": tempo_horas_total, "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao})

        elif "Etiquetagem" in nome_servico:
            unidades_para_etiquetagem = qtd_pallets * qtd_containers if "Palletizada" in nome_servico else qtd_caixas_outros * qtd_containers
            
            # Custo do Assistente de Etiquetagem
            salario_assistente = FUNCOES_CUSTOS["Etiquetagem"][0]["salario"]
            tempo_por_unidade_h = 1 / 3600
            demanda_horas = tempo_por_unidade_h * unidades_para_etiquetagem
            taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
            custo_assistente = salario_assistente * taxa_ocupacao * demanda_horas
            
            custo_total += custo_assistente
            discriminacao_detalhada.append({"Serviço": nome_servico, "Função": "Assistente", "Custo (R$)": custo_assistente, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": demanda_horas, "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao})

            # Custo da Etiqueta
            custo_etiqueta_unitario = FUNCOES_CUSTOS["Etiquetagem"][1]["salario"]
            custo_etiquetas = custo_etiqueta_unitario * unidades_para_etiquetagem
            custo_total += custo_etiquetas
            discriminacao_detalhada.append({"Serviço": nome_servico, "Função": "Etiqueta", "Custo (R$)": custo_etiquetas, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0})
            
        elif "TFA" in nome_servico:
            func = FUNCOES_CUSTOS["TFA"][0]
            tempo_conferente_tfa_h = func["tempo"] / 60
            demanda_horas_tfa = tempo_conferente_tfa_h * qtd_containers
            taxa_ocupacao_tfa = (demanda_horas_tfa / headcount_val) if headcount_val > 0 else 0
            custo_conferente_tfa = func["salario"] * taxa_ocupacao_tfa
            custo_total += custo_conferente_tfa
            discriminacao_detalhada.append({"Serviço": nome_servico, "Função": "Conferente", "Custo (R$)": custo_conferente_tfa, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": demanda_horas_tfa, "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao_tfa})

        elif "Separação" in nome_servico:
            funcoes = FUNCOES_CUSTOS["Separação"]
            unidades_demanda = qtd_containers * qtd_caixas_outros
            for func in funcoes:
                demanda_horas = (func["tempo"] / 3600) * unidades_demanda
                taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                custo = func["salario"] * taxa_ocupacao if func["nome"] != "Máquina Elétrica" else func["salario"] * taxa_ocupacao * demanda_horas
                custo_total += custo
                discriminacao_detalhada.append({"Serviço": nome_servico, "Função": func["nome"], "Custo (R$)": custo, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": demanda_horas, "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao})

        elif "Carregamento" in nome_servico:
            funcoes = FUNCOES_CUSTOS["Carregamento"]
            for func in funcoes:
                custo = 0
                tempo_horas_total = 0
                taxa_ocupacao = 0
                if func["nome"] == "Mão de Obra de Terceiros":
                    custo = func["salario"] * qtd_containers
                elif func["nome"] == "Máquina GLP":
                    demanda_horas = (func["tempo"] / 60) * qtd_containers
                    taxa_ocupacao = (demanda_horas / headcount_val) if headcount_val > 0 else 0
                    custo = func["salario"] * taxa_ocupacao * demanda_horas
                else: # Mão de obra
                    tempo_horas_total = (func["tempo"] / 60) * qtd_containers
                    taxa_ocupacao = (tempo_horas_total / headcount_val) if headcount_val > 0 else 0
                    custo = func["salario"] * taxa_ocupacao
                custo_total += custo
                discriminacao_detalhada.append({"Serviço": nome_servico, "Função": func["nome"], "Custo (R$)": custo, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": tempo_horas_total, "HeadCount (h disponível)": headcount_val, "Taxa Ocupação": taxa_ocupacao})
        else: # Armazenagem
            custo_total = VALORES_SERVICOS[nome_servico]
            discriminacao_detalhada.append({"Serviço": nome_servico, "Função": "N/A", "Custo (R$)": custo_total, "Qtd Containers": qtd_containers, "Qtd Pallets": qtd_pallets, "Qtd Caixas/Outros": qtd_caixas_outros, "Demanda (h)": 0, "HeadCount (h disponível)": 0, "Taxa Ocupação": 0})
        
        return custo_total, discriminacao_detalhada
    
    # Executa os cálculos
    custo_servicos = 0.0
    custos_por_servico = {}
    discriminacao = []
    
    for servico in servicos_selecionados:
        custo, detalhes = calcular_custo(servico, qtd_containers, qtd_pallets, qtd_caixas_outros, dias_trabalhados, horas_trabalhadas_dia, eficiencia)
        custo_servicos += custo
        custos_por_servico[servico] = custo
        discriminacao.extend(detalhes)
    
    # --- Painel de Resultados ---
    st.markdown("---")
    st.header("📈 Resumo dos Resultados")
    
    col_metricas, col_grafico = st.columns([1, 1.5])

    with col_metricas:
        st.subheader("Custos da Operação")
        st.metric("💰 **Custo Total dos Serviços**", f"R$ {custo_servicos:,.2f}")
    
    total_containers = qtd_containers
    total_pallets = qtd_containers * qtd_pallets
    total_caixas_outros = qtd_containers * qtd_caixas_outros

    if any(s in receitas_por_servico for s in servicos_selecionados):
        receita_total = sum(receitas_por_servico.get(s, 0) for s in servicos_selecionados)
        lucro = receita_total - custo_servicos
        margem_lucro = (lucro / receita_total) * 100 if receita_total > 0 else 0
        
        with col_metricas:
            st.markdown("---")
            st.subheader("Receita e Lucro")
            st.metric("💵 **Receita Total**", f"R$ {receita_total:,.2f}")
            st.metric("✅ **Lucro Estimado**", f"R$ {lucro:,.2f}")
            st.metric("📊 **Margem de Lucro**", f"{margem_lucro:,.2f}%")
            
    with col_metricas:
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
            df_custos_final = df_custos[df_custos['Custo'] > 0]
            if not df_custos_final.empty:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(df_custos_final['Custo'], labels=df_custos_final['Serviço'], autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
                ax.axis('equal') # Garante que o gráfico de pizza seja um círculo.
                st.pyplot(fig)
            else:
                st.info("Nenhum custo calculado para exibir o gráfico.")
        else:
            st.info("Nenhum serviço selecionado para calcular a distribuição de custos.")

    # --- Tabela de discriminação detalhada ---
    with st.expander("📋 Ver Discriminação Detalhada dos Custos"):
        if discriminacao:
            df_discriminacao = pd.DataFrame(discriminacao)
            df_discriminacao = df_discriminacao.fillna(0)
            df_discriminacao.index += 1
            
            df_discriminacao = df_discriminacao[[
                "Serviço", "Função", "Qtd Containers", "Qtd Pallets", "Qtd Caixas/Outros",
                "Demanda (h)", "HeadCount (h disponível)", "Taxa Ocupação", "Custo (R$)"
            ]]
            
            st.dataframe(df_discriminacao.style.format({
                "Demanda (h)": "{:.2f}",
                "HeadCount (h disponível)": "{:.2f}",
                "Taxa Ocupação": "{:.2f}",
                "Custo (R$)": "R$ {:,.2f}",
                "Qtd Containers": "{:.0f}",
                "Qtd Pallets": "{:.0f}",
                "Qtd Caixas/Outros": "{:.0f}"
            }))
        else:
            st.info("Nenhuma discriminação de custos disponível.")