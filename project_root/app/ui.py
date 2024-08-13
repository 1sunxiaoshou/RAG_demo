import gradio as gr
import requests


def predict(message, history, file):
    # 发送文本请求
    if file:
        # 如果有文件，使用multipart/form-data发送
        files = {'file': open(file, 'rb')}
        response = requests.post('http://127.0.0.1:5001/chat_file?question=' + message, files=files)
        response_json = response.json()
    else:
        # 否则，使用JSON发送问题
        response = requests.post('http://127.0.0.1:5001/chat_file?question=' + message)
        response_json = response.json()

    # 确保文件被关闭
    if file:
        files['file'].close()

    return response_json


def vector_interface(file=None):
    headers = {"Content-Type": "multipart/form-data"}
    if file:
        files = {'file': open(file.name, 'rb')}
        response = requests.post('http://127.0.0.1:5001/vector', files=files)
        response_json = response.json()
        files['file'].close()  # 确保文件被关闭
    else:
        response_json = {"error": "No file provided"}

    return response_json


with gr.Blocks(title="RAG测试") as demo:
    with gr.Tab("Chat_Bot"):
        File = gr.File(label="附带文件", file_types=[".pdf", ".txt", ".docx", ".md", ".csv", ".json"],render=False)
        iface_chat = gr.ChatInterface(
            predict,
            chatbot=gr.Chatbot(height=540),
            textbox=gr.Textbox(placeholder="请询问家电相关的问题"),
            autofocus=True,
            additional_inputs=[File]
        )
    with gr.Tab("导入知识库"):
        iface_vector = gr.Interface(
            fn=vector_interface,
            inputs=gr.File(label="Upload File to Vector"),
            outputs="text",
            title="Vector Interface",
            description="选择文件导入到向量知识库"
        )

demo.launch()
