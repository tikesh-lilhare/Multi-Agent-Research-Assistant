from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_Key"))    

@tool
def web_search(query:str) -> str:
    """
    Search The Web For Recent And Reliable Information On a Topic. Returns Titles , URLs and Snippets. 
    """

    results = tavily_client.search(query=query, max_results=5)
    out=[]
    for r in results['results']:
        out.append(
        f"Title : {r['title']}\n URl:{r['url']}\nSnippet:{r['content'][:300]}\n" 
    )
    return "\n--\n".join(out)



@tool
def scrape_url(url : str) -> str:
    """Scrape And Return Clean Text From A Given URL For Deeper Reading."""
    try:
        resp = requests.get(url , timeout=8 , headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup (["script", "style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator="\n",strip=True)[:3000]
    except Exception as e:
        return f"Could Not Scrape URL :{str(e)}" 
