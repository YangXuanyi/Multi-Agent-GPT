from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.tools import BaseTool

#联网搜索Tool, 名字可以随便起，只要基于BaseTool即可
class InternetSearch(BaseTool):
    name = "internet search"  #工具名称
    #工具的描述
    description = 'Use this tool to access the internet and obtain the latest knowledge'

    def _run(self, expr: str):
        '''
        同步相应处理函数：这个工具要实现的具体功能
        expr是llm想Tool里的输入
        '''
        #eval(expr)
        serpapi = SerpAPIWrapper()
        result = serpapi.run(query=expr)
        return result
    
    def _arun(self, query: str):
        '''
        异步相应处理函数
        '''
        raise NotImplementedError("Async operation not supported yet")