# Web Application Deployment Troubleshooting Guide


## Prerequisites
- Docker
- kubectl
- kind

## Clone the repo and, inside the project folder, run the following instructions.

## Initial Problem Assessment

Make sure you don't have any kind cluster by running.

```bash
kind delete cluster
```

create the kind cluster then the problemtic deployment
```bash
kind create cluster --config kind_config.yaml
kubectl cluster-info --context kind-kind
kubectl apply -f problemtic_deployment.yaml
```

### 1. Check Deployment Status
```bash
$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
web-application   0/3     3            0           2m
```

Problem Indicator: Pods are created but not ready (0/3 available)

### 2. Check Pod Status
```bash
$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
web-application-7d9f4b4f8d-1x2y3   0/1     Pending   0          2m
web-application-7d9f4b4f8d-2a3b4   0/1     Pending   0          2m
web-application-7d9f4b4f8d-5c6d7   0/1     Pending   0          2m
```

Problem Indicator: Pods are stuck in Pending state

## Detailed Investigation

### 1. Check Node Resources
```bash
$ kubectl describe nodes
```

Findings:
```
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests   Limits
  --------           --------   ------
  cpu                100m (2%)  100m (2%)
  memory             50Mi (0%)  50Mi (0%)
```

Issue: Resource requests are too high for the cluster's capacity.

### 2. Check Pod Details
```bash
$ kubectl describe pod <pod-name>
```

Findings:
```
Warning  FailedScheduling  7s    default-scheduler  0/2 nodes are available: 1 Insufficient cpu, 1 Insufficient memory, 1 node(s)
```


## Step-by-Step Resolution

### 1. Fix Resource Allocation
- Problem: Over-allocated resources preventing pod scheduling.
- Solution: Update resource requests and limits to appropriate values.

```bash
$ kubectl edit deployment web-application
```

Change from:
```yaml
resources:
  requests:
    memory: "1000Gi"      # Over-allocated resources
    cpu: "100000m"
  limits:
    memory: "20000Gi"
    cpu: "200000m"
```

To:
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### 2. Fix Port Configuration
- Problem: Incorrect port configuration for nginx
- Solution: Update container port to 80

1. Update the container port:
```yaml
ports:
- containerPort: 80
```

2. Remove unnecessary NGINX_PORT environment variable:
```yaml
# Remove this environment variable
- name: NGINX_PORT
  value: "8080"
```

### 3. Secure Sensitive Information
- Problem: Database password in plain text.
- Solution: Create and use a Kubernetes Secret.

1. Create a Secret:
```bash
$ kubectl create secret generic web-app-secrets \
  --from-literal=db-password='secretpassword123'
```

2. Update the deployment to use the secret:
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: web-app-secrets
      key: db-password
```

## Verification Steps

### 1. Verify Pod Status
```bash
$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
web-application-9d8f7b6f5d-1a2b3   1/1     Running   0          2m
web-application-9d8f7b6f5d-4c5d6   1/1     Running   0          2m
web-application-9d8f7b6f5d-7e8f9   1/1     Running   0          2m
```

### 2. Verify Application Access
```bash
$ kubectl port-forward deployment/web-application 8080:80
```
Then access http://localhost:8080 in your browser or:
```bash
$ curl localhost:8080
```

### 3. Check Secret Usage
```bash
$ kubectl describe pods | grep -A 2 "Environment:"
```
Should show the secret reference instead of plain text password.

## Best Practices Learned
1. Right-size resource requests and limits based on actual application needs
2. Use appropriate container ports based on the application (80 for nginx)
3. Store sensitive information in Kubernetes Secrets
4. Remove unnecessary environment variables
5. Use `kubectl describe` to investigate scheduling issues
6. Monitor pod status and logs during troubleshooting

## Additional Notes
- Always backup your deployment configuration before making changes
- Consider using `kubectl rollout history` to track changes
- Use `kubectl rollout undo` if new changes cause issues
- Resource limits should be based on actual application monitoring data
