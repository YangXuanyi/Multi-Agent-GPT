<div align="center">

![poster](https://github.com/YangXuanyi/Multi-Agent-GPT/assets/83216339/b111f8f3-3b14-42dc-89b3-9a26c7a7deeb)

##

A multimodal expert assistant GPT platform built using RAG+agent. It integrates tools for modalities such as text, images, and audio. Support local deployment and private database construction.

![Code](https://img.shields.io/badge/Code-python-purple)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat#pic_center)](http://makeapullrequest.com)
![license](https://img.shields.io/badge/License-MIT-{右半部分颜色})


[Web Video](https://github.com/YangXuanyi/Multi-Agent-GPT/assets/83216339/30e76e97-d02e-4a18-b5e1-896be99d5564)

</div>

## 💡 1 RoadMap

`1` Basic Function
   - [x] Single/multi turn chat
   - [x] Multimodal information display and interaction
   - [x] Agent
   - [x] Tools
      - [x] Web searching
      - [x] Image generation
      - [x] Image caption
      - [ ] audio-to-text
      - [ ] text-to-audio
      - [ ] Video caption
   - [ ] RAG
      - [ ] Private database
      - [ ] Offline deployment

   

`2` Supporting Information Modality
   - [x] text
   - [x] image
   - [ ] audio
   - [ ] video

`3` Model Interface API
   - [x] ChatGPT
   - [x] Dalle
   - [x] Google-Search
   - [x] BLIP

## 👨‍💻 2 Development

Project technology stack: Python + torch + langchain + gradio

### **⚡ 2.1 Installation**

1. Create a virtual environment in Anaconda:

  ```
  conda create -n agent python=3.10
  ```

2. Enter the virtual environment and Install related dependency packages:
  
  ```
  conda activate agent
  ```

  ```
  pip install -r ./requirements.txt
  ```

3. Install the BLIP model locally, open the [BLIP website](https://huggingface.co/Salesforce/blip-image-captioning-large), and download all files to ``Models/BLIP``.


4. Follow the prompts to configure the key for the API that needs to be used in the `.env`.



### **💻 2.2 Demo**

Multi Agent GPT provides UI interface interaction, allowing users to launch agents and achieve intelligent conversations by running the ``web.py``:

```
python ./web.py
```
The program will run a local URL: http://XXX. Open using a local browser to see the UI interface:

<div align="center">

![demo](https://github.com/YangXuanyi/Multi-Agent-GPT/assets/83216339/82444566-c7db-41ab-b471-cc3fba5ada82)

</div>

### **📻 2.3 News**

#### 1 Chat_with_Image

By integrating the BLIP model, agents can understand image information and provide high-quality dialogue information.



## 🗄️ 3 Structure

```
- .env
- Agents/
  - openai_agents.py  #用来定义基于gpt3.5的agent
- Database/
- Docs/
- Imgs/
  - Show/                #存储一些示例图片
- Models
  - BLIP                 #图像理解大模型
- Tools/
  - ImageCaption.py      #基于BLIP的图像理解工具
  - ImageGeneration.py  #定义了一个基于openai dalle的文本生成图像的工具
  - search.py            #基于Google-search的联网搜索工具
- Utils/
  - data_io.py
  - stdio.py            #实现了如何截获当前程序的日志信息，主要是用来获取agent的verbose信息
  - utils_image.py      #关于图像处理的一些功能函数
  - utils_json.py       #从已有的log日志信息中提取相关的有用字段(服务stdio) 
- python_new_funciton.py #开发过程中的测试文件
- readme.md
- requirements.txt
- web.py                 #主运行文件

```