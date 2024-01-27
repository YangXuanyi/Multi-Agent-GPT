from langchain.tools import BaseTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

#绘制图像Tool, 名字可以随便起，只要基于BaseTool即可
class ImageExpressionByDalle(BaseTool):
    name = "str to Image"  #工具名称
    #工具的描述，这个很重要，它相当于一个提示词，llm会根据这个来判断当前的任务适不适合用这个工具去解决
    description = 'Use this tool to generate images with text as prompts'

    def _run(self, expr: str):
        '''
        同步相应处理函数：这个工具要实现的具体功能
        expr是llm想Tool里的输入
        '''
        #eval(expr)
        dalle = DallEAPIWrapper()
        result = dalle.run(query=expr)
        return result
    
    def _arun(self, query: str):
        '''
        异步相应处理函数
        '''
        raise NotImplementedError("Async operation not supported yet")