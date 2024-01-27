"""
主文件: 调试agent
"""
#加载环境变量，其中包括openai的API密钥等设置
from dotenv import load_dotenv
load_dotenv()
#调用依赖包
from Agents.openai_agents import AgentModel
import sys
from Utils.stdio import ConsoleOutput

#实例化agent
agent = AgentModel()

# 创建ConsoleOutput对象用来截获agnet的log信息
console_output = ConsoleOutput()
# 重定向sys.stdout到ConsoleOutput对象和日志文件对象
sys.stdout = console_output


while True:
    question = input("请问：")
    result = agent.qa_agent_debug(question=question)
    log_content = console_output.get_information() #获取当前的log信息
    console_output.clear_information() #清空当前截获的log信息
