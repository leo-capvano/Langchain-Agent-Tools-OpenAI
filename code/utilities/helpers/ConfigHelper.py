import json

from .DocumentProcessorHelper import Processor
from .EnvHelper import EnvHelper
from ..common.ResourceReader import read_resource
from ..document_chunking import ChunkingSettings, ChunkingStrategy
from ..document_loading import LoadingSettings, LoadingStrategy
from ..orchestrator import OrchestrationStrategy, OrchestrationSettings

CONFIG_CONTAINER_NAME = "config"


class Config:
    def __init__(self, config: dict):
        self.prompts = Prompts(config['prompts'])
        self.messages = Messages(config['messages'])
        self.logging = Logging(config['logging'])
        self.document_processors = [
            Processor(
                document_type=c['document_type'],
                chunking=ChunkingSettings(c['chunking']),
                loading=LoadingSettings(c['loading'])
            )
            for c in config['document_processors']]
        self.env_helper = EnvHelper()
        self.default_orchestration_settings = {'strategy': self.env_helper.ORCHESTRATION_STRATEGY}
        self.orchestrator = OrchestrationSettings(self.default_orchestration_settings)

    def get_available_document_types(self):
        return ["txt", "pdf", "url", "html", "md", "jpeg", "jpg", "png", "docx"]

    def get_available_chunking_strategies(self):
        return [c.value for c in ChunkingStrategy]

    def get_available_loading_strategies(self):
        return [c.value for c in LoadingStrategy]

    def get_available_orchestration_strategies(self):
        return [c.value for c in OrchestrationStrategy]


class Prompts:
    def __init__(self, prompts: dict):
        self.condense_question_prompt = Prompts.read_prompt_file(
            "condense_question_prompt.txt") if "condense_question_prompt" not in prompts else prompts[
            'condense_question_prompt']
        self.answering_prompt = Prompts.read_prompt_file(
            "answering_prompt.txt") if "answering_prompt" not in prompts else prompts['answering_prompt']
        self.post_answering_prompt = Prompts.read_prompt_file(
            "post_answering_prompt.txt") if "post_answering_prompt" not in prompts else prompts['post_answering_prompt']
        self.enable_post_answering_prompt = prompts['enable_post_answering_prompt']
        self.enable_content_safety = prompts['enable_content_safety']

    @staticmethod
    def read_prompt_file(prompt_file_name: str):
        return read_resource(prompt_file_name)


class Messages:
    def __init__(self, messages: dict):
        self.post_answering_filter = messages['post_answering_filter']


class Logging:
    def __init__(self, logging: dict):
        self.log_user_interactions = logging['log_user_interactions']
        self.log_tokens = logging['log_tokens']


class ConfigHelper:
    @staticmethod
    def get_active_config_or_default():
        print("Returning default config")
        return Config(json.loads(read_resource("default_config.json")))
