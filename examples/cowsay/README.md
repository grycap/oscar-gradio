# cowsay integrated with OSCAR and Gradio

## Cowsay

cowsay program generates an ASCII art picture of a cow with a message.

## Prerequisites

* Deploy an OSCAR cluster, and follow the deployment on [OSCAR documentation](https://docs.oscar.grycap.net/deploy-im-dashboard/). 

* Deploy [cowsay](https://github.com/grycap/oscar/tree/master/examples/cowsay) services with [OSCAR-CLI](https://docs.oscar.grycap.net/oscar-cli)

``` oscar-cli apply cowsay.yaml ```

## Explaining the code

### UI

This example needs three components.

* Textbox component where the input text will be introduced.
* Textbox component where the output text will be shown.
* Button component will execute the services.

```
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="input text")
            inbtw4 = gr.Button("From Text to cowsay")
        text_output = gr.Textbox(label="output text")
        inbtw4.click(fn=cowsay,
                inputs= [text_input],
                outputs=[text_output])            
```

### Communication with OSCAR cluster - Synchronous call

Gradio builds an interface web with Python.
So, import the Python library [oscar-python](https://pypi.org/project/oscar-python) to interact with the OSCAR cluster.
In this case, an environment variable indicates if the input should be in JSON format.
So first, invoke the `get_service` function to get the information of the service and then parse the response of the service information.
After that, parse the input text. Now appear three possibilities:

* Call the service if the service needs JSON and the input text is in JSON format.
* Change the input if the service needs JSON and the input text is not in JSON format.
* If the service does not need JSON input, call the service.

Finally, return the service response.

```
def cowsay(text_input):
    service = client.get_service("cowsay") # returns an HTTP response
    try:
        variable=json.loads(service.text)['environment']['Variables']['INPUT_TYPE']
    except ValueError:
        variable="not"
    try:
        JSON.loads(text_input)
        json_parse=True
    except ValueError:
        json_parse=False
    if(variable == 'JSON' and json_parse):
        info = client.run_service("cowsay",input=text_input)
    elif(variable == 'JSON' and not json_parse):
        input='{"message": "'+text_input+'"}'
        info = client.run_service("cowsay",input=input)
    else:
        info = client.run_service("cowsay",input=text_input)
    return info.text
```

### Authentication

On the main page of [oscar-gradio repository](https://github.com/grycap/oscar-gradio#Authentication) there is a general explanation of the authentication. Here it will be explained in more detail. The function assigned by `auth` will be executed after the login process to verify your credentials.
The authentication in this example will be made with the OSCAR cluster.
In the first step, a global variable of the OSCAR cluster client will be created. This variable will be invoked later from other functions.
Then to verify that the credentials are correct, the authentication process will call a function that provides information like `get_info_cluster`.
If it returns 200 in the status code, the password is correct and will grant access.

```
def authentication(login,password):
    global client
    client = Client("oscar-GPU-cluster",baseurl, login, password, True)
    info = client.get_cluster_info()
    if info.status_code == 200:
        return True
    else:
        return False
```

### Environment variable

This Gradio app that uses the cowsay service has two environmental variables. The first environment variable, `oscar_endpoint,` contains where the OSCAR cluster deployed. And the second environment variable is `port`, which specifies which port Gradio will be deployed.

## Cowsay container works on your localhost

Change the variable `oscar_endpoint` to your endpoint OSCAR.
And try the Gradio app with the following command.
This command will create and run in localhost the Gradio app container that interacts with the cowsay OSCAR service.
Once the container is running, the web interface can be accessed in the `http://0.0.0.0:7000` direction.

```docker run -it -e oscar_endpoint='{oscar_endpoint}' -e port="7000" -p 7000:7000 ghcr.io/grycap/gradio_cowsay```

## Deploy Gradio with cowsay

The Kubernetes file is already created. To make it work. Change the `oscar_endpoint` environment value to your OSCAR cluster:`spec.containers.env.value`.
And add the subdomain in the Ingress component in the fields:`spec.tls.hosts`, `spec.tls.hosts.secretName`, and `spec.rules.host`.
Then [pass the YAML file](https://github.com/grycap/oscar-gradio#pass-file) to the OSCAR cluster
and [connect it via ssh](https://github.com/grycap/oscar-gradio#connect-to-oscar-via-ssh).
Finally, apply the changes to Kubernetes.

``` kubectl apply -f deploy_gradio.yaml ```
