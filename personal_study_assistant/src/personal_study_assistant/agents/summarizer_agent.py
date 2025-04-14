from agents import Agent
from personal_study_assistant.config import model
from personal_study_assistant.guardrails.summarizer_agent_guardrails import summarizer_word_count_guardrail
from personal_study_assistant.context import Context

INSTRUCTIONS = (
    "You are an expert summarizer. Given a research query and supporting findings, "
    "generate a short 2–3 sentence summary that captures the essence of the research. "
    "Then, provide a concise, markdown-formatted report organized into sections such as "
    "“Overview,” “Key Points,” and “Implications.” Conclude with a list of thoughtful follow-up questions "
    "that encourage deeper exploration. Do not request clarification — "
    "infer the topic’s scope and depth based on the provided material. "
    "Ensure the output is brief, highly readable, and well-structured for quick comprehension."
)


summarizer_agent = Agent[Context](
    name="Summarizer Agent",
    instructions=INSTRUCTIONS,
    model=model,
    output_guardrails=[summarizer_word_count_guardrail]
)
