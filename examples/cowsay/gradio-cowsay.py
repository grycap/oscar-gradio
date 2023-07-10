import gradio as gr
import json
from oscar_python.client import Client
import base64
import os 
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

baseurl= os.environ['oscar_endpoint']
if os.environ['ssl'] == "True":
    ssl_verify=True
else:
    ssl_verify=False
port=int(os.environ['port'])

def authentication(login,password):
    global client
    client = Client(id="cluster-id",endpoint=baseurl, user=login, password=password, ssl=ssl_verify)
    info = requests.get(baseurl+"/system/info", auth=HTTPBasicAuth(login, password), verify=ssl_verify)
    try:
        info = client.get_cluster_info()
    except Exception as err:
        print("Failed with: ", err)
    if info.status_code == 200:
        return True
    else:
        return False

def cowsay(text_input):
    service = client.get_service("cowsay") # returns an http response
    try:
        variable=json.loads(service.text)['environment']['Variables']['INPUT_TYPE']
    except:
        variable="not"
    try:
        json.loads(text_input)
        json_parse=True
    except:
        json_parse=False
    if(variable == 'json' and json_parse):
        info = client.run_service("cowsay",input=text_input)
    elif(variable == 'json' and not json_parse):
        input='{"message": "'+text_input+'"}'
        info = client.run_service("cowsay",input=input)
    else:
        message_bytes = text_input.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        info = client.run_service("cowsay",input=base64_message)
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
demo.launch(server_name="0.0.0.0",server_port=port,auth=authentication)
