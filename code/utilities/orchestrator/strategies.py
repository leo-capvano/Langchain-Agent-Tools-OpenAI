from enum import Enum


class OrchestrationStrategy(Enum):
    LANGCHAIN_OPENAI_TOOLS = "langchain_openai_tools"
    LANGCHAIN = 'langchain'


def get_orchestrator(orchestration_strategy: str):
    if orchestration_strategy == OrchestrationStrategy.LANGCHAIN.value:
        from .langchain_agent import LangChainAgent
        from ..tools.react_tools.question_answer_tool import question_answering_react_tool
        from ..tools.react_tools.chat_learning_tool import chat_learning_react_tool
        return LangChainAgent([question_answering_react_tool, chat_learning_react_tool])
    elif orchestration_strategy == OrchestrationStrategy.LANGCHAIN_OPENAI_TOOLS.value:
        from .langchain_agent import LangChainAgent
        from ..tools.openai_tools.question_answer_tool import question_answering_openai_tool
        from ..tools.openai_tools.chat_learning_tool import chat_learning_openai_tool
        return LangChainAgent([question_answering_openai_tool, chat_learning_openai_tool])
    else:
        raise Exception(f"Unknown orchestration strategy: {orchestration_strategy}")
