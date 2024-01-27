"""
重新定义log日志信息的输出方向, 用于截获agent中的log信息
"""

import sys
from io import StringIO

# 定义一个自定义的文件对象，用于在控制窗口中输出
class ConsoleOutput:
    def __init__(self):
        # 创建一个内存中的文件对象，用于写入日志文件
        self.log_file = StringIO()
        
    def write(self, message):
        # 在控制窗口中输出
        sys.__stdout__.write(message)
        sys.__stdout__.flush()
        # 写入日志文件
        self.log_file.write(message)
        self.log_file.flush()
    
    def get_information(self):
        """
        获取当前控制台的log信息
        """
        return self.log_file.getvalue()
    
    
    def clear_information(self):
        """
        用来清空当前截取到的所有log日志信息
        """
        self.log_file.truncate(0)   #清空信息
        self.log_file.seek(0)       #将指针重新定位到文件的开头
