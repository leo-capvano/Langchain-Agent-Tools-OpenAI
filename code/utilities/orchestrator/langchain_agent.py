import logging
from typing import List

from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import get_openai_callback

from .agent_executor_factory import get_agent_executor
from ..common.Answer import Answer
from ..helpers.LLMHelper import LLMHelper
from ..parser.OutputParserTool import OutputParserTool


class LangChainAgent:
    def __init__(self, tools: list) -> None:
        super().__init__()
        self.tools = tools

    def orchestrate(self, user_message: str, chat_history: List[dict], **kwargs: dict) -> List[dict]:
        llm_helper = LLMHelper()
        output_formatter = OutputParserTool()

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        for message in chat_history:
            memory.chat_memory.add_user_message(message[0])
            memory.chat_memory.add_ai_message(message[1])

        agent_executor = get_agent_executor(llm=llm_helper.get_llm(), memory=memory, tools=self.tools)
        with get_openai_callback() as cb:
            try:
                answer = agent_executor.invoke({"input": user_message}).get("output")
                logging.info("Used tokens: %s", cb.completion_tokens)
            except Exception as e:
                logging.exception(e)
                answer = "I'm sorry, an error occurred during the generation"
        try:
            answer = Answer.from_json(answer)
        except:
            answer = Answer(question=user_message, answer=answer)

        return output_formatter.parse(question=answer.question, answer=answer.answer,
                                      source_documents=answer.source_documents)
