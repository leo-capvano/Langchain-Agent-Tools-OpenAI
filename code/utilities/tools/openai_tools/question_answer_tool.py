from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from ..base_tools_procedure.question_answer_tool import do_internal_question_answering_tool


class QuestionAnsweringToolInput(BaseModel):
    question: str = Field(description="Input question to be used by question answering tool")


@tool("question-answering-tool", args_schema=QuestionAnsweringToolInput)
def question_answering_openai_tool(question: str) -> str:
    """useful for when you need to answer questions about anything.
    Input should be a fully formed question. Do not call the tool for text processing
    operations like translate, summarize, make concise."""
    return do_internal_question_answering_tool(question)
