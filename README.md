# User Interfaces with Gradio for AI model inference in OSCAR services

[Gradio](https://gradio.app) is a Python library for building user web interfaces for Machine Learning (ML) applications. [OSCAR](https://oscar.grycap.net) is an open-source serverless computing platform for data-processing applications, that can be used to deploy AI/ML models for inference.

This repository describes how to create Gradio apps for OSCAR services. 

## Prerequisites

Each Gradio app needs to be adapted to the specific OSCAR service that will execute the pre-trained AI/ML model that is encapsulated as a Docker container image.

First, deploy an OSCAR cluster and then, an OSCAR service: 

### Deploy an OSCAR cluster
    To deploy in [localhost](https://docs.oscar.grycap.net/local-testing/) use the next command:

    ``` sh
    curl -sSL http://go.oscar.grycap.net | bash
    ```

    Also, OSCAR can be deployed with the [Infraastructure Manager (IM)](https://docs.oscar.grycap.net/deploy-im-dashboard/)

### Deploy an OSCAR service
    OSCAR services can be deployed with [OSCAR-CLI](https://docs.oscar.grycap.net/oscar-cli/) with the command `apply` or using the [UI](https://docs.oscar.grycap.net/usage/#deploying-services)

    ``` sh
    oscar-cli apply FDL_FILE
    ```

## Create your UI

If you are using an example that already exists, such as the ones in the `examples` folder, you can skip this part. Otherwise, first create a demo in localhost with [the components that Gradio provides](https://gradio.app/docs). Each service will need a different component depending on the inputs and outputs of the services. Take a look in the examples folder for assistance building your UI. To connect to the OSCAR services, use the [OSCAR Python library](https://pypi.org/project/oscar-python/).

### Build Docker

Once the local demo works, changes need to be introduced to the Gradio app. The OSCAR cluster endpoint must be an environment variable with the value assigned at deployment time. Also, change the parameters of the [.launch()](https://gradio.app/docs/#launch) function by introducing `server_name` with the value `0.0.0.0`. The last change is the `server_port` variable as an environment variable `int(os.environ['port'])`.

### Authentication

By default, Gradio apps are not protected with user credentials. Therefore, the `auth` parameter to the [.launch()](https://gradio.app/docs/#launch) method will create an authentication process.

In the `auth` parameter, assign a function that will be executed in the login process. This authentication can be made with the OSCAR cluster. For more information, check the code samples in the `examples` folder.

## Try an example UI

Once the OSCAR cluster is up and running and the Docker image for the Gradio application is already built, verify that it works in `localhost` with the following command:

```sh
docker run -it -e oscar_endpoint='{oscar_endpoint}' -e port="7000" -p 7000:7000 ghcr.io/grycap/{image_name}
```

## Deployment  in Kubernetes

Once the containerised Gradio app works, it is time to deploy it in the Kubernetes cluster.

### Apply the YAML file

Deploy the YAML file to the Kubernetes cluster.

``` kubectl apply -f deploy_gradio.yaml ```

### Structure

This final section explains the minimum structure required for the YAML that is deployed in Kubernetes for the Gradio app. It contains three components. A Deployment is a component that creates pods. In case a pod fails, it will be replaced. A Service, is the component User interfaces with Gradio for the AI model inference in OSCAR services

Then create a Deployment with a container from the Docker image and the required environment variables. It needs two environment variables to expose the service: the OSCAR endpoint and the port. Also, expose the container on a certain port.

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {pod_name}
  labels:
    app: {pod_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {pod_name}
  template:
    metadata:
        labels:
          app: {pod_name}
    spec:
      containers:
        - name: {pod_name}
          image: ghcr.io/grycap/{image_name}
          env:
            - name: oscar_endpoint
              value: {oscar_endpoint}
            - name: port
              value: "30001"
          ports:
            - name: web
              containerPort: 30001
              protocol: TCP
```

Create a Service to have permanent access to the containers. This service will aim at the container port called `web`.

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: service-{pod_name}  
spec:
  selector:
    app: {pod_name}
  ports:
    - protocol: TCP
      port: 9000
      name: service-port
      targetPort: 30001
  type: NodePort
```

Finally, create an Ingress resource to expose the service from outside of the cluster.
If it uses HTTPS protocol, add `nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"` into the annotations of the ingress component.

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-{pod_name}
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - {sub_domain}.{public_hostname}
    secretName: {sub_domain}.{public_hostname}
  rules:
  - host: {sub_domain}.{public_hostname}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service-{pod_name}
            port:
              number: 9000
```

## Configure the DNS

The Docker with the Gradio app is probably deployed, but it cannot be accessed via the web. So, use a DNS service cloud like Amazon Route 53, Azure DNS or Google Cloud DNS to link the public IP of the front machine of the OSCAR cluster (the one that does not start with the prefix `10.`) with the subdomain you have been created in the DNS service.