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
from Tools.ImageCaption import ImageCaption #图像内容理解工具
from Utils.stdio import ConsoleOutput
from Utils.utils_json import extract_json_and_observation, extract_urls
from Utils.data_io import multifile_classification


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
        #定义LLM
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        #定义目前可用的工具
        self.tools = [ImageExpressionByDalle(), InternetSearch()]
        #定义系统提示词, 需要根据实际工具进行重写
        self.system_message = self.init_SystemPrompt()
        
        #加载图像理解工具
        self.imagecaption = ImageCaption()
        
    def init_SystemPrompt(self):
        """
        重写llm中的系统提示词, 让llm能够正确的选择Tools完成任务,
        该函数的设置与agent使用的Tools有关
        """
        #重写llm中的system prompt，让模型凡是遇到生成图像问题统一交给Tool来解决
        system_message = PREFIX + "\n" + '''
            Unfortunately, the assistant is unable to generate images based on text. 
            Assistants should always refer to available tools and not attempt to answer any drawing related questions on their own. 
            When deciding to use a text generated image tool, please generate detailed prompts for the tool based on the user's questions'''
        
        return system_message
    
    
    def init_openai_agent(self, memory=None):
        """
        实例化一个基于openai的agent
        为了实现上下文对话的记忆, 需要传入memory
        """
        
        #实例化agent
        agent = initialize_agent(
                            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                            tools=self.tools,
                            llm=self.llm,
                            verbose=True,
                            max_iterations=3,
                            early_stopping_method='generate',
                            memory=memory
                        )
        
        #传入重写的系统提示词, 让agent更好的完成任务
        new_prompt = agent.agent.create_prompt(
                        system_message=self.system_message,
                        tools=self.tools
                        )
        agent.agent.llm_chain.prompt = new_prompt
        
        return agent
    
        
    def aq_agent_MultimodalChatbot_web(self, question, chat_history, multifile):
        """
        多模态显示的web端
        """

        #获取历史会话只内存
        memory = self.load_history2memory(window_length=5, chat_history=chat_history)
        #实例化agent
        agent = self.init_openai_agent(memory=memory)
        
        #处理非文字模态的输入信息
        if multifile != None:
            file_type, file_path = multifile_classification(multifile)
            if file_type == "image":
                image = Image.open(file_path)
                text = question
                caption_result = self.imagecaption.infer_image(image,text)
            user_msg = {"text": question,
                        "files": [{"file": FileData(path=file_path)}]}
        else:
            user_msg = {"text": question,
                    "files": []}
        
        #先实例化日志输出类，指定可以将log读入内存，然后调用智能体开始监视
        console_output = ConsoleOutput()
        # 重定向sys.stdout到ConsoleOutput对象和日志文件对象
        sys.stdout = console_output
        
        # 考虑当前问题是否涉及到处理多模态文件，
        # 如果涉及则使用大模型对问题+多模态识别结果进行二次预测
        if multifile != None:
            prompt = '这是一个看图回答问题的对话, 不用调用任何Tool, 请直接用中文回答。目前图像中的内容可以总结为：' \
                     + caption_result  + '\n请根据图像中的内容和回答下面的问题: '
            question =  prompt + question
        
        result = agent(question)
        log = console_output.get_information()
        robot_msg = self.data_postprocess(result, log)   
        chat_history.append([user_msg, robot_msg])

        return "", chat_history
    
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
    
    def load_history2memory(self, window_length, chat_history):
        """
        将chat_history读入内存中, 作为上下文对话信息输入agent, 实现关注上下文的多轮对话
        window_length: 设置当前问答中关注的上下文窗口大小
        chat_history: 自对话启动后所有的历史对话记录 
        """
        #定义agent需要的对话记录形式memory
        memory=ConversationBufferWindowMemory(
                            memory_key='chat_history',
                            k=window_length,
                            return_messages=True
                            )
        
        #从chat_history制作上下文关系memory
        memory_list = chat_history[-window_length:]
        for i in range(len(memory_list)):
            input_context = memory_list[i][0].text
            output_context = memory_list[i][1].text
            memory.save_context({"input": input_context}, 
                                {"output": output_context})
        
        return memory
    
    def qa_agent_web(self, question: str):
        """
        web端专用qa,当前在弃用状态
        """
        agent = self.init_openai_agent()
        json = '\n the trace log is:\n'
        if self.trace_log:
            #先实例化日志输出类，指定可以将log读入内存，然后调用智能体开始监视
            console_output = ConsoleOutput()
            # 重定向sys.stdout到ConsoleOutput对象和日志文件对象
            sys.stdout = console_output
            result = agent(question)
            log = console_output.get_information()
            json_data, observation_data = extract_json_and_observation(log)
            json = str(json_data[0])
        else:
            result = agent(question)
        
        
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
        memory=ConversationBufferWindowMemory(
                            memory_key='chat_history',
                            k=5,
                            return_messages=True
                            )
        agent = self.init_openai_agent(memory=memory)
        result = agent(question)
        output =  result["output"]
        return output
    
    
# #提问
# #第一次
# agent = AgentModel()
# while True:
#     query = input("请输入问题：")
#     result = agent.qa_agent(query)
#     url = extract_urls_from_string(result["output"])
#     print(url[0]) #打印绘制图像的url链接 url是一个list，里面存折在output里识别出的所有的url链接