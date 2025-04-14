import asyncio
from personal_study_assistant.manager import PersonalStudyAssistant
from personal_study_assistant.context import Context

async def run_researcher() -> None:
    await PersonalStudyAssistant().run("I have to learn python by next week.")


def main() -> None:
    asyncio.run(run_researcher())


if __name__ == "__main__":
    main()
