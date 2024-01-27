from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import os
import sys
import urllib.request
from urllib.parse import urlparse
from langchain.agents.conversational_chat.prompt import (PREFIX)
from gradio.data_classes import FileData
from PIL import Image

from Tools.ImageGeneration import ImageExpressionByDalle  #导入生成图像工具
from Tools.search import InternetSearch  #联网搜索工具
from Utils.stdio import ConsoleOutput
from Utils.utils_json import extract_json_and_observation, extract_urls


# os.environ["OPENAI_API_BASE"] = 'https://oneapi.xty.app/v1'
# os.environ["OPENAI_API_KEY"] = 'sk-yIjuHjfVC2v4Of88050b6a4404444d9eAdD507DfC1Dd382d'

class AgentModel():
    """
    代理人类
    """
    def __init__(self, trace_log=False):
        '''
        参数：
        trace_log: 是否截获当前agent的log日志信息, 原本的log信息是直接打印在控制台上的
                   可以调用此功能来将log信息实时载入内存, 进行程序调用
        
        '''
        self.trace_log = trace_log
        
        #实例化LLM
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        
        #定义目前可用的工具
        self.tools = [ImageExpressionByDalle(), InternetSearch()]
        
        #实例化agent
        self.agent = initialize_agent(
                            agent='chat-conversational-react-description',
                            tools=self.tools,
                            llm=self.llm,
                            verbose=True,
                            max_iterations=3,
                            early_stopping_method='generate',
                            memory=ConversationBufferWindowMemory(
                            memory_key='chat_history',
                            k=5,
                            return_messages=True
                            )
                        )

        #重写llm中的system prompt，让模型凡是遇到生成图像问题统一交给Tool来解决
        self.system_message = PREFIX + "\n" + '''
            Unfortunately, the assistant is unable to generate images based on text. 
            Assistants should always refer to available tools and not attempt to answer any drawing related questions on their own. 
            When deciding to use a text generated image tool, please generate detailed prompts for the tool based on the user's questions'''

        #特殊语法,记住
        self.new_prompt = self.agent.agent.create_prompt(
                        system_message=self.system_message,
                        tools=self.tools
                        )
        self.agent.agent.llm_chain.prompt = self.new_prompt
    
    def aq_agent_MultimodalChatbot_web(self, question:str, chat_history: list=[]):
        """
        多模态显示的web端
        """
        user_msg = {"text": question,
            "files": []
        }
        
        if self.trace_log:
            #先实例化日志输出类，指定可以将log读入内存，然后调用智能体开始监视
            console_output = ConsoleOutput()
            # 重定向sys.stdout到ConsoleOutput对象和日志文件对象
            sys.stdout = console_output
            result = self.agent(question)
            log = console_output.get_information()
            robot_msg = self.data_postprocess(result, log)   
        else:
            result = self.agent(question)
            robot_msg = user_msg
        
        chat_history.append([user_msg, robot_msg])
        return "", chat_history
    
        #return [[user_msg, robot_msg]]
    
    def data_postprocess(self, result, log):
        """
        对agent输出的结果信息result和日志信息log做标准化处理, 使之符合chatbot的输出格式
        """
        #检查输出信息中是否含有图像
        imgs_url = extract_urls(str(log))
        if len(imgs_url)>0:
            # 下载图像并保存到本地文件
            img_path = './Imgs/image.jpg'
            urllib.request.urlretrieve(imgs_url[0], img_path)
            robot_msg = {"text": result["output"],
                         "files": [{"file": FileData(path=img_path)}]}
        else:
            robot_msg = {"text": result["output"],
                         "files": []}
        return robot_msg
    
    def qa_agent_web(self, question: str):
        """
        web端专用qa
        """
        json = '\n the trace log is:\n'
        if self.trace_log:
            #先实例化日志输出类，指定可以将log读入内存，然后调用智能体开始监视
            console_output = ConsoleOutput()
            # 重定向sys.stdout到ConsoleOutput对象和日志文件对象
            sys.stdout = console_output
            result = self.agent(question)
            log = console_output.get_information()
            json_data, observation_data = extract_json_and_observation(log)
            json = str(json_data[0])
        else:
            result = self.agent(question)
        
        
        #关于输出的格式说明：
        # 首先输出参数的数量和web中的outputs=[chatbot]列表中的参数数量是一一对应的
        # 其次在return中每一个返回值都应该写成元组+列表的形式
        # 以当前为例，因问outputs的接收列表中只有一个参数，所以只需要return一个结果（列表）即可
        # 其中的结果必须是：[(结果)]。在这个示例中我们返回的结果是question+ result["output"]
        # 它们两个是一个参数
        return [(question, result["output"]+json)]

    def qa_agent_debug(self, question: str):
        """
        调试专用qa接口
        """
        result = self.agent(question)
        return result
    
    
# #提问
# #第一次
# agent = AgentModel()
# while True:
#     query = input("请输入问题：")
#     result = agent.qa_agent(query)
#     url = extract_urls_from_string(result["output"])
#     print(url[0]) #打印绘制图像的url链接 url是一个list，里面存折在output里识别出的所有的url链接