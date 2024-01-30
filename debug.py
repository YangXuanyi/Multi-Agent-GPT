"""
主文件: 调试agent
"""
#加载环境变量，其中包括openai的API密钥等设置
import os
from dotenv import load_dotenv
from Agents.openai_agents import AgentModel
agent_1 = AgentModel(trace_log=True)

while True:
    question = input("请问：")
    result = agent_1.qa_agent_debug(question=question)
    print(result)