import asyncio
import uuid

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace
from config import model

"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model=model,
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
    model=model,
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model=model,
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
    model=model,
)


async def main():
    # We'll create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    print(f"Conversation ID: {conversation_id}")
    print("Hi! We speak French, Spanish, and English. How can I help?")
    msg = input("> ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    while True:
        print(f"\n[INFO] Sending input to agent '{agent.name}': {inputs[-1]['content']}")
        # Each conversation turn is a single trace. Normally, each input from the user would be an
        # API request to your app, and you can wrap the request in a trace()
        with trace("Routing example", group_id=conversation_id):
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            print(f"[INFO] Receiving response from agent '{agent.name}':")
            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n[INFO] Response part done.")

        inputs = result.to_input_list()

        user_msg = input("Enter a message (type 'exit' to quit): ")
        if user_msg.lower() == "exit":
            print("[INFO] Exiting conversation.")
            break
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent
        print(f"[INFO] Switching to agent: {agent.name}")


if __name__ == "__main__":
    asyncio.run(main())