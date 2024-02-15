from typing import List

from ..orchestrator import get_orchestrator


class Orchestrator:
    def __init__(self) -> None:
        pass

    def handle_message(self, user_message: str, chat_history: List[dict], conversation_id: str, orchestrator,
                       **kwargs: dict) -> dict:
        orchestrator = get_orchestrator(orchestrator.strategy.value)
        if orchestrator is None:
            raise Exception(f"Unknown orchestration strategy")
        return orchestrator.orchestrate(user_message, chat_history)
