from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from ..base_tools_procedure.chat_learning_tool import do_internal_chat_learning_tool


class ChatLearningToolInput(BaseModel):
    question: str = Field(description="Input request for the chat learning tool")


@tool("chat-learning-tool", args_schema=ChatLearningToolInput, return_direct=True)
def chat_learning_react_tool(question: str) -> str:
    """This tool useful when the user asks you to remember or learn something.
    Action Input should be only the relevant information to remember/learn.
    Run the tool when the user asks you to learn or remember something, get only the text that represents the informations to learn or remember;
    For example: 1. if you receive the request "I want you to learn that [...]" run the tool and get only the [...] text
    or 2. if you receive the request "learn the following: [...]", run the tool and get only the [...] text"""
    return do_internal_chat_learning_tool(question)
