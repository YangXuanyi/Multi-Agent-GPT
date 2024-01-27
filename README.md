# Multi-Agent-GPT
Multi-Agent-GPT: A multimodal expert assistant GPT platform built using RAG+agent. It integrates tools for modalities such as text, images, and audio. Support local deployment and private database construction.

# Web
Multi-Agent-GPT can interact on web pages through Gradio. 

The following video shows how to directly communicate with the GPT3.5 model, call the Dalle drawing tool, and call the Serpapi online search tool. Implemented multimodal result output:

[Web Video](https://github.com/YangXuanyi/Multi-Agent-GPT/assets/83216339/f6e69cb1-d97f-4fe5-a306-a8e386ac9914)


# File Structure

```
- .env
- Agents/
  - openai_agents.py  #用来定义基于gpt3.5的agent
- Database/
- Docs/
- Imgs/
- Tools/
  - ImageGeneration.py  #定义了一个基于openai dalle的文本生成图像的工具
- Utils/
  - stdio.py            #实现了如何截获当前程序的日志信息，主要是用来获取agent的verbose信息
  - utils_image.py      #关于图像处理的一些功能函数
  - utils_json.py       #从已有的log日志信息中提取相关的有用字段(服务stdio) 
- debug.py
- web.py
- readme.md
```


