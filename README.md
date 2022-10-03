# Deploy Gradio in OSCAR

So to abstract the infrastructure from the user. Execute services and see the results immediately in an easy way with a graphical user interface.

Use (Gradio)[https://gradio.app/] to create a demo user interface. Each example fits with an OSCAR service or OSCAR workflow. Some of them are in the (OSCAR)[https://github.com/grycap/oscar/tree/master/examples] repository.

## Create demo in local

Create a demo in localhost with (the components that Gradio provides)[https://gradio.app/docs]. Each use case or service will need a different component.

## Build Docker

Once the local demo works, make some changes to the file. OSCAR cluster end-point variable must be an environment variable with the value assigned in deploy time. Change the parameters of the (.launch())[https://gradio.app/docs/#launch] function by introducing `server_name` with the value `0.0.0.0`, `server_port` as a environment variable and the `auth` parameter to create an authentication process. This authentication could be the same as the OSCAR cluster. When all those changes are made, build the Docker. Try that works with the command:

```docker run -it -e oscar_endpoint='{oscar_endpoint}' -e port="7000" -p 7000:7000 ghcr.io/grycap/{image_name}```

## Deploy in Kubernetes

Once the Docker it is running. Expose the demo with a permanent link. Create a pod with the docker image. Create a service that aims at the pod. Moreover, create an ingress to access from the outside of Kubernetes.


For more information on the Gradio integration with (OSCAR)[https://oscar.grycap.net/], visit our (blog)[https://oscar.grycap.net/blog/] and (Gradio entry)[https://oscar.grycap.net/blog/visualize-oscar-service-with-gradio].# oscar-gradio
