"""
与图像处理相关的工具函数
"""

import re
from IPython.display import display
import urllib.request
from PIL import Image


def display_url_image(url):
    # 从URL下载图像文件
    image_data = urllib.request.urlopen(url).read()

    # 使用PIL库加载图像并调整大小
    image = Image.open(urllib.request.urlopen(url))
    image.thumbnail((400, 400))  # 调整图像大小，使其适应输出区域

    # 使用display函数显示图像
    display(image)

def extract_urls_from_string(text):
    # 使用正则表达式匹配URL
    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(pattern, text)
    return urls