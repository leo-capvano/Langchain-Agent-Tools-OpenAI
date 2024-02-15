from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from langchain_core.runnables import RunnableLambda, RunnableBranch

from utilities.common.Answer import Answer
from utilities.common.SourceDocument import SourceDocument
from utilities.helpers.ConfigHelper import ConfigHelper
from utilities.helpers.LLMHelper import LLMHelper
from utilities.helpers.VectorStoreHelper import VectorStoreHelper


def do_internal_question_answering_tool(question: str) -> str:
    llm_helper = LLMHelper()
    config = ConfigHelper.get_active_config_or_default()

    context_rag_documents = VectorStoreHelper().get_vector_store().similarity_search(query=question, k=4,
                                                                                     search_type="hybrid")

    question_answering_prompt = PromptTemplate(template=config.prompts.answering_prompt,
                                               input_variables=["question", "sources"])
    question_answering_chain = LLMChain(llm=llm_helper.get_llm(), prompt=question_answering_prompt,
                                        verbose=True)

    post_answering_prompt = PromptTemplate(template=config.prompts.post_answering_prompt,
                                           input_variables=["question", "answer", "sources"])
    post_answering_chain = LLMChain(llm=llm_helper.get_llm(), prompt=post_answering_prompt, verbose=True)

    full_chain = (question_answering_chain |
                  {"question": RunnableLambda(lambda x: question),
                   "answer": RunnableLambda(lambda prev_chain_result: prev_chain_result['text']),
                   "sources": RunnableLambda(lambda x: context_rag_documents)} |
                  {"post_answering": RunnableBranch(
                      (lambda x: config.prompts.enable_post_answering_prompt == True, post_answering_chain),
                      (lambda x: config.prompts.enable_post_answering_prompt == False,
                       RunnableLambda(lambda x: {"text": "True"})),
                      lambda x: {"text": "True"}
                  ), "original_chain_result": RunnableLambda(lambda x: x['answer'])})

    sources_text = "\n\n".join(
        [f"[doc{i + 1}]: {source.page_content}" for i, source in enumerate(context_rag_documents)])
    with get_openai_callback() as cb:
        lcel_result = full_chain.invoke({"question": question, "sources": sources_text})

    answer: str = lcel_result["original_chain_result"] if lcel_result[
                                                              "post_answering"][
                                                              "text"].lower() == "true" else config.messages.post_answering_filter
    print(f"Answer: {answer}")

    # Generate Answer Object
    source_documents = []
    for source in context_rag_documents:
        source_document = SourceDocument(
            id=source.metadata["id"],
            content=source.page_content,
            title=source.metadata["title"],
            source=source.metadata["source"],
            chunk=source.metadata["chunk"],
            offset=source.metadata["offset"],
            page_number=source.metadata["page_number"],
        )
        source_documents.append(source_document)

    clean_answer = Answer(question=question,
                          answer=answer,
                          source_documents=source_documents,
                          prompt_tokens=cb.prompt_tokens,
                          completion_tokens=cb.completion_tokens)

    return clean_answer.to_json()
