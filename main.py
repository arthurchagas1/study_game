import streamlit as st
import json
import sqlite3

# Função para salvar o progresso do usuário em um arquivo JSON
def save_progress(progresso_usuario):
    with open("progresso_usuario.json", "w") as file:
        json.dump(progresso_usuario, file)

def load_progress():
    try:
        with open("progresso_usuario.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função principal
def main():
    # Inicializa o progresso do usuário
    progresso_usuario = load_progress()

    # Carrega os tópicos por matéria do ENEM
    topicos_enem = {
        "GEOGRAFIA": [
            "Cartografia", "Superfícies da Terra", "Hidrografia", "Mecanismos do Clima e Circulação Atmosférica",
            "Características Climáticas do Território Brasileiro", "Vegetação e Domínios da Natureza no Mundo",
            "Vegetação e Domínios da Natureza no Brasil", "Problemas Ambientais", "Política Ambiental Brasileira",
            "Mudanças Climáticas", "Conferências Ambientais", "Fontes de Energia", "Matriz Energética",
            "Mundialização do Capitalismo", "As Grandes Instituições Financeiras Mundiais", "A Formação dos Blocos Econômicos",
            "Organizações Mundiais", "Globalização", "Nova Divisão Internacional do Trabalho", "As Transformações no Leste Europeu (Guerra Fria e Cortina de Ferro)",
            "Nova Ordem Mundial (China, Rússia e Estados Unidos)", "Conflitos na Ásia, no Oriente Médio, na África e na América Latina",
            "A Questão Agrária Brasileira", "A Industrialização da Agricultura e a Pecuária no Brasil", "Processos Migratórios",
            "Urbanização", "A Questão Urbana e os Problemas Urbanos do Brasil", "Organização do Estado Brasileiro", "Geografia da Saúde",
            "Geografia Cultural"
        ],
        "FILOSOFIA": [
            "Introdução à Filosofia", "Pré-Socráticos", "Sócrates e os Sofistas", "Platão", "Aristóteles", "Filosofia Medieval",
            "Filosofia Helênica", "Filosofia Moderna", "Filosofia Moral", "Antropologia", "Ócio e Trabalho", "Filosofia Contemporânea",
            "Teoria Crítica", "Política", "Filosofia Pós-Moderna"
        ],
        "SOCIOLOGIA": [
            "Introdução à Sociologia", "Emile Durkheim", "Max Weber", "Karl Marx", "Indivíduo e Sociedade", "Cultura e Sociedade",
            "Raça, Etnia e Multiculturalismo", "Socialização", "Controle Social", "Estado, Política e Poder", "Democracia, Direitos Humanos e Cidadania",
            "Movimentos Sociais", "Sociologia do Brasil", "Trabalho e Sociedade", "Desigualdade Social", "A Sociedade e o Espaço Urbano",
            "Globalização", "Gênero e Sexualidade", "Violência", "Sistema Prisional", "Internet e Redes Sociais", "Preconceito Racial",
            "Representatividade e Exclusão", "Biopolítica", "Necropolítica", "Sociologia Contemporânea", "Escola de Frankfurt e a Indústria Cultural"
        ],
        "HISTORIA GERAL": [
            "Pré-História", "Antiguidade Oriental", "Grécia", "Roma", "Idade Média Ocidental", "Idade Média Oriental",
            "Renascimento Cultural", "Reforma Protestante", "Formação das Monarquias Nacionais", "Mercantilismo", "Absolutismo",
            "Revoluções Inglesas do Século XVII", "Revolução Industrial", "Iluminismo", "Fisiocracia", "Liberalismo", "Processo de Independência dos Estados Unidos",
            "Revolução Francesa", "Era Napoleônica", "Expansão dos Estados Unidos para o Oeste e a Guerra de Secessão", "Imperialismo",
            "Segunda Revolução Industrial", "Unificação da Alemanha e da Itália", "Primeira Guerra Mundial", "Revolução Russa",
            "Período Entreguerras (Crise de 1929 e a Ascensão do Totalitarismo)", "Segunda Guerra Mundial", "Guerra Fria",
            "Crise dos Mísseis de Cuba", "Mundo Pós-Guerra Fria"
        ],
        "HISTORIA DO BRASIL": [
            "As Grandes Navegações", "Brasil Pré-Cabralino ou Pré-Colonial", "Modelo de Colonização (Capitanias Hereditárias e o Governo-Geral)",
            "Sistema Açucareiro", "União Ibérica", "Período Holandês", "Bandeiras, Entradas, Monções e Expansão das Fronteiras do Brasil",
            "Movimentos Nativistas", "Ciclo da Mineração", "Período Pombalino", "Movimentos Emancipacionistas", "Período Joanino",
            "Processo de Independência do Brasil", "Primeiro Reinado", "Período Regencial", "Revoltas Regenciais", "Segundo Reinado",
            "Processo de Proclamação da República", "Escravidão", "Primeira República", "Era Vargas", "Governo de Dutra",
            "Segundo Governo de Vargas", "Governo de Juscelino Kubitschek", "Governo de Jânio Quadros", "Governo de João Goulart",
            "Primeiros Governos Militares (Castelo Branco e Costa e Silva)", "Ditadura Militar", "República Nova"
        ],
        "BIOLOGIA": [
            "Método Científico", "Origem da Vida", "Água", "Sais Minerais", "Vitaminas", "Ácidos Nucleicos (RNA e DNA)",
            "Duplicação do DNA", "Transcrição do RNA, Tradução, Síntese Proteica e OPERON", "Mutações Gênicas", "Lipídios",
            "Carboidratos", "Proteínas", "Enzimas", "Citologia (Eucariontes e Procariontes)", "Membrana Plasmática e seus Transportes",
            "Citoplasma e Organelas Citoplasmáticas", "Núcleo e Cariótipo Celular", "Ciclo de Vida Celular e Divisão Celular",
            "Erros Cromossômicos", "Bioenergética", "Fotossíntese", "Quimiossíntese", "Respiração Celular", "Fermentação (Alcoólica, Láctica e Acéptica)",
            "Reprodução Geral dos Animais e dos Vegetais", "Anatomia e Fisiologia dos Sistemas Reprodutores Masculino e Feminino",
            "Métodos Contraceptivos e Infecções Sexualmente Transmissíveis", "Embriologia", "Gestação e Ciclo Menstrual",
            "Tecido Epitelial", "Tecido Conjuntivo", "Tecido Sanguíneo", "Coagulação, Imunização, Soro, Vacina e Alergia",
            "Tecido Muscular", "Tecido Nervoso", "Ecologia (Cadeias Alimentares, Pirâmides Ecológicas e Fluxo de Energia)",
            "Ciclos Biogeoquímicos (Carbono, Nitrogênio, Oxigênio, Água, Enxofre e Fósforo)", "Dinâmica das Populações e Relações Ecológicas",
            "Sucessões Ecológicas", "Biomas Aquáticos e Biomas Terrestres", "Biomas Brasileiros", "Poluição", "Evolução",
            "Especiações e Evolução Humana", "Sistema Digestório", "Sistema Circulatório", "Sistema Respiratório", "Sistema Excretor",
            "Sistema Endócrino", "Sistema Nervoso", "Taxonomia e Filogenia", "Grupos Vegetais", "Morfologia e Fisiologia das Plantas",
            "Genética Mendeliana (1° Lei de Mendel, 2° Lei de Mendel e Heredogramas)", "Biotecnologia", "Programa de Saúde",
            "Agentes Patogênicos (Vírus, Bactérias, Protozoários, Algas e Fungos)", "Doenças Parasitárias do Brasil (Viroses, Bacterioses e Protozooses)",
            "Verminoses do Brasil", "Doenças Causadas por Platelmintos e Nematelmintos", "Zoologia dos Invertebrados",
            "Equinodermos e Protocordados", "Cordados Vertebrados", "Aves e Mamíferos"
        ],
        "QUIMICA": [
            "Mudanças de Estado Físico e Diagrama de Fases", "Métodos de Separação de Misturas", "Grandezas Químicas", "Estequiometria",
            "Gases", "Densidade", "Alotropia", "Distribuição Eletrônica e Características da Tabela Periódica", "Propriedades Periódicas",
            "Ligação Iônica", "Ligação Covalente", "Ligação Metálica", "Ligação Intermolecular", "Funções Inorgânicas (Ácido)",
            "Funções Inorgânicas (Base)", "Funções Inorgânicas (Sais)", "Funções Inorgânicas (Óxidos)", "Reações Inorgânicas de Síntese e de Adição",
            "Reações de Simples Troca e de Dupla Troca", "Coeficiente de Solubilidade", "Concentração das Soluções", "Diluição e Concentração das Soluções",
            "Reações Químicas em Solução", "Termoquímica", "Radioatividade", "Eletrólise", "Pilhas", "Cinética Química",
            "Equilíbrio Químico", "Equilíbrio Iônico", "Hidrólise", "Produto de Solubilidade", "Solução Tampão", "Equação de Gibbs e Espontaneidade",
            "Oxidação e Redução", "Propriedades e Classificações do Carbono", "Hibridação do Carbono e Classificação das Cadeias Carbônicas",
            "Hidrocarbonetos", "Funções Oxigenadas", "Funções Nitrogenadas", "Isomeria Plana", "Isomeria Espacial Geométrica",
            "Isomeria Espacial Óptica", "Acidez e Basicidade", "Reações Orgânicas", "Saponificação, Detergente e Sabão",
            "Transesterificação e Biodiesel", "Lixo, Lixão, Aterro Controlado e Aterro Sanitário"
        ],
        "FISICA": [
            "Velocidade Média e Aceleração Média", "Movimento Retilíneo Uniforme", "Movimento Retilíneo Uniformemente Variado",
            "Aplicações do MRU e do MRUV", "Cinemática Vetorial", "Lançamento Horizontal", "Lançamento Oblíquo", "Movimento Circular",
            "Leis de Newton", "Força Elástica", "Roldanas e Sistema de Força", "Força de Atrito", "Força Centrípeta", "Gravitação",
            "Trabalho e Potência", "Energia e sua Conservação", "Impulso e Quantidade de Movimento", "Estática dos Sólidos", "Hidrostática",
            "Temperatura e Calor", "Dilatação", "Calor Sensível e Calor Latente", "Gás Ideal e suas Transformações", "1° Lei da Termodinâmica e 2° Lei da Termodinâmica",
            "Fundamentos da Óptica Geométrica", "Reflexão, Espelhos Planos e Espelhos Esféricos", "Refração da Luz", "Lentes Esféricas",
            "Óptica da Visão", "Fundamentos da Ondulatória", "Ondas em Cordas", "Fenômenos Ondulatórios", "Acústica", "Tubos Sonoros",
            "Cordas Vibrantes", "Carga Elétrica", "Força e Campo Elétrico", "Potencial Elétrico", "Corrente Elétrica", "1° Lei de Ohm e 2° Lei de Ohm",
            "Medidores e Circuitos Elétricos", "Gerador Elétrico", "Receptor Elétrico", "Circuito com Gerador, Receptor e Resistor", "Capacitores e Ponte de Wheatstone",
            "Imã e Campo Magnético", "Campo Magnético e Corrente Elétrica", "Força Magnética", "Indução Eletromagnética", "Aplicações do Magnetismo"
        ],
        "MATEMATICA": [
            "Conjuntos Numéricos", "Problemas do 1° Grau", "Problemas do 2° Grau", "Razão e Proporção", "Porcentagem", "Geometria Plana",
            "Análise Combinatória", "Probabilidade", "Função Afim (Função do 1° Grau)", "Função Quadrática (Função do 2° Grau)", "Função Exponencial",
            "Logarítmo", "Sequências Numéricas", "Progressões Aritméticas", "Progressões Geométricas", "Geometria Analítica", "Geometria Espacial",
            "Trigonometria", "Estatística", "Juros Simples", "Juros Composto", "Matemática Básica (Multiplicação, Divisão, Soma, Subtração, MMC, MDC, Potenciação, Radiciação, Dízimas, Frações, Decimais e Notação Científica)",
            "Regra de Três", "Escala"
        ],
        "GRAMATICA": [
            "Hífen", "Vírgula", "Crase", "Pontuação", "Pronomes", "Operadores Argumentativos", "Orações Coordenadas e Subordinadas",
            "Gêneros e Tipos Textuais", "Variação Linguística", "Concordância Verbal", "Concordância Nominal", "Regência", "Figuras de Linguagem",
            "Funções da Linguagem", "Sintaxe", "Charge, Cartum e Tirinha", "Característica da Poesia e da Prosa", "Campanhas e Textos Publicitários",
            "Processos de Formação das Palavras"
        ],
        "LITERATURA": [
            "Barroco", "Arcadismo", "Romantismo", "Realismo", "Naturalismo", "Parnasianismo", "Simbolismo", "Modernismo", "Pós-Modernismo"
        ],
        "REDACAO": [
            "Tipologia Textual", "Interpretação de Texto", "Análise Crítica de Texto", "Texto Argumentativo", "Coesão e Coerência", "Estrutura e Organização Textual",
            "Paragrafação", "Construção do Parágrafo", "Estilo e Variação Linguística", "Adequação da Linguagem ao Contexto", "Vícios de Linguagem",
            "Norma Culta", "Erros Gramaticais Comuns", "Pontuação", "Ortografia", "Acentuação Gráfica", "Concordância Verbal e Nominal",
            "Regência Verbal e Nominal", "Crase", "Tipos de Discurso", "Discurso Direto e Indireto", "Gêneros Textuais", "Narrativa", "Descrição",
            "Dissertação", "Artigo de Opinião", "Resenha", "Carta Argumentativa", "Resumo", "Entrevista", "Biografia", "Documentário",
            "Ensaio", "Relato de Viagem", "Notícia", "Reportagem", "Entrevista", "Diário Pessoal", "Blog", "Fórum de Discussão",
            "Twitter e Redes Sociais", "Cinema, Teatro, TV, Rádio e Música", "Gêneros Literários", "Literatura Brasileira", "Literatura Portuguesa",
            "Literatura Africana e Indígena", "Literatura Inglesa e Norte-Americana", "Literatura Hispânica e Latina", "Literatura Asiática e Oriental",
            "Contos, Crônicas e Poesias", "Teoria Literária", "Figuras de Linguagem", "Gêneros do Discurso", "Movimentos Literários",
            "Escolas Literárias", "Autores e Obras", "Aspectos Sociais, Históricos e Culturais Relacionados às Obras Literárias"
        ]
    }

    # Define o título do aplicativo
    st.title("Preparação para o ENEM")

    # Barra lateral para selecionar o vestibular
    vestibular = st.sidebar.selectbox("Selecione o vestibular", ["ENEM"])

    # Barra lateral para selecionar a matéria
    materia_selecionada = st.sidebar.selectbox("Selecione a matéria", list(topicos_enem.keys()))

    # Obtém os tópicos da matéria selecionada
    topicos_materia = topicos_enem.get(materia_selecionada, [])

    lel = st.sidebar.checkbox("Todos os tópicos dessa matéria foram concluídos?", value = False)
    
    if lel: 
        st.sidebar.markdown("[Clique aqui para ir para a página de provas e resgatar seu premio](http://seu-link-aqui)")
        save_progress(progresso_usuario)
    
    for topico in topicos_materia:
        # Exibe o checkbox para marcar o tópico como concluído
        progresso_usuario.setdefault(vestibular, {}).setdefault(materia_selecionada, {}).setdefault(topico, False)
        progresso_usuario[vestibular][materia_selecionada][topico] = st.checkbox(topico, value=progresso_usuario[vestibular][materia_selecionada][topico])

        # Salva o progresso do usuário
        save_progress(progresso_usuario)   # Executa a função principal

    save_progress(progresso_usuario)

if __name__ == "__main__":
    main()
