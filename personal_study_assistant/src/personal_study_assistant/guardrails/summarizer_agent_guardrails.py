from pydantic import BaseModel
from personal_study_assistant.config import model, config
from personal_study_assistant.context import Context


from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    output_guardrail,
)


class SummarizerOutput(BaseModel):
    word_count: int


# Define new agent for summarizer word count check
word_count_agent = Agent(
    name="Summarizer Word Count Check",
    instructions=(
        "Analyze the provided summary to ensure it adheres to the word count limit specified in the user query. "
        "Verify that the summary is concise and does not exceed the allowed word count."
    ),
    model=model,
    output_type=SummarizerOutput,
)


# Define guardrail for summarizer word count check
@output_guardrail
async def summarizer_word_count_guardrail(
    ctx: RunContextWrapper[Context],
    agent: Agent,
    output: str,
) -> GuardrailFunctionOutput:
    # Extract the word count limit from the context
    word_limit = ctx.context.word_limit
    if word_limit is None:
        return GuardrailFunctionOutput(
            output_info=output,
            tripwire_triggered=False,
        )

    # Run the summarizer agent on the output response
    result = await Runner.run(
        starting_agent=word_count_agent,
        input=f"Check the word count of the following summary (max {word_limit} words): {output}",
        run_config=config,
    )

    # Check if the word count exceeds the defined limit
    tripwire_triggered = result.final_output.word_count > word_limit

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=tripwire_triggered,
    )
