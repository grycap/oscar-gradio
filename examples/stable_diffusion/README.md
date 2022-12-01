# Stable diffusion integrated with OSCAR and Gradio

## Stable diffusion

Stable diffusion is a deep learning IA that converts and generates an image from a natural language text description.

## Prerequisites

* Deploy an OSCAR cluster, and follow the deployment on [OSCAR documentation](https://docs.oscar.grycap.net/deploy-im-dashboard/). Remember that the cluster must have GPU support, so in OSCAR Parameters, put `Flag to add NVIDIA support` as True.

* Deploy [stable difussion](https://github.com/grycap/oscar/tree/master/examples/stable-diffusion) services with [OSCAR-CLI](https://docs.oscar.grycap.net/oscar-cli)

``` oscar-cli apply filename.yaml ```

## Explaining the code

### UI

This example needs text as input and images as output. Three components will be created.

* Textbox component where the input text will be introduced.
* Image component where the output images will be printed. This will have six instances.
* Button component will execute the services.

It needs to declare the action after clicking the button.

* Function that will be executed. In this case, the function is called `text_imgAsync`.
* Inputs parameter is an array with the variables of input components.
* Outputs parameter is an array with the variables of the output component.

```
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
```

### Communication with OSCAR cluster - Asynchrony call

This example has been implemented using an asynchronous way because the Stable-diffusion service requires too much time
that a synchronous call can not handle.
So the process starts uploading the input file into the input bucket. This will trigger the Stable diffusion service.
The process will be listening in the output bucket until the work is finished.
So, once the service has finished, a file will be uploaded to the output bucket.
And this event will download the final file into your actual folder.
This file is a zip file with six images inside it.
All the images will be extracted and printed in the web interface.

### Authentication

On the main page of [oscar-gradio repository](https://github.com/grycap/oscar-gradio#Authentication) there is a general explanation of the authentication. Here it will be explained in more detail. The function assigned by `auth` will be executed after the login process to verify your credentials.
This authentication will be made with the OSCAR cluster. A global object will be created to connect and interact with the OSCAR cluster.

### Environment variable

This Gradio app that uses the Stable diffusion service has two environmental variables. The first environment variable, `oscar_endpoint` contains where the OSCAR clúster deployed. And the second environment variable is `port`, it specifies in which port it will be deployed.

## Stable diffusion container works on your localhost

Change the variable `oscar_endpoint` to your endpoint OSCAR.
And try the Gradio app with the following command.
This command will create and run in localhost the Gradio app container that interacts with the cowsay OSCAR service.
Once the container is running, the web interface can be accessed in the `http://0.0.0.0:7000` direction.

```docker run -it -e oscar_endpoint='{oscar_endpoint}' -e port="7000" -p 7000:7000 ghcr.io/grycap/gradio_stable_diffusion```

## Deploy Gradio with Stable Diffusion

The Kubernetes file is already created. To make it work. Change the `oscar_endpoint` environment value to your OSCAR cluster:`spec.containers.env.value`. And add the subdomain in the Ingress component in the fields:`spec.tls.hosts`, `spec.tls.hosts.secretName` and `spec.rules.host`.
Then [pass the YAML file](https://github.com/grycap/oscar-gradio#pass-file) to the OSCAR cluster
and [connect it via ssh](https://github.com/grycap/oscar-gradio#connect-to-oscar-via-ssh).
Finally, apply the changes to Kubernetes.

``` kubectl apply -f deploy_gradio.yaml ```
