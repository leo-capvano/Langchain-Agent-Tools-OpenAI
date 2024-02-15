from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_react_agent
from langchain_core.prompts import PromptTemplate

from ..common.ResourceReader import read_resource
from ..helpers.EnvHelper import EnvHelper


def get_agent_executor(llm, memory, tools: list):
    env_helper = EnvHelper()
    if env_helper.ORCHESTRATION_STRATEGY == "langchain_openai_tools":
        agent_prompt = hub.pull("hwchase17/openai-tools-agent")
        openai_tools_agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=agent_prompt)
        agent_executor = AgentExecutor(agent=openai_tools_agent, tools=tools, memory=memory, verbose=True)
        return agent_executor
    elif env_helper.ORCHESTRATION_STRATEGY == "langchain":
        agent_prompt = PromptTemplate.from_template(read_resource("agent_prompt.txt"))
        react_agent = create_react_agent(llm=llm, tools=tools, prompt=agent_prompt)
        return AgentExecutor(agent=react_agent, tools=tools, memory=memory, verbose=True)
