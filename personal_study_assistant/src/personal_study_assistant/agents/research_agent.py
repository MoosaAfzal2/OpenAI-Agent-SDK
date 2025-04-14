from agents import Agent
from agents.model_settings import ModelSettings

from personal_study_assistant.tools.tavily_search_tool import tavily_search_tool
from personal_study_assistant.config import model
from personal_study_assistant.agents.summarizer_agent import summarizer_agent
from personal_study_assistant.guardrails.research_agent_guardrails import (
    relevance_and_conciseness_guardrail,
)

INSTRUCTIONS = (
    "You are a highly capable research assistant. When given a study topic, "
    "conduct a brief web search and summarize the most relevant and recent findings "
    "in 2–3 clear paragraphs (under 300 words total). Focus on capturing key insights, "
    "core concepts, and recent developments, omitting all filler, commentary, or personal opinions. "
    "Assume the user needs quick and accurate synthesis for academic or professional use. "
    "Do not ask for clarification; if details are vague, infer reasonable defaults "
    "(e.g., beginner-level overview, one-week timeline, broad scope). Use clear, objective, and "
    "informative language throughout."
)

research_agent = Agent(
    name="Researcher Agent",
    instructions=INSTRUCTIONS,
    model=model,
    tools=[tavily_search_tool],
    model_settings=ModelSettings(tool_choice="required"),
    handoffs=[summarizer_agent],
    output_guardrails=[relevance_and_conciseness_guardrail],
)
