from langchain.tools import tool
from pydantic import BaseModel, Field

# Defina um schema para o modelo entender que ele deve passar um valor
class SearchInput(BaseModel):
    produto: str = Field(description="Nome do produto a ser buscado.")


def scraping_produtos(produto: str ) -> str:
    """
    This tool collects information about any produtcs from Mercado Livre, Amazon and Magazine Luiza.

    ---

    How it works:
    - To run is necessary pass name of product in summary form, don't pass words like cheap, economic and any other noun related to price, promotion, only fetures of products .
    - The tool performs **no analysis or filtering**, only raw data collection.
    - It returns a Markdown-formatted table. Each row in the table represents a product.

    ---

    The table includes the following columns:
    - **'Brand'**: The brand of the produtc.
    - **'Rating (score from 0 to 5)'**: The average user rating.
    - **'Description'**: A brief description of the product.
    - **'Price'**: The product current price.
    - **'Store'**: Website where the product is being sold.
    - **'Link'**: Link of webpage product.

    ---

    """
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import time
    
    #produto = 'notebook 8Gb RAM'
    print(produto)
    url_prod = produto.replace(' ','-').lower()
    url_pord2 = produto.replace(' ','+').lower()
    pgs = 6
    frame = pd.DataFrame(columns=['marca','avaliacao','descricao','preco','loja','link'])
    
    headers = {
            'User-Agent': 'Chrome/58.0.3029.110 '
    }
    
    # Fazendo a requisição para a página de produtos com o cabeçalho
    urls = ["https://lista.mercadolivre.com.br/","https://www.amazon.com.br/s?k=","https://www.magazinevoce.com.br/magazinemaiordescontao/busca/"]
    
    for url in urls:
            for i in range(4):
                    if 'mercadolivre' in url:
                            print(f"Entrou mercado livre {i+1}")
                            consulta = f'{url}{url_prod}_Desde_{49*i}_NoIndex_True'
                            response = requests.get(consulta, headers=headers)
                            html = response.text
    
                            # Criando o objeto Beautiful Soup
                            soup = BeautifulSoup(html, 'html.parser')
    
                            # Buscando todos os elementos que contêm os preços dos produtos
                            precos = soup.find_all(['div'], class_=['poly-card__content'])
    
                            # Extraindo e imprimindo os preços
                            for j in range(len(precos)):
                                    add_marca = '' if precos[j].find('span',class_='poly-component__brand') == None else precos[j].find('span',class_='poly-component__brand').text
                                    add_avaliacao = '' if precos[j].find('span',class_='andes-visually-hidden') == None else precos[j].find('span',class_='andes-visually-hidden').text
                                    add_descricao = '' if precos[j].find('h3',class_='poly-component__title-wrapper') == None else precos[j].find('h3',class_='poly-component__title-wrapper').text
                                    add_preco = '' if precos[j].find('span',class_='andes-money-amount andes-money-amount--cents-superscript') == None else precos[i].find('span',class_='andes-money-amount andes-money-amount--cents-superscript').text
                                    add_loja = 'Mercado Livre' 
                                    add_link = '' if precos[0].find('a',class_='poly-component__title')['href'] == None else precos[0].find('a',class_='poly-component__title')['href']
    
                                    nova_linha_produto = {'marca':add_marca,'avaliacao':add_avaliacao,'descricao':add_descricao,'preco':add_preco,'loja':add_loja,'link':add_link}
    
                                    frame.loc[len(frame)] = nova_linha_produto
                    if 'amazon.com' in url:
                            print(f"Entrou amazom {i+1}")
                            chorme_opt = Options()
                            chorme_opt.add_argument("--headless")
    
                            navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= chorme_opt)
                            url_get = f"{url}{url_pord2.lower()}&page={i+1}"
                            navegador.get(url_get)
    
                            soup = BeautifulSoup(navegador.page_source, 'html.parser')
                            prod_amazon = soup.find_all(['div'],class_=['sg-col-inner'])
    
                            for l in range(len(prod_amazon)):
                                if prod_amazon[l].find('h2',class_='a-size-base-plus a-spacing-none a-color-base a-text-normal') != None:
                                    if prod_amazon[l].find('span',class_='a-icon-alt') != None:
                                        if prod_amazon[l].find('span',class_='a-price-whole') != None:
                                            add_marca = ''    
                                            add_descricao = prod_amazon[l].find('h2',class_='a-size-base-plus a-spacing-none a-color-base a-text-normal').text
                                            add_avaliacao = prod_amazon[l].find('span',class_='a-icon-alt').text
                                            add_preco = 'R$'+prod_amazon[l].find('span',class_='a-price-whole').text
                                            add_loja = 'Amazon' 
                                            add_link = '' if prod_amazon[l].find('a')['href'] == None else 'https://www.amazon.com.br/'+prod_amazon[l].find('a')['href']
                                        else:
                                            add_marca = ''
                                            add_descricao = prod_amazon[l].find('h2',class_='a-size-base-plus a-spacing-none a-color-base a-text-normal').text
                                            add_avaliacao = prod_amazon[l].find('span',class_='a-icon-alt').text
                                            add_preco = "Sem preço"
                                            add_loja = 'Amazon' 
                                            add_link = '' if prod_amazon[l].find('a')['href'] == None else 'https://www.amazon.com.br/'+prod_amazon[l].find('a')['href'] 
                                    else:
                                        if prod_amazon[l].find('span',class_='a-price-whole') != None:
                                            add_marca = ''    
                                            add_descricao = prod_amazon[l].find('h2',class_='a-size-base-plus a-spacing-none a-color-base a-text-normal').text
                                            add_avaliacao = "Sem Avaliação "
                                            add_preco = 'R$'+prod_amazon[l].find('span',class_='a-price-whole').text
                                            add_loja = 'Amazon' 
                                            add_link = '' if prod_amazon[l].find('a')['href'] == None else 'https://www.amazon.com.br/'+prod_amazon[l].find('a')['href'] 
                                        else:
                                            add_marca = ''    
                                            add_descricao = prod_amazon[l].find('h2',class_='a-size-base-plus a-spacing-none a-color-base a-text-normal').text
                                            add_avaliacao = "Sem Avaliação" 
                                            add_preco = "Sem preço"
    
                                            add_loja = 'Amazon' 
                                            add_link = '' if prod_amazon[l].find('a')['href'] == None else 'https://www.amazon.com.br/'+prod_amazon[l].find('a')['href'] 
    
                                nova_linha_produto = {'marca':add_marca,'avaliacao':add_avaliacao,'descricao':add_descricao,'preco':add_preco,'loja':add_loja,'link':add_link}
                                frame.loc[len(frame)] = nova_linha_produto
                            navegador.quit()
                    if 'magazinevoce' in url:
                            print(f"Entrou magazine luiza {i+1}")
                            chorme_opt = Options()
                            chorme_opt.add_argument("--headless")
                            
                            navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= chorme_opt)
                            consulta = f'{url}{url_pord2.lower()}/?page={i+1}'
                            navegador.get(consulta)
    
                            soup = BeautifulSoup(navegador.page_source, 'html.parser')
                            card = soup.find_all('li',class_='sc-kaaGRQ kIiMKW')
    
                            for li in range(len(card)):
                                if card[li].find('h2',class_='sc-hsUFQk PdLos') != None:
                                    add_marca = '' 
                                    add_descricao = '' if card[li].find('h2',class_='sc-hsUFQk PdLos') == None else card[li].find('h2',class_="sc-hsUFQk PdLos").text
                                    add_avaliacao = '' if card[li].find('div',class_='sc-gtJxfw bqrMZi') == None else card[li].find('div',class_='sc-gtJxfw bqrMZi').text
                                    add_preco = '' if card[li].find('p',class_='sc-dcJsrY lmAmKF sc-cezyBN fATncB') == None else card[li].find('p',class_='sc-dcJsrY lmAmKF sc-cezyBN fATncB').text
                                    add_loja = 'Magazine Luiza' 
                                    add_link = '' if card[li].find('a',class_='sc-fHjqPf eXlKzg sc-iNIeMn cBHvjI sc-iNIeMn cBHvjI')== None else 'https://www.magazinevoce.com.br/'+card[li].find('a',class_='sc-fHjqPf eXlKzg sc-iNIeMn cBHvjI sc-iNIeMn cBHvjI')['href']
    
                                nova_linha_produto = {'marca':add_marca,'avaliacao':add_avaliacao,'descricao':add_descricao,'preco':add_preco,'loja':add_loja,'link':add_link}
                                frame.loc[len(frame)] = nova_linha_produto
    
                            navegador.quit()
    
    fr_mk = frame.to_markdown()
    return fr_mk

###################################
#  Agente                         #
###################################

# Seu código, mas com a abordagem ReAct
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.tools import Tool, StructuredTool
from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
import streamlit as st

model = "llama3.2:3b-instruct-q4_K_S" 
#model = "qwen3:4b-instruct" 
#model = "mistral:7b-instruct" # Funciona, só precisa melhoar o prompt
#model = "orieg/gemma3-tools:1b" # Funciona, só a resposta é gerada em inglês
#model = "MFDoom/deepseek-r1-tool-calling:7b"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # A chave pode ser qualquer coisa, 'ollama' é uma convenção
os.environ["OPENAI_MODEL_NAME"] = model

# Instancia o LLM. A classe ChatOpenAI já usará o Ollama por padrão
llm = ChatOpenAI(model=model, temperature=0.7)

scraping = StructuredTool.from_function(
                                        func=scraping_produtos,
                                        name='scraping_produtos', 
                                        description="""Realiza a buscas de preço, descrição, loja e link de qualquer produtos nos sites Mercado Livre, Amazon e Magazine Luiza""", 
                                        args_schema=SearchInput)
tools = [scraping]

#Prompt com a estrutura ReAct
prompt = ChatPromptTemplate.from_messages([
   ("system","""Você é um agentes especialista em cotação que anlisa a melhor relação entre preço e avaliação dos pordutos e busca sempre os produtos mais em conta, 
                sempre traga a opção que tive ro melhor preço e que a descrição seja o que foi solicitado siga a seguinte cadeia de relevância para a sua análise descrição, preço e avaliação. Para que o usuário possa
                melhor compreender o melhor produto traga sempre os 3 melhores produtos e os informe em um rankin"""),
   ("system", "A ferramenta de busca retorna todos os dados necessários em uma única consulta. **Não faça múltiplas consultas ou tente refinar a busca com termos adicionais.**, analise apenas a resposta da função em sua primeira execução"),
    ("system", """Após utilizar a ferramenta para coletar a tabela de dados, você deve:
        1. Leia com extrema atenção a string que a ferramenta retorna, pois todos os dados necessários estão contidos nessa string, a string está no formato de Markdown e seu conteúdo está organizado em uma tabela, leia essa string tendo essa formatação em mente.
        2. Analisar as informações de preço, avaliação e descrição de cada produto.
        3. Comparar os produtos entre si para identificar a que oferece a melhor combinação de preço baixo e avaliação alta, com base em um bom número de avaliações (indicando que a avaliação é confiável).
        4. Apresentar uma recomendação clara e justificada, explicando por que aquele produto é a melhor escolha.
        5. Não utilizar a ferramenta novamente, o uso da ferramenta é único e vee acontecer apenas uma única vez.
        
        **IMPORTANTE: A ferramenta 'scraping_produtos' aceita apenas 1 parâmetro. Apenas chame a ferramenta com no máximo argumento, pois ela foi construida para receber 1 parâmtro**
        **IMPORTANTE: Analiise a descrição dos produtos retornados pela tool pra que seja avaliadao apenas os produtos que possuem relação com o que foi pedido para a cotação**
        """),
    ("system", """
        Para que a resposta final seja clara, siga rigorosamente o formato abaixo. Use Markdown para estruturar a resposta.

        ---

        ### Recomendação
        [Nome e modelo do produto recomendada]

        ### Motivação da Escolha
        [Explique, em um parágrafo, por que esse produto oferece o melhor custo-benefício. Mencione como o preço se relaciona com a avaliação e o número de reviews.]

        ### Resumo dos Dados
        -**Descrição:** [Descrição do produto]
        - **Avaliação:** [Avaliação (ex: 4.8/5)]
        - **Loja:** [Loja do produto]
        - **Preço:** [Preço do produto]
        -**Link:** [Link do produto presente na tabela dentro do arquivo retornado pela tool]

        ---
        """),
    ("system", "No more tools available"),
    ("placeholder","{agent_scratchpad}"),
    ("placeholder","{tool_code}"),
    ("human","{input}"),  
])

agente = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agente, tools=tools, verbose=False)

st.set_page_config(page_title="Agente de Cotação de Produtos", layout="wide")
st.title("🛍️ Agente de Cotação de Produtos")
st.markdown("Bem-vindo! Eu sou um agente especialista em encontrar o melhor custo-benefício para você. Basta me dizer o que você quer cotar!")
user_input = st.text_input("Digite o produto que deseja cotar ", key="user_input")

resposta = executor.invoke({"input":user_input})
print(resposta["output"])