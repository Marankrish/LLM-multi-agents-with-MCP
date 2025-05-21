from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from mcp.client.sse import sse_client
from mcp import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
import logging
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
logger = logging.getLogger(__name__)

query = input("Enter a query: ")


llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0.8)

async def main():
    async with sse_client("http://127.0.0.1:8001/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()

            tools = await load_mcp_tools(client)
            logger.info(f"Tools: {tools}")


            agent = create_react_agent(llm, tools)

            system_message = SystemMessage(content= (
                "You have access to multiple tools that can help answer queries. "
                "Use them dynamically and efficiently based on the user's request."
            ))

            result = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})
            logger.info(f"Raw result: {result}")

            if isinstance(result, dict) and 'messages' in result:
                return result['messages'][-1].content
            elif hasattr(result, 'content'):
                return result.content
            else:
                return str(result)

if __name__ == "__main__":
    response = asyncio.run(main())
    print(f"Result: {response}")

