"""
主文件: 用来从web界面测试multi-agent-gpt的性能
"""
#加载环境变量，其中包括openai的API密钥等设置
import os
from dotenv import load_dotenv
load_dotenv()
#调用依赖包
import gradio as gr
from Agents.openai_agents import AgentModel
from gradio_multimodalchatbot import MultimodalChatbot
from gradio.data_classes import FileData
from PIL import Image
import time

         
# 实例化核心功能对象
model_center = AgentModel(trace_log=True)
# 创建一个 Web 界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):   
        with gr.Column(scale=15):
            # 展示的页面标题
            gr.Markdown("""
                        <p style="text-align:center; font-size:32px;"><strong>Multi-Agent-GPT</strong></p>
                        <p style="text-align:center; font-size:18px;">Author: Elbert</p>
                """)

    with gr.Row():
        with gr.Column(scale=4):
            # 创建一个聊天机器人对象
            chatbot = MultimodalChatbot(height=450, show_copy_button=True)
            #chatbot = gr.Chatbot(height=450, show_copy_button=True)
            # 创建一个文本框组件，用于输入 prompt。
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                # 创建提交按钮。
                db_wo_his_btn = gr.Button("Chat")
            with gr.Row():
                # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                clear = gr.ClearButton(
                    components=[chatbot], value="Clear console")
                
        # 设置按钮的点击事件。当点击时，调用上面定义的 qa_chain_self_answer 函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
        db_wo_his_btn.click(model_center.aq_agent_MultimodalChatbot_web, inputs=[
                            msg], outputs=[chatbot])
        # 设置用户在输入完消息后可以使用回车进行提交
        msg.submit(model_center.aq_agent_MultimodalChatbot_web, inputs=[
                            msg,chatbot], outputs=[msg,chatbot])
        
    gr.Markdown("""提醒：<br>
    1. 在指定模型使用绘画工具时运行时间会很长，请耐心等待。
    2. 目前还不能展示完整的对话过程。<br>
    """)
gr.close_all()
# 直接启动
demo.launch()
#请使用工具帮我画一幅高山和溪流的画