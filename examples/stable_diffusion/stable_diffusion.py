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
    print(uid)
    file=gro.callAsyncUuid(data,"txtimg/input","txtimg/output",uid)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove(file)
    return "./samples/00000.png", \
        "./samples/00001.png", "./samples/00002.png", "./samples/00003.png", \
        "./samples/00004.png", "./samples/00005.png","grid-0000.png"

def text_imgSync(text):
    data=bytes('"'+text+'"',"utf-8")
    file64=base64.b64encode(data)
    file=gro.callSync("txt-to-img-sync",file64,"stable_difussion.zip")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove(file)
    return "./samples/00000.png", \
        "./samples/00001.png", "./samples/00002.png", "./samples/00003.png", \
        "./samples/00004.png", "./samples/00005.png","grid-0000.png"



with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(label="text")
            inbtw3 = gr.Button("From Text to Image Sync")
            inbtw4 = gr.Button("From Text to Image Async")
        img = gr.Image(type="filepath")
        img0 = gr.Image(type="filepath")
        img1 = gr.Image(type="filepath")
        img2 = gr.Image(type="filepath")
        img3 = gr.Image(type="filepath")
        img4 = gr.Image(type="filepath")
        img5 = gr.Image(type="filepath")
        #inbtw2.click(fn=text_imgAsync,
        #        inputs= [text],
        #        outputs=[img5])    
        inbtw3.click(fn=text_imgSync,
                inputs= [text],
                outputs=[img,img0,img1,img2,img3,img4,img5])
        inbtw4.click(fn=text_imgAsync,
                inputs= [text],
                outputs=[img,img0,img1,img2,img3,img4,img5])            
demo.launch(server_name="0.0.0.0",server_port=int(os.environ['port']),auth=authorization)
