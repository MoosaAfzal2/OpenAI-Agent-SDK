from typing import cast
import chainlit as cl
from chainlit.cli import run_chainlit
from openai.types.responses import ResponseTextDeltaEvent

from personal_study_assistant.manager import PersonalStudyAssistant
from personal_study_assistant.context import Context
from personal_study_assistant.config import model, config


@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    cl.user_session.set("model", model)

    context = Context()

    personal_study_assistant = PersonalStudyAssistant(
        model=model,
        config=config,
        context=context,
    )

    cl.user_session.set("assistant", personal_study_assistant)

    await cl.Message(
        content="Welcome to the Personal Study Assistant! How can I help you today?"
    ).send()


@cl.on_message
async def run_assistant(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    assistant: PersonalStudyAssistant = cast(
        PersonalStudyAssistant, cl.user_session.get("assistant")
    )

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    final_response = ""

    try:
        result = await assistant.run_streamed(query=history)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                final_response += event.data.delta
                msg.content = final_response
                await msg.update()

        history.append({"role": "assistant", "content": final_response})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")


def main():
    run_chainlit(__file__)


if __name__ == "__main__":
    main()
