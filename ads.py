from dotenv import load_dotenv

load_dotenv()

from datetime import datetime
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FirecrawlScrapeWebsiteTool
from tools.firecrawl_scrape_tool import InnerFirecrawlScrapeWebsiteTool
from tools.serper_search_tool import InnerSerperDevTool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

tool_web_page_scrape = InnerFirecrawlScrapeWebsiteTool()

agent_copywriter = Agent(
    llm=llm,
    role='Copywriter',
    verbose=True,
    memory=True,
    allow_delegation=False,
    goal='Escrever copys para anúncios em vídeo de acordo com o brienfing passado.',
    backstory="""
        Você é um copywriter muito experiênte, criativo e profundo conhecedor da lógica clássica.
        Você cria copys que servem de roteiros para anúncios no facebook ads.  

        Você nunca começa uma copy falando do produto. Você fala dele apenas no final da copy.
        Você sempre começa uma copy falando uma coisa pouco (ou nada) óbvia para o público-alvo.

        Você sempre escolhe um único argumento para a copy. Apenas um argumento é suficiente.
        Escolher um único argumento te ajuda a manter uma coesão na copy.
        Ao longo da copy, você vai conduzindo esse argumento na mente do leitor/ouvinte.
        Seu primeiro objetivo é fazer o leitor entender seu argumento.
        Você cria o argumento para fazer com que a pessoa concorde com você antes de falar do produto/serviço.
        Apenas no final, após o leitor/ouvinte entender seu argumento, você fala sobre o produto/serviço.

        Você é muito bom em criar copys que antecipam objeções para que elas não passem pela mente do leitor/ouvinte.

        Antes de falar do produto/serviço, você precisa deixa claro o que o leitor/ouvinte vai ganhar ou perder.
        Você não é dramático a menos que esteja falando de um assunto muito sério.
        O leitor/ouvinte precisa saber das consequências/benefícios antes de descobrir de que produto/serviço se trata.
        
        Você consegue envolver o leitor/ouvinte na copy.
        Sua copy se parece muito com uma conversa "cara a cara".
        Você usa frases curtas e um tom informal de conversa.
        Às vezes, você faz perguntas retoricas para reforçar a ideia de que a copy é uma conversa.
        Para aumentar o engajamento, você usa palavras que evocam a imaginação do leitor/ouvinte.
        Você nunca escreve uma copy sem garantir que vai usar, pelo menos, uma figura de linguagem que crie uma imagem na mente do leitor.
        As frases curtas que você usa também ajudam na clareza da copy.
        Nas suas frases curtas, você usa um tom informal.

        Você gosta de saltar linhas a cada frase escrita.

        Você nunca inventa uma informação!

        Ao falar do autor, você usa 1ª pessoa. Escreve como se fosse o mesmo.
        Você escreve as copys em nome do autor/criador do produto/serviço.
    """
)

agent_analista = Agent(
    # llm=llm,
    role='Analista de Marketing',
    verbose=True,
    memory=True,
    allow_delegation=False,
    goal='Levantar informações do produto/serviço para o copywriter escrever as copys.',
    backstory="""
        Você é um analista de marketing muito experiente e competente.
        Você é excepcional em organizar informações.
    """
)

task_organizar_informacoes_produto = Task(
    agent=agent_analista,
    tools=[tool_web_page_scrape],
    description="""
        Levantar informações do produto/serviço presentes na página {url}.
    """,
    expected_output="""
        Um briefing organizado com as informações que vou descrever a seguir.

        - Nome do produto
        - Descrição do produto
        - Público-alvo do produto
        - Argumento principal de vendas
        - Problemas que o produto resolve
        - Benefícios do produto
        - Detalhamento da metodologia, funcionamento ou mecanismo do produto
        - Garantia
        - Preço

        Não quero comentários inúteis que não vão agregar como informação do produto.

        Exemplo de como deve ser o documento final em markdown:

        # Informações para criação das copys

        ## Nome do Produto Aqui

        Aqui uma descrição do produto.

        ## Autor do produto

        Nome da empresa/pessoa criadora do produto. Se houverem detalhes interessantes sobre o criador do produto, adicione também.

        ## Público-alvo

        Uma descrição do público.

        ## Argumento principal

        Aqui coloque o argumento principal de vendas.

        ## Problemas que o produto resolve

        - Problema 1
        - Problema 2
        - Problema N

        ## Benefícios do produto

        - Benefício 1
        - Benefício 2
        - Benefício N

        ## Metodologia

        Explicação sobre a metodologia, funcionamento ou mecanismo do produto. Coloque todos os detalhes que encontrar sobre isso.

        ## Preço e formas de pagamento

        Coloque aqui o preço e formas de pagamento.

        ## Garantia

        Explicação sobre a garantia.
    """
)

task_criar_anuncios = Task(
    agent=agent_copywriter,
    context=[task_organizar_informacoes_produto],
    description="""
        Criar 5 copys de anúncios em vídeos para o facebook ads de acordo com as informações do produto.
        As copys devem ter mais de 150 palavras. Pelo menos 1 anúncio precisa ter mais de 200 palavras.
        O CTA é para clicar em "saiba mais".
    """,
    expected_output="""
        Espero um documento markdown organizado com as copys do que será dito no vídeo do anúncio.
        Não quero nada de emojis ou sugestões de cenários de gravação.
        Os anúncios não precisam de títulos.
        Caso você precise criar mais de 1 anúncio, quero que adicione, acima de cada um, a numeração. Ex: Anúncio 1, Anúncio 2, Anúncio 3.
    """,
)

crew = Crew(
    agents=[agent_analista, agent_copywriter],
    tasks=[task_organizar_informacoes_produto, task_criar_anuncios],
    process=Process.sequential,
    verbose=True
)

def write_briefing():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"tmp/{timestamp}_briefing.md"
    with open(filename, 'w') as f:
        f.write(task_organizar_informacoes_produto.output.raw)

def write_anuncios():    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"tmp/{timestamp}_anuncios.md"
    with open(filename, 'w') as f:
        f.write(task_criar_anuncios.output.raw)


url = "https://promovaweb.com/"
url = "https://victorelius.com.br/prolegomenos-academia-de-logica-correcao-seo/"
url = "https://educaverbum.com.br/pagina-de-assinatura/"
url = "https://rafaelcenson.com/"
url = "https://matemateca.com/"
url = "https://raquelcamposdemedeiros.com.br/"
url = "https://laboratoriodocriador.luizguilhermepro.com.br/"
url = "https://codigoviral.com.br/vejaovideo/"
url = "https://alexandreafonso.com.br/curso-headlines"
url = "https://temciencia.com.br/"

result = crew.kickoff(inputs={'url': url})
print(result)

write_briefing()
write_anuncios()


