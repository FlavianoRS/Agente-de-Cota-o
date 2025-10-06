# Agente de Cotação
### Objetivo
- Agente capaz de realizar a cotação de qualquer produto desejado;
- Deixar dinâmico e ágil a realização de cotações e Orçementos de produtos.
##
### Tecnologias Utilizadas
O projeto utiliza a biblioteca Lnagchaim para a estruturação do Agente organizando a tool o modelo utilizado e o prompt que rege suas ações.

Para a tool são utilizadas as bibliotecas Selenuim e 
Beatifulsoap para a estração dos dados das informações dos produtos em cada site.

Para o modelo o porojeto utiliza das possíveis abordagens a primeira sendo a utilização do modelo Gemini Flash 2.0 que é utilizado atravé da key do Google para isso é utilizado a biblioteca langchain_google_genai e a segunda abordagem que utiliza um modelo local sendo executados em Docker, para isso é utilizado a biblioteca langchain_openai e uma imagem base Ollma com um modelo em especíco, que nesse projeto é utilizado o modelo orieg/gemma3-tools:1b.
##
### Construção
#### Tool
Para a contrução da tool foram selecionados 3 sites específicos que são eles Amazon, Mercado Livre e Magazine Luiza. A tool recebe como parâmetro que se trata do produto, realiza a pesquisa nos três sites e retorna um markdown com as informações organizadas para o agente.

#### Agente
O gente é montado tendo como modelo na primeira opção o Gemini flas 2.0 rodando em api pelo Google AI Studio e na segunda opção o orieg/gemma3-tools:1b rodando localmente em Docker. Em cada opção há um prompt específico qpara que cada modelo posso entregar o seu melhor desempenho  deixando assim o projeto mais eficiente. Para que o agente possa ser utilizado cmo mais facilidade foi utilizado a biblioteca Streamlit como interface.

#### Arquivos Docker
Em cada projeto há os arquivos Dockerfile para que seja possível ser executado dentro de qualquer orquestrador docker, junto também há os arquvos requeriments.txt correspondentes para montar a imagens.