import gradio as gr
import json
import os
from oscar_python.client import Client

baseurl=os.environ['oscar_endpoint']

def authentication(login,password):
    global client
    client = Client("oscar-gpu-cluster",baseurl, login, password, True)
    info = client.get_cluster_info()
    if info.status_code == 200:
        return True
    else:
        return False

def cowsay(text_input):
    service = client.get_service("cowsay") # returns an http response
    try:
        variable=json.loads(service.text)['environment']['Variables']['INPUT_TYPE']
    except ValueError:
        variable="not"
    try:
        json.loads(text_input)
        json_parse=True
    except ValueError:
        json_parse=False
    if(variable == 'json' and json_parse):
        info = client.run_service("cowsay",input=text_input)
    elif(variable == 'json' and not json_parse):
        input='{"message": "'+text_input+'"}'
        info = client.run_service("cowsay",input=input)
    else:
        info = client.run_service("cowsay",input=text_input)
    return info.text



with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="input text")
            inbtw4 = gr.Button("From Text to cowsay")
        text_output = gr.Textbox(label="output text")
        inbtw4.click(fn=cowsay,
                inputs= [text_input],
                outputs=[text_output])            
demo.launch(server_name="0.0.0.0",server_port=int(os.environ['port']),auth=authentication)