import os

from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI


class LLMHelper:

    def get_llm(self):
        # return AzureChatOpenAI(deployment_name=self.llm_model, temperature=0, max_tokens=self.llm_max_tokens, openai_api_version=openai.api_version)
        return AzureChatOpenAI(openai_api_version="2023-09-15-preview",
                               azure_deployment="genai-oai-gpt35-turbo",
                               azure_endpoint="https://swedencentral.api.cognitive.microsoft.com",
                               openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
                               temperature=0,
                               model_name="gpt-35-turbo-instruct")

    def get_embedding_model(self):
        # return OpenAIEmbeddings(deployment=self.embedding_model, chunk_size=1)
        return AzureOpenAIEmbeddings(openai_api_version="2023-09-15-preview",
                                     azure_deployment="genai-oai-ada-002",
                                     azure_endpoint="https://swedencentral.api.cognitive.microsoft.com",
                                     openai_api_key=os.getenv("AZURE_OPENAI_KEY"))
