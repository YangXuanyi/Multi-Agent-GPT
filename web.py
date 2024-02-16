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
from Utils import data_io
from gradio_multimodalchatbot import MultimodalChatbot

        
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
                """)

    with gr.Row():
        with gr.Column(scale=5):
            # 创建一个聊天机器人对象
            chatbot = MultimodalChatbot(height=450, show_copy_button=True)
            #chatbot = gr.Chatbot(height=450, show_copy_button=True)
            # 创建一个文本框组件，用于输入 prompt。
            with gr.Row():
                msg = gr.Textbox(placeholder="请提问：",
                                 scale=5)  #scale用于控制在同行中不同控件的长度占比
                multifile_show = gr.File(height=50, scale=0)
                
                with gr.Row():
                    #1 创建上传文件按钮，按钮本身返回文件的地址str
                    multifile_btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])
                    #2 创建删除当前上传文件按钮
                    clear_file = gr.ClearButton(
                                 components=[multifile_btn, multifile_show], value="Clear File")
                    #3 创建提交按钮。
                    db_wo_his_btn = gr.Button("Chat")
                    #4 创建清除按钮，用于清除聊天机器人组件的内容。
                    clear = gr.ClearButton(
                             components=[chatbot, multifile_show], value="Clear console")

        ###########################################################################
        #************************各功能按钮对应的触发事件链接************************
        #点击事件的书写模板：按钮.点击类型(激发的函数, input=[激发函数传入的参数], 
        #                               output=[将激发函数传出的参数赋值给...])
        ###########################################################################
   
        multifile_btn.upload(data_io.upload_file, inputs=[multifile_btn], 
                             outputs=[multifile_show])
        
        # 设置按钮的点击事件。当点击时，调用上面定义的 qa_chain_self_answer 函数，
        # 并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
        db_wo_his_btn.click(model_center.aq_agent_MultimodalChatbot_web, inputs=[
                            msg, chatbot, multifile_btn], outputs=[msg, chatbot])
        # 设置用户在输入完消息后可以使用回车进行提交
        msg.submit(model_center.aq_agent_MultimodalChatbot_web, inputs=[
                            msg, chatbot, multifile_btn], outputs=[msg,chatbot])
        
    gr.Markdown("""提醒：<br>
    1. 在指定模型使用绘画工具时运行时间会很长，请耐心等待。
    2. 图像理解采用本地部署BLIP的方式, 对GPU性能要求较高。<br>
    """)

#gr.close_all()
# 直接启动
demo.launch()