"""
图像内容理解工具, 在这里BLIP模型, 目前该模型已被huggingface集成
具体介绍网址为: https://huggingface.co/Salesforce/blip-image-captioning-large

在代码首次运行时, 程序会默认访问huggingface并下载BLIP模型的相关文件至系统默认处
如果想本地部署并访问BLIP, 请到对应网址手动下载并配置模型
"""

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageCaption():
    def __init__(self):
        """
        实例化BLIP图像内容理解模型
        """
        # 线上调用BLIP的方法
        # self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        # self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

        #线下部署BLIP, 将BLIP模型的所有文件下载至本地文件夹
        self.processor = BlipProcessor.from_pretrained("/root/autodl-tmp/Multi-Agent-GPT/Models/BLIP")
        self.model = BlipForConditionalGeneration.from_pretrained("/root/autodl-tmp/Multi-Agent-GPT/Models/BLIP").to("cuda")
    
    def infer_image(self, image, text=None):
        """
        根据问题text对图像内容进行理解
        """
        if text==None:
            # unconditional image captioning
            inputs = self.processor(image, return_tensors="pt").to("cuda")
            out = self.model.generate(**inputs)
        else:
            # conditional image captioning
            inputs = self.processor(image, text, return_tensors="pt").to("cuda")
            out = self.model.generate(**inputs)
        
        #aqurie result
        result = self.processor.decode(out[0], skip_special_tokens=True)
        
        return result
    
    
    
# test
# imagecaption = ImageCaption()
# test = None
# image = Image.open("/root/autodl-tmp/Multi-Agent-GPT/Imgs/image.jpg")
# result = imagecaption.infer_image(image,test)
# print(result)



