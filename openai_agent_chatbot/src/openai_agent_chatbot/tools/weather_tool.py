from typing_extensions import TypedDict, Any
from agents import function_tool
import requests


class FetchWeatherToolInput(TypedDict):
    city: str


@function_tool
async def fetch_weather_tool(tool_input: FetchWeatherToolInput) -> str:
    try:
        base_url = f"https://wttr.in/{tool_input['city']}?format=%t+%C"
        response = requests.get(base_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        weather_info = response.text.strip()
        return f"Current weather in {tool_input['city']}: {weather_info}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather for {tool_input['city']}: {e}"
