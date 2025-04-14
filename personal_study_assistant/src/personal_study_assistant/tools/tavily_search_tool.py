import os
from dotenv import load_dotenv
from agents import function_tool
from tavily import TavilyClient  # type: ignore

# Load the environment variables from the .env file
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the Tavily client
client = TavilyClient(api_key=TAVILY_API_KEY)


@function_tool
def tavily_search_tool(
    query: str,
    include_images: bool = False,
    search_depth: str = "basic",
    max_results: int = 1,
    days: int = 3,
) -> dict:
    """
    Calls the Tavily Search API using the official SDK to fetch market news based on the query.
    Returns:
        dict: Contains both a formatted summary and the raw JSON response.
    """
    try:
        response = client.search(
            query=query,
            topic="general",
            search_depth=search_depth,
            max_results=max_results,
            time_range=None,
            days=days,
            include_answer=True,
            include_raw_content=False,
            include_images=include_images,
            include_image_descriptions=False,
            include_domains=[],
            exclude_domains=[],
        )
        # Build a formatted summary.
        summary = ""
        results = response.get("results", [])
        if results:
            for res in results:
                title = res.get("title", "No Title")
                content = res.get("content", "No Content")
                summary += f"Title: {title}\nContent: {content}\n\n"
        else:
            summary = "No text results found.\n"
        if include_images:
            images = response.get("images", [])
            if images:
                summary += "Image Results:\n"
                for image in images:
                    summary += f"{image}\n"
            else:
                summary += "No image results found.\n"
        return {"formatted_summary": summary, "raw_response": response}
    except Exception as e:
        return {"error": str(e)}
