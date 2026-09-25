![Banner do Dash Analyzer](assets/logo.svg)
<div align="center">
  <br><br>
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=32&pause=1000&color=F7931E&center=true&vCenter=true&width=600&lines=An%C3%A1lise+de+dados+com+IA;Gr%C3%A1ficos+e+pain%C3%A9is+interativos" alt="Dash Analyzer">
  </a>

  <p>
    Uma aplicação web para analisar arquivos de dados, criar gráficos e responder perguntas sobre as informações enviadas.
    Ela combina Python, Pandas, Plotly e a API da Groq com o modelo <b>GPT-OSS-20B</b>.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-orange?style=for-the-badge" alt="Status">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-Aplica%C3%A7%C3%A3o%20web-lightgrey?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/Plotly-Gr%C3%A1ficos%20interativos-blueviolet?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
    <img src="https://img.shields.io/badge/Groq-GPT--OSS--20B-black?style=for-the-badge" alt="Groq e GPT-OSS-20B">
  </p>
</div>

## Sobre o projeto

O Dash Analyzer ajuda a entender conjuntos de dados sem precisar montar cada gráfico ou resumo manualmente. Basta enviar um arquivo CSV para receber uma visão geral dos dados, gráficos interativos e uma área de chat para fazer perguntas.

A inteligência artificial usa os resumos criados pela aplicação para sugerir análises e visualizações com base nas colunas que realmente existem no arquivo. Assim, o resultado é mais útil e confiável.

<!--
<div align="center">
  <img src="./assets/demo.gif" alt="Demonstração da aplicação em funcionamento" width="85%">
  <br>
  <sub><i>Demonstração da aplicação em funcionamento</i></sub>
</div> -->

## Tecnologias usadas

| Área | Tecnologia | Para que serve |
| --- | --- | --- |
| Processamento | Python, Flask e Pandas | Ler os dados e organizar a aplicação |
| Gráficos | Plotly | Criar gráficos dinâmicos e fáceis de explorar |
| Inteligência artificial | Groq API + GPT-OSS-20B | Gerar sugestões e respostas sobre os dados |
| Interface | HTML, CSS e JavaScript | Exibir uma experiência moderna e simples de usar |

## O que a aplicação faz

- Envia e prepara arquivos CSV para análise.
- Cria um resumo automático com informações importantes, como tipos de coluna, valores vazios e medidas numéricas.
- Garante que as sugestões usem apenas as colunas presentes no arquivo enviado.
- Gera gráficos automaticamente, como histogramas para números e gráficos de barras para categorias.
- Permite conversar com a aplicação e tirar dúvidas sobre os dados carregados.

## Próximos passos

- Gerar DashBoard final, para download, PowerBI.
- Aceitar arquivos Excel (`.xlsx` e `.xls`) além de CSV.
- Melhorar o tratamento de arquivos muito grandes para manter a análise rápida e estável.

## Como instalar e executar

### 1. Baixe o projeto

```bash
git clone https://github.com/teu-utilizador/dash-analyzer.git
cd dash-analyzer
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione a chave da Groq

Crie um arquivo chamado `.env` na pasta principal do projeto e inclua sua chave:

```env
GROQ_API_KEY=sua_chave_aqui
```

> Não compartilhe esse arquivo nem publique a sua chave no GitHub.

### 5. Inicie a aplicação

```bash
python main.py
```

Depois, abra [http://127.0.0.1:5000](http://127.0.0.1:5000) no navegador.

## Como usar

1. Abra a página inicial e envie um arquivo CSV.
2. Veja o resumo criado automaticamente.
3. Explore os gráficos interativos.
4. Use o chat para fazer perguntas específicas sobre o conteúdo do arquivo.

## Autor

Desenvolvido por Guilherme Araújo Fernandes como parte de estudos e projetos em inteligência artificial e desenvolvimento de software.

<div align="center">
  <sub>⭐ Se este projeto ajudou você, considere deixar uma estrela no repositório.</sub>
</div>
