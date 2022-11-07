# User interfaces with Gradio for AI model inference in OSCAR services

## Prerequisites

Each Gradio app needs to be adapted to specific services.
But first, it needs to deploy an OSCAR clúster with the services.

* Deploy OSCAR
    To deploy in [localhost](https://docs.oscar.grycap.net/local-testing/) use the next command:

    ``` sh
    curl -sSL http://go.oscar.grycap.net | bash
    ```

    Also, OSCAR can be deployed with [IM](https://docs.oscar.grycap.net/deploy-im-dashboard/)

* Deploy services
    OSCAR services can be deployed with [OSCAR-CLI](https://docs.oscar.grycap.net/oscar-cli/) with the command `apply` or using the [UI](https://docs.oscar.grycap.net/usage/#deploying-services)

    ``` sh
    oscar-cli apply FDL_FILE
    ```

## Create your UI

If you are using an example that already exists, skip that part. First, create a demo in localhost with [the components that Gradio provides](https://gradio.app/docs). Each service will need a different component depending on the inputs and outputs of the services. Take a look in the examples folder for help building your UI. To connect to OSCAR services, use [OSCAR python library](https://pypi.org/project/oscar-python/)

### Build Docker

Once the local demo works, make some changes to the Gradio app. OSCAR cluster endpoint variable must be an environment variable with the value assigned in deploy time. Also, change the parameters of the [.launch()](https://gradio.app/docs/#launch) function by introducing `server_name` with the value `0.0.0.0`.The last change is the `server_port` variable as an environment variable `int(os.environ['port'])`.

### Authentication

Gradio apps are insecure because everybody can use them without credentials.
So the `auth` parameter to the [.launch()](https://gradio.app/docs/#launch) method will create an authentication process.
In the `auth` parameter, assign a function that will execute in the login process.
This authentication could be made with the OSCAR cluster. For more information, check an example.

## Try an example UI

If all the services required are already deployed, and the Docker is already built. Try that the Gradio app works in a localhost with the command:

```docker run -it -e oscar_endpoint='{oscar_endpoint}' -e port="7000" -p 7000:7000 ghcr.io/grycap/{image_name}```

## Deploy in Kubernetes

Once the Docker works perfectly, it is time to expose the demo in a permanent link using Kubernetes.

### Cluster in remote

Probably your Kubernetes cluster is located in a remote machine. So first, you must pass the YAML file that contains the structure to deploy on Kubernetes. Then connect to the remote machine via ssh.

#### Pass file

Use the `scp` command to pass the Kubernetes YAML file to your remote machine.

```
scp -i key.pem /local/path/deploy_gradio.yaml root@<public-domain>:/root
```

#### Connect to OSCAR via ssh

Use the `ssh` command to connect to your remote machine.

```
ssh -i key.pem root@<public-domain>
```

### Apply the file

Once you have access to the machine where the Gradio app will be deployed, and it has the YAML file inside, you must apply the YAML file to Kubernetes.

``` kubectl apply -f deploy_gradio.yaml ```

### Structure

This final section explains the minimum structure that is deployed in Kubernetes with Gradio app. The structure contains three components. A Deployment is a component that creates pods. In case a pod fails, it will be replaced. A Service, it is the compone# User interfaces with Gradio for AI model inference in OSCAR services

Then create a Deployment inside the Deployment and create a container with the docker image and the environment variables. It needs two environment variables to expose the service: the OSCAR endpoint and the port. Also, create a port to expose the container with the same value as the variable.

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

Finally, create an Ingress resource to expose the service from the outside.
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

The Docker with the Gradio app is probably deployed, but it can not be accessed via the web.
So, use a DNS service cloud like route53, Azure DNS or Google Cloud DNS to link the public IP
of the front machine of the OSCAR cluster (the one that does not start with the prefix `10.`) with the subdomain you have been deployed.