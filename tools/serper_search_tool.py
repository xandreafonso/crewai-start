from rich.console import Console
from rich.markdown import Markdown
from crewai_tools import FirecrawlScrapeWebsiteTool
from firecrawl import FirecrawlApp
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Optional, Any, Type, Dict
import datetime
import os
import json
import requests

class InnerSerperDevToolSchema(BaseModel):
	"""Input for SerperDevTool."""
	search_query: str = Field(..., description="Mandatory search query you want to use to search the internet")


class InnerSerperDevTool(BaseTool):
    name: str = "Search the internet"
    description: str = "A tool that can be used to search the internet with a search_query."
    args_schema: Type[BaseModel] = InnerSerperDevToolSchema
    search_url: str = "https://google.serper.dev/search"
    country: Optional[str] = ''
    location: Optional[str] = 'Brazil' # esse foi o motivo de eu ter customizado essa tool. A pesquisa feita em inglês por padrão.
    locale: Optional[str] = 'pr-br' # esse foi o motivo de eu ter customizado essa tool. A pesquisa feita em inglês por padrão.
    n_results: int = 10
    save_file: bool = False

    def _run(
		self,
		**kwargs: Any,
	) -> Any:

        search_query = kwargs.get('search_query') or kwargs.get('query')
        save_file = kwargs.get('save_file', self.save_file)
        n_results = kwargs.get('n_results', self.n_results)

        payload = { "q": search_query, "num": n_results }

        if self.country != '':
            payload["gl"] = self.country
        if self.location != '':
            payload["location"] = self.location
        if self.locale != '':
            payload["hl"] = self.locale

        payload = json.dumps(payload)

        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
		}

        response = requests.request("POST", self.search_url, headers=headers, data=payload)
        results = response.json()

        if 'organic' in results:
            results = results['organic'][:self.n_results]
            string = []
            for result in results:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "---"
                    ]))
                except KeyError:
                    continue

            content = '\n'.join(string)
            if save_file:
                _save_results_to_file(content)
            return f"\nSearch results: {content}\n"
        else:
            return results

def _save_results_to_file(content: str) -> None:
    """Saves the search results to a file."""
    filename = f"search_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Results saved to {filename}")




















# https://serper.dev/playground
# https://github.com/crewAIInc/crewAI-examples/blob/main/instagram_post/tools/search_tools.py

# import json
# import os

# import requests
# from langchain.tools import tool

# class SearchTools():

#   @tool("Search internet")
#   def search_internet(query):
#     """Useful to search the internet about a given topic and return relevant
#     results."""
#     return SearchTools.search(query)

#   @tool("Search instagram")
#   def search_instagram(query):
#     """Useful to search for instagram post about a given topic and return relevant
#     results."""
#     query = f"site:instagram.com {query}"
#     return SearchTools.search(query)

#   def search(query, n_results=5):
#     url = "https://google.serper.dev/search"
#     payload = json.dumps({"q": query})
#     headers = {
#         'X-API-KEY': os.environ['SERPER_API_KEY'],
#         'content-type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     results = response.json()['organic']
#     stirng = []
#     for result in results[:n_results]:
#       try:
#         stirng.append('\n'.join([
#             f"Title: {result['title']}", f"Link: {result['link']}",
#             f"Snippet: {result['snippet']}", "\n-----------------"
#         ]))
#       except KeyError:
#         next

#     content = '\n'.join(stirng)
#     return f"\nSearch result: {content}\n"
