import gradio as gr

def toggle_buttons():
    if upload_button.properties["visible"]:
        upload_button.properties["visible"] = False
        clear_button.properties["visible"] = True
    else:
        upload_button.properties["visible"] = True
        clear_button.properties["visible"] = False

upload_button = gr.Button("Upload")
clear_button = gr.Button("Clear")
clear_button.properties["visible"] = False

iface = gr.Interface(
    fn=None,
    inputs=[upload_button, clear_button],
    outputs=None,
    title="Upload and Clear"
)
iface.launch(share=True)