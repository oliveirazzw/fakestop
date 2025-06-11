import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
import sqlite3

# Carregar variáveis de ambiente
load_dotenv()             
openai_api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o modelo de linguagem com o provedor correto (GPT-4o-mini)
llm = LLM(
    model="gpt-4o-mini",  # Especificando o modelo gpt-4o mini
    temperature=0.7
)

# === AGENTES: COLETOR, LINGUISTA E VERIFICADOR ===

coletor = Agent(
    role="Agente Coletor",
    goal="Buscar e apresentar notícias semelhantes à fornecida",
    backstory="Especialista em recuperar textos similares da internet ou arquivos históricos",
    verbose=True,
    llm=llm
)

linguista = Agent(
    role="Agente Linguístico",
    goal="Avaliar o tom, estilo e estrutura da notícia",
    backstory="Expert em análise linguística e detecção de padrões retóricos",
    verbose=True,
    llm=llm
)

verificador = Agent(
    role="Agente Verificador de Fatos",
    goal="Comparar as informações da notícia com dados verificáveis e confiáveis",
    backstory="Profissional de checagem de fatos com acesso a várias fontes verificadas",
    verbose=True,
    llm=llm
)

# === TAREFAS DOS AGENTES ACIMA ===

tarefa_coletor = Task(
    description="Coletar notícias semelhantes à seguinte: {{noticia}}",
    expected_output="Uma lista de resumos de notícias semelhantes encontradas.",
    agent=coletor
)

tarefa_linguista = Task(
    description="Analisar o tom, estilo e estrutura da seguinte notícia: {{noticia}}",
    expected_output="Um relatório descrevendo o tom (neutro, sensacionalista, alarmista, etc), estilo de escrita e padrões linguísticos detectados.",
    input="coletor_md",
    agent=linguista,
    output_file="analise_linguistica.md"
)

tarefa_verificador = Task(
    description="Comparar a seguinte notícia com fatos reais e bancos de dados confiáveis: {{noticia}}",
    expected_output="Uma verificação detalhada dos principais pontos da notícia, indicando se há inconsistências ou falsas alegações.",
    input="analise_linguistica.md",
    agent=verificador
)

# == Agente classificador e sua tarefa

classificador = Agent(
    role="Agente Classificador",
    goal="Determinar se a notícia é confiável, dúbia ou falsa, com justificativa",
    backstory="Analista final responsável por classificar a notícia com base nos dados dos outros agentes",
    verbose=True,
    llm=llm
)

tarefa_classificador = Task(
    description="Com base nas análises anteriores, classifique a seguinte notícia: {{noticia}}",
    expected_output="Classificação final: Confiável, Dúbia ou Falsa, com justificativa.",
    agent=classificador
)

# === CREW - Primeira Crew (Coletor, Linguista e Verificador) ===

equipe = Crew(
    agents=[coletor, linguista, verificador],
    tasks=[tarefa_coletor, tarefa_linguista, tarefa_verificador],
    process=Process.sequential,
    verbose=True
)

# === CREW - Segunda Crew (Classificador) ===
eqp_classificacao = Crew(
    agents=[classificador],
    tasks=[tarefa_classificador],
    process=Process.sequential,
    llm=llm
)

# === Funções do Banco de Dados ===

# Conectar ao banco de dados SQLite
def conectar_db():
    return sqlite3.connect('analises.db')

# Função para criar a tabela de análises, caso não exista
def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        noticia TEXT,
        coletor_resultado TEXT,
        linguista_resultado TEXT,
        verificador_resultado TEXT,
        classificacao_resultado TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Criar a tabela ao iniciar o aplicativo
criar_tabela()

# Inserir dados no banco de dados
def inserir_analise(noticia, coletor_resultado, linguista_resultado, verificador_resultado, classificacao_resultado):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO analises (noticia, coletor_resultado, linguista_resultado, verificador_resultado, classificacao_resultado)
    VALUES (?, ?, ?, ?, ?)
    ''', (noticia, coletor_resultado, linguista_resultado, verificador_resultado, classificacao_resultado))
    conn.commit()
    conn.close()

# Buscar histórico de análises
def buscar_historico():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analises ORDER BY id DESC')
    historico = cursor.fetchall()
    conn.close()
    return historico

# === INTERFACE STREAMLIT ===

# Função para exibir o histórico de análises
def exibir_historico():
    historico = buscar_historico()
    if historico:
        for analise in historico:
            st.subheader(f"Análise #{analise[0]}")
            st.write(f"**Notícia:** {analise[1]}")
            st.write(f"**Resultado do Coletor:** {analise[2]}")
            st.write(f"**Resultado do Linguista:** {analise[3]}")
            st.write(f"**Resultado do Verificador:** {analise[4]}")
            st.write(f"**Resultado da Classificação:** {analise[5]}")
            st.divider()
    else:
        st.write("Ainda não há histórico de análises.")

# Função para exibir os resultados das tarefas da primeira crew
def exibir_resultados_primeira_crew(resultado):
    try:
        if hasattr(resultado, 'tasks_output'):
            tasks_output = resultado.tasks_output  # Usando um método para acessar os outputs das tarefas
            for i, task_output in enumerate(tasks_output):
                st.subheader(f"🧑‍💼 {task_output.agent} - Tarefa {i+1}")
                st.markdown(f"**Descrição da Tarefa:**\n\n{task_output.description}")
                st.markdown(f"**Resultado:**\n\n{task_output.raw.strip()}")
                st.divider()
        else:
            st.error("A chave ou método 'tasks_output' não foi encontrado no resultado.")
    except Exception as e:
        st.error(f"Erro ao acessar os dados: {str(e)}")
        
st.title("🔍 Verificador de Notícias com IA - CrewAI")

# Criar abas
aba_analise, aba_historico = st.tabs(["📰 Nova Análise", "📚 Histórico de Análises"])

with aba_analise:
    noticia = st.text_area("📄 Cole aqui a notícia que você quer verificar")

    if st.button("Verificar"):
        if noticia.strip() == "":
            st.warning("⚠️ Por favor, insira uma notícia para verificar.")
        else:
            with st.spinner("🧠 Aguardando análise completa pelos agentes..."):
                resultado = equipe.kickoff(inputs={"noticia": noticia})
        
            st.success("✅ Análise Concluída na Primeira Crew!")
            exibir_resultados_primeira_crew(resultado)

            with st.spinner("🔍 Realizando a classificação..."):
                resultado_classificacao = eqp_classificacao.kickoff(inputs={"noticia": noticia})

            st.success("✅ Classificação Concluída!")

            st.subheader("📊 Resultado da Classificação")
            try:
                if hasattr(resultado_classificacao, 'tasks_output'):
                    tasks_output = resultado_classificacao.tasks_output
                    for i, task_output in enumerate(tasks_output):
                        st.subheader(f"🧑‍💼 {task_output.agent} - Tarefa {i+1}")
                        st.markdown(f"**Descrição da Tarefa:**\n\n{task_output.description}")
                        st.markdown(f"**Resultado:**\n\n{task_output.raw.strip()}")
                        st.divider()
                else:
                    st.error("A chave ou método 'tasks_output' não foi encontrado no resultado.")
            except Exception as e:
                st.error(f"Erro ao acessar os dados: {str(e)}")

            # (Opcional) Substituir com os outputs reais, se disponível
            coletor_resultado = "Resultado do Coletor"
            linguista_resultado = "Resultado do Linguista"
            verificador_resultado = "Resultado do Verificador"
            classificacao_resultado = "Resultado da Classificação"
            inserir_analise(noticia, coletor_resultado, linguista_resultado, verificador_resultado, classificacao_resultado)

            st.subheader("🔍 Análise Completa")
            st.markdown("""
            ### Agentes Individuais:

            **Agente Coletor**: Busca e apresenta notícias semelhantes.  
            **Agente Linguístico**: Avalia o tom, estilo e estrutura.  
            **Agente Verificador**: Confere os fatos com fontes confiáveis.  
            **Agente Classificador**: Classifica a confiabilidade da notícia.
            """)

with aba_historico:
    st.subheader("📚 Histórico de Análises")
    exibir_historico()
