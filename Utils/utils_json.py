"""
这个文件集成了使用正则化提取log信息的一些工具
"""
import re

import re

import re

def extract_urls(text):
    # 定义URL的正则表达式模式
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F])|\))*')

    # 使用finditer函数迭代查找所有匹配的URL
    matches = re.finditer(url_pattern, text)

    # 提取匹配项的值，并存放在列表中
    urls = [match.group().rstrip(')') for match in matches]

    return urls

def extract_json_and_observation(log_data):
    
    json_pattern = r'```json\n(.*?)\n```'
    observation_pattern = r'Observation: (.+?)(?=\n\n)'

    json_matches = re.finditer(json_pattern, log_data, re.DOTALL)
    observation_matches = re.finditer(observation_pattern, log_data)

    json_data = [match.group(1) for match in json_matches]
    observation_data = [match.group(1) for match in observation_matches]

    return json_data, observation_data

#########################################################################
#example
#########################################################################

json = '''
> Entering new AgentExecutor chain...
```json
{
    "action": "str to Image",
    "action_input": "我的名字叫Assistant"
}
```
Observation: https://oaidalleapiprodscus.blob.core.windows.net/private/org-XS04I63QDU2nxnczjF49v5JY/user-xiVSgHzIMP2RmZx4CIk5PuBM/img-s6nxCvs2eiE4C8i86bcFJjhx.png?st=2024-01-22T05%3A36%3A21Z&se=2024-01-22T07%3A36%3A21Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-21T19%3A41%3A14Z&ske=2024-01-22T19%3A41%3A14Z&sks=b&skv=2021-08-06&sig=KZKC6Wq0JBTv72O4fFtClUL9Yzs7GqLnJpZJPwoMfqk%3D
Thought:```json
{
    "action": "Final Answer",
    "action_input": "我的名字叫Assistant"
}
```

> Finished chain.
'''
#json_data, observation_data = extract_json_and_observation(json)

ss =  '''
Observation: [36;1m[1;3mhttps://oaidalleapiprodscus.blob.core.windows.net/private/org-dN8AExG0uBkDqJqA7CbNq3Q5/user-n0EINDNhlbpFlQTFbfEKhnn2/img-XymEQV65Chg8YQm5lMcBZp9A.png?st=2024-01-23T11%3A25%3A02Z&se=2024-01-23T13%3A25%3A02Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-22T21%3A50%3A09Z&ske=2024-01-23T21%3A50%3A09Z&sks=b&skv=2021-08-06&sig=PVfKLqTcKz2BnruK5Ibw6P27QWum7Gd3GxwvlWucElk%3D[0m
Thought:[32;1m[1;3m```json
{
    "action": "Final Answer",
    "action_input": "Here is the image you requested: [Mountain and Stream](https://oaidalleapiprodscus.blob.core.windows.net/private/org-dN8AExG0uBkDqJqA7CbNq3Q5/user-n0EINDNhlbpFlQTFbfEKhnn2/img-XymEQV65Chg8YQm5lMcBZp9A.png?st=2024-01-23T11%3A25%3A02Z&se=2024-01-23T13%3A25%3A02Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-22T21%3A50%3A09Z&ske=2024-01-23T21%3A50%3A09Z&sks=b&skv=2021-08-06&sig=PVfKLqTcKz2BnruK5Ibw6P27QWum7Gd3GxwvlWucElk%3D)"
}
```[0m

[1m> Finished chain.[0m
'''

#print(extract_urls(ss)[1])