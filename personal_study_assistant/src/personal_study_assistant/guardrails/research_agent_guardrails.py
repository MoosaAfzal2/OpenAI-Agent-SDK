from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
from personal_study_assistant.config import model, config


class RelevanceOutput(BaseModel):
    is_relevant: bool
    word_count: int
    academic_sources: bool


# Define new agent for relevance and conciseness check
relevance_agent = Agent(
    name="Relevance and Conciseness Check",
    instructions=(
        "Analyze the provided response to ensure it is concise and relevant to academic research. "
        "Verify that the content is derived from academic sources, is not overly verbose, "
        "and aligns with the context of the query."
    ),
    model=model,
    output_type=RelevanceOutput,
)


# Define guardrail for relevance and conciseness check
@output_guardrail
async def relevance_and_conciseness_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str,
) -> GuardrailFunctionOutput:
    """
    Guardrail to check the relevance and conciseness of the output from the research agent.
    If the content is not relevant, too verbose, or lacks academic sources, trigger the guardrail.
    """
    # Run the relevance check agent on the output response
    result = await Runner.run(
        relevance_agent,
        output,
        context=ctx.context,
        run_config=config,
    )

    # Check for the tripwires based on the conditions defined
    tripwire_triggered = (
        not result.final_output.is_relevant  # If the content is not relevant
        or result.final_output.word_count > 100  # If the word count is more than 100
        or not result.final_output.academic_sources  # If the sources are not academic
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=tripwire_triggered,
    )
