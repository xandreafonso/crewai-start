from rich.console import Console
from rich.markdown import Markdown
from crewai_tools import FirecrawlScrapeWebsiteTool
from firecrawl import FirecrawlApp
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Optional, Any, Type, Dict

app = FirecrawlApp()

class InnerFirecrawlScrapeWebsiteToolSchema(BaseModel):
    url: str = Field(description="Website URL")

class InnerFirecrawlScrapeWebsiteTool(BaseTool):
    name: str = "Firecrawl web scrape tool"
    description: str = "Scrape webpages url using Firecrawl and return the contents."
    args_schema: Type[BaseModel] = InnerFirecrawlScrapeWebsiteToolSchema

    def _run(self, url: str) -> str:
        scrape_status = app.scrape_url(url,
                            params={'formats': ['markdown'], 'onlyMainContent': False} # Esse foi o motivo de eu ter feito essa tool. A versão original está com erros. Ela está enviando chaves inexistentes nesse dicionário de parametros da requisição para o Firecrawl.
                        )
        return scrape_status









#url = "https://alexandreafonso.com.br/curso-headlines"
# app = FirecrawlApp()
# scrape_status = app.scrape_url(
#   url, 
#   params={'formats': ['markdown'], 'onlyMainContent': False}
# )
# # print(scrape_status)
# console = Console()
# console.print(Markdown(scrape_status['markdown']))

# tool_web_page_scrape = FirecrawlScrapeWebsiteTool()
# result = tool_web_page_scrape.run(url)
# print(result)