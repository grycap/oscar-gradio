import gradio as gr
import base64
import os
import zipfile
import json 
from gradio_oscar import gradiooscar
import uuid

baseurl=os.environ['oscar_endpoint']
ssl= True   

def authorization(login, password):
    global gro 
    gro = gradiooscar(baseurl,login,password,ssl)
    return gro.getLogin()


def text_imgAsync(data):
    uid=str(uuid.uuid4())
    file=gro.callAsyncUuid(data,"stable-diffusion/in","stable-diffusion/out",uid)
    os.rename(uid, uid+".zip")
    with zipfile.ZipFile(uid+".zip", 'r') as zip_ref:
        zip_ref.extractall(".")
    return "./output-1.png", \
        "./output-2.png", "./output-3.png", "./output-4.png", \
        "./output-5.png", "./output-6.png"



with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(label="text")
            inbtw4 = gr.Button("From Text to Image")
        img = gr.Image(type="filepath")
        img0 = gr.Image(type="filepath")
        img1 = gr.Image(type="filepath")
        img2 = gr.Image(type="filepath")
        img3 = gr.Image(type="filepath")
        img4 = gr.Image(type="filepath")
        inbtw4.click(fn=text_imgAsync,
                inputs= [text],
                outputs=[img,img0,img1,img2,img3,img4])            
demo.launch(server_name="0.0.0.0",server_port=int(os.environ['port']),auth=authorization)
