from agents import (
    Runner,
    Model,
    RunConfig,
    RunResult,
    RunResultStreaming,
    TResponseInputItem,
)

from personal_study_assistant.agents.scheduler_agent import scheduler_agent
from personal_study_assistant.config import model as globalModel, config as globalConfig


class PersonalStudyAssistant:
    def __init__(
        self,
        model: str | Model | None = None,
        config: RunConfig | None = None,
        context=None,
    ):
        self.config = config or globalConfig
        self.model = model or globalModel
        self.context = context

    async def run(self, query: str | list[TResponseInputItem]) -> RunResult:
        """
        Run the personal study assistant with the given query.
        This method initializes the context and runs the scheduler agent with the provided query.
        """
        result = await Runner.run(
            starting_agent=scheduler_agent,
            input=query,
            run_config=self.config,
            context=self.context,
        )

        return result

    async def run_streamed(
        self, query: str | list[TResponseInputItem]
    ) -> RunResultStreaming:
        """
        Run the personal study assistant with the given query.
        This method initializes the context and runs the scheduler agent with the provided query.
        """

        result = Runner.run_streamed(
            starting_agent=scheduler_agent,
            input=query,
            run_config=self.config,
            context=self.context,
        )

        return result
