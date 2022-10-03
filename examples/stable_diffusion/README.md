# Stable diffusion integrate with OSCAR and Gradio

## Deploy the cluster

Follow the deployment on (OSCAR documentation)[https://docs.oscar.grycap.net/deploy-im-dashboard/]. Remember that the cluster must have GPU support in this case, so in OSCAR Parameters, put `Flag to add NVIDIA support` as True.

## Deploy the service

To deploy the service, use (OSCAR-CLI)[https://docs.oscar.grycap.net/oscar-cli] with the example of (stable-diffusion)[https://github.com/grycap/oscar/tree/master/examples/stable-diffusion]

``` oscar-cli apply filename.yaml ```

## Deploy Gradio

Change the oscar_endpoint environment value to your OSCAR cluster:`spec.containers.env.value`. Add the subdomain in the ingress component in the fields:`spec.tls.hosts`, `spec.tls.hosts.secretName` and `spec.rules.host`. Apply the changes to Kubernetes.

``` kubectl apply -f deploy_gradio.yaml ```