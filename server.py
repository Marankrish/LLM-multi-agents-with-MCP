from mcp.server.fastmcp import FastMCP
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(
    name = "various_tools",
    host = "127.0.0.1",
    port = "8001",
    log_level = "INFO")

@mcp.tool()
def Internet_tool(query:str) -> str:
    """Input for the Tavily Tool"""
    wrapper = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(
        name="Internet-Tool",
        api_wrapper=wrapper
    )
    return tavily_tool.run({"query": query})

@mcp.tool()
def get_weather(query:str) -> str:
    """Input for the Weather Tool"""
    wrapper = OpenWeatherMapAPIWrapper()
    weather_data = wrapper.run(query)
    return weather_data

@mcp.tool()
def wikipedia_tool(query:str) -> str:
    """Inputs to the Wikipedia tool"""
    wrapper = WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=2000)
    tool = WikipediaQueryRun(
        name="Wiki-Input",
        api_wrapper=wrapper
    )
    return tool.run({"query": query})

if __name__ == "__main__":
    mcp.run(transport = "sse")
