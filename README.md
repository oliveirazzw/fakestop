
# 🤖 Verificador de Notícias com IA - Projeto em Python + Streamlit + CrewAI

Este projeto utiliza **inteligência artificial com múltiplos agentes** para verificar notícias automaticamente e classificá-las como **Confiável, Dúbia ou Falsa**, com base em análise linguística, checagem de fatos e comparação com notícias semelhantes.

---

## 🚀 O que este projeto faz?

🔍 Ao colar uma notícia no sistema, ele:

- Busca **notícias semelhantes** para comparar
- Analisa o **tom, estilo e estrutura da linguagem**
- Faz a **checagem dos fatos**
- Classifica a notícia como **confiável, dúbia ou falsa**
- Salva tudo em um **banco de dados** para consultas futuras

---

## 🧰 Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [OpenAI API (GPT-4o-mini)](https://platform.openai.com/)
- [SQLite](https://www.sqlite.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚙️ Como executar o projeto localmente

### 1. Clone este repositório

```bash
git clone https://github.com/oliveirazzw/fakestop.git
cd nome-do-repositorio
```

### 2.🐍 Crie e ative o ambiente virtual

### Para Windows (CMD):

1- python -m venv venv

2- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

3- venv\Scripts\activate


### Para PowerShell:

1- python -m venv venv

2- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

3- .\venv\Scripts\Activate.ps1

### Para Linux/MacOS:

1- python3 -m venv venv

2- source venv/bin/activate


### 3. Instale as dependências

```bash
pip install -r requirements.txt
```   

> Caso não tenha o arquivo `requirements.txt`, use:
```bash
pip install streamlit crewai python-dotenv
```

### 4. Configure sua chave da OpenAI

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```
OPENAI_API_KEY=sua-chave-aqui
```

> 🔑 Você pode obter sua chave em: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

### 5. Execute o sistema

```bash
streamlit run fakestop_app.py
```

---

## 🖥️ Como usar o sistema no navegador

1. **Cole uma notícia** no campo de texto.
2. Clique em **"Verificar"**.
3. A IA:
   - Busca outras notícias semelhantes
   - Analisa o texto da notícia
   - Verifica os fatos
   - Classifica o conteúdo
4. Você verá os resultados na tela e poderá consultar o histórico de verificações.

---

## 🧠 Agentes Inteligentes envolvidos

- 🕵️‍♂️ **Agente Coletor**: Busca notícias similares à fornecida.
- 📝 **Agente Linguista**: Analisa estilo, tom e estrutura do texto.
- 🧾 **Agente Verificador**: Checa os fatos com fontes confiáveis.
- 🧑‍⚖️ **Agente Classificador**: Dá o veredito final da notícia.

---

## 💾 Histórico de Análises

As análises são salvas automaticamente em um banco de dados local `analises.db` usando SQLite.

Você pode consultar os dados direto pela interface gráfica ou por ferramentas como [DB Browser for SQLite](https://sqlitebrowser.org/).

---

## 📌 Dicas

- Execute localmente para evitar custos com nuvem.
- Personalize os agentes para diferentes domínios (política, saúde, etc.).
- Funciona com qualquer modelo OpenAI, mas o ideal é usar o **GPT-4o-mini** ou superior.

---

## 🧑‍💻 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para enviar PRs, abrir issues ou adaptar para seu próprio uso.

---

## 📞 Contato

Caso tenha dúvidas, sugestões ou deseje contribuir com ideias:

📧 seu-email@exemplo.com  
🐙 GitHub: [oliveirazzw](https://github.com/oliveirazzw)

---
