from crewai_tools import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()

tool = ScrapeWebsiteTool(website_url='https://alexandreafonso.com.br/curso-headlines')

text = tool.run()
print(text)