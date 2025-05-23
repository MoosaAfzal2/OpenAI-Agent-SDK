import asyncio

from agents import (
    Agent,
    ItemHelpers,
    MessageOutputItem,
    ToolCallOutputItem,
    ToolCallItem,
    Runner,
    trace,
)
from config import model

"""
In the orchestrator-workers pattern, a central LLM dynamically breaks down tasks, 
delegates them to worker LLMs, and synthesizes their results.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
    model=model,
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
    model=model,
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
    model=model,
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    model=model,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
    model=model,
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, ToolCallItem):
                print(f"- {item.agent.name} - Tool call: {item.to_input_item()}")
            if isinstance(item, ToolCallOutputItem):
                print(f"- {item.agent.name} - Tool call output: {item.to_input_item()}")
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"- {item.agent.name} - Translation step:\n{text}")

        orchestrator_result_list = orchestrator_result.to_input_list()
        orchestrator_result_list.append(
            {
                "role": "user",
                "content": "Pick Any 2 translations",
            }
        )

        synthesizer_result = await Runner.run(
            synthesizer_agent,
            orchestrator_result_list,
        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
