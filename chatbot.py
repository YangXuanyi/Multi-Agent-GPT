import gradio as gr
from PIL import Image
import numpy as np

def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    img = Image.open('./Imgs/lena.jpeg')
    return greeting, img

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "image"],
)
demo.launch()
