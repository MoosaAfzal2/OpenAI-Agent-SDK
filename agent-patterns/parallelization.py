import asyncio

from agents import Agent, ItemHelpers, Runner, trace
from config import model

"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=model,
)

translation_picker = Agent(
    name="translation_picker",
    instructions="You pick the best Spanish translation from the given options.",
    model=model,
)


async def main():
    print("Hi! Enter a message, and we'll translate it to Spanish.")
    msg = input("> ")

    # Ensure the entire workflow is a single trace
    with trace("Parallel translation"):
        print("\nStarting parallel translation...")
        res_1, res_2, res_3 = await asyncio.gather(
            Runner.run(
                spanish_agent,
                msg,
            ),
            Runner.run(
                spanish_agent,
                msg,
            ),
            Runner.run(
                spanish_agent,
                msg,
            ),
        )

        print("\nParallel translations completed. Processing outputs...")
        outputs = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]

        translations = "".join(outputs)
        print(f"\nTranslations:\n{translations}")

        print("\nRunning translation picker to select the best translation...")
        best_translation = await Runner.run(
            translation_picker,
            f"Input: {msg}\nTranslations:\n{translations}",
        )

    print("-----")
    print(f"Best translation: {best_translation.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
