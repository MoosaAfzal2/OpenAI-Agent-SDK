import asyncio
from research_bot.manager import ResearchManager


async def run_researcher() -> None:
    query = input("What would you like to research? ")
    await ResearchManager().run(query)


def main() -> None:
    asyncio.run(run_researcher())


if __name__ == "__main__":
    main()
