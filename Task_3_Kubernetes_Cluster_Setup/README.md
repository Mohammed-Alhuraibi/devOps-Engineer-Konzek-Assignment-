# Kubernetes Cluster Setup

This guide explains how to set up a Kubernetes cluster, deploy a simple Python HTTP server application, and expose it via an Ingress controller for load balancing and demonstrating rolling updates. The instructions are tailored for a local Kind (Kubernetes in Docker) cluster setup.

---

## Prerequisites

- Docker installed on your machine.
- `kubectl` command-line tool installed.
- `kind` (Kubernetes in Docker) installed.

---

## Steps

### 1. Create a Kind Cluster

Make sure you don't have any old kind cluster by running.

```bash
kind delete cluster
```

Now create a Kind cluster using the configuration file `kind_config.yaml`:

```bash
kind create cluster --config kind_config.yaml
```

Set the context to the newly created Kind cluster:

```bash
kubectl cluster-info --context kind-kind
```

---

### 2. Install the Ingress Controller

Install the Ingress-NGINX controller into the cluster:

```bash
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
```

This will create a namespace `ingress-nginx` and install the necessary resources. Verify the installation:

```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

---

### 3. Deploy the Application

All necessary Kubernetes manifests (`deployment.yaml`, `service.yaml`, and `ingress.yaml`) are located in the root folder of this project. Apply these manifests to the cluster:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

All resources will be deployed in the default namespace.


Access [localhost](http://localhost).

---

### 4. Demonstrating Rolling Updates

To demonstrate rolling updates, you can switch between two versions of the Python HTTP server image:

- Current version: `alhuraibisaeed/simple-http-server:latest`
- Older version: `alhuraibisaeed/simple-http-server:old`


#### Steps for Rolling Update:

1. Update the image in the `deployment.yaml` file:

   ```yaml
   spec:
     containers:
     - name: simple-http-server
       image: alhuraibisaeed/simple-http-server:old
   ```

2. Apply the updated deployment:

   ```bash
   kubectl apply -f deployment.yaml
   ```


3. Verify the update progress:

   ```bash
   kubectl rollout status deployment/simple-http-server
   ```

> **Important:** Wait until all old pods are terminated and new ones are running.


The older version displays the additional text:

```
****** I'M AN OLD IMAGE ******
```

4. Access the application again at [localhost](http://localhost). to confirm the update. The old image will display the additional text mentioned above.

5. To roll back to the previous image version just run,
```bash
kubectl rollout undo deployment/simple-http-server
```

6. Access the application again at [localhost](http://localhost) to confirm the update.

#### Check Load Balancing

To verify load balancing, keep refreshing the page at [localhost](http://localhost). The displayed hostname will change as traffic is routed to different replicas.

---


## Additional Notes

- The Python HTTP server image is hosted publicly on Docker Hub.
- The Ingress controller simplifies load balancing by handling traffic routing.

Feel free to modify the deployment, service, and ingress configurations as needed for your environment!
