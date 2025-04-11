import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ItemHelpers
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

from openai_agent_chatbot.tools.weather_tool import fetch_weather_tool

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemeni_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )


@cl.on_chat_start
async def start():
    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model=gemeni_model,
        openai_client=external_client,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
        tools=[fetch_weather_tool],
    )
    cl.user_session.set("agent", agent)

    await cl.Message(
        content="Welcome to the OpenAI Agent SDK Chatbot! How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=history,
            run_config=config,
        )

        response_content = ""

        async for event in result.stream_events():
            if event.type == "run_item_stream_event":
                # When items are generated, print them
                if event.item.type == "tool_call_item":
                    async with cl.Step(
                        name=cast(
                            str, getattr(event.item.raw_item, "name", "Unknown Tool")
                        ),
                        type="tool",
                    ) as step:
                        if hasattr(event.item.raw_item, "arguments"):
                            step.input = event.item.raw_item.arguments
                        else:
                            step.input = "No arguments available for this tool call."
                elif event.item.type == "tool_call_output_item":
                    step.output = event.item.output
                    await step.update()
                else:
                    pass  # Ignore other event types

            elif event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                response_content += event.data.delta

                # Update the thinking message with the actual response
                msg.content = response_content
                await msg.update()

        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
