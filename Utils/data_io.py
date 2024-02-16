"""
聊天机器人数据交互功能
"""

def upload_file(files):
    """
    此函数为UI界面的“文件上载”按钮服务,具体的功能是当文件上载后将链接发送至gr.File()组件显示
    因为上载按钮返回的files就是数据文件链接, 即显示组件的输入, 所以函数内部无需做操作, 直接回传
    """
    return files

def multifile_classification(files):
    """
    此函数负责解析上传至gr.File()中的文件类型
    目前支持图像，后续会扩展音频和视频等多模态信息类型, 方便agent的数据读取和处理
    """
    
    #some classification method
    
    file_tpye = "image"
    file_path = files #因为目前只支持图像类型，所以files默认传出的就是图像的path
    
    return file_tpye, file_path