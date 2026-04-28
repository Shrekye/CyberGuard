```
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
deployment.apps/nginx created
deployment.apps/nginx scaled
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl create deployment cyberguard \
  --image=ghcr.io/shrekye/cyberguard:latest
deployment.apps/cyberguard created
                                                                                                                                                                                                                                       
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl scale deployment cyberguard --replicas=5
deployment.apps/cyberguard scaled
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl expose deployment cyberguard \
  --type=NodePort \
  --port=5000
service/cyberguard exposed
                                                                                                                                                                                                                                                                                                                                       
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl expose deployment nginx --type=NodePort --port=80
service/nginx exposed
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl get pods                                         
kubectl get services
NAME                         READY   STATUS    RESTARTS   AGE
cyberguard-b9ddc6c8c-2hztp   1/1     Running   0          57s
cyberguard-b9ddc6c8c-4qmjt   1/1     Running   0          52s
cyberguard-b9ddc6c8c-kcl8p   1/1     Running   0          52s
cyberguard-b9ddc6c8c-lh8qz   1/1     Running   0          52s
cyberguard-b9ddc6c8c-q4p5r   1/1     Running   0          52s
nginx-56c45fd5ff-2plsv       1/1     Running   0          60s
nginx-56c45fd5ff-f9j86       1/1     Running   0          60s
nginx-56c45fd5ff-jfwd7       1/1     Running   0          60s
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
cyberguard   NodePort    10.96.118.100    <none>        5000:30359/TCP   42s
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          31m
nginx        NodePort    10.109.228.237   <none>        80:32009/TCP     3s



┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl set image deployment/cyberguard \
cyberguard=ghcr.io/shrekye/cyberguard:main
deployment.apps/cyberguard image updated
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl rollout restart deployment cyberguard
deployment.apps/cyberguard restarted



┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ kubectl get pods   
kubectl get services
NAME                         READY   STATUS    RESTARTS   AGE
cyberguard-7679bdcbf-lfnqf   1/1     Running   0          52s
cyberguard-7679bdcbf-ndwm2   1/1     Running   0          56s
cyberguard-7679bdcbf-rrhs7   1/1     Running   0          56s
cyberguard-7679bdcbf-wlmqt   1/1     Running   0          52s
cyberguard-7679bdcbf-xzfsz   1/1     Running   0          56s
nginx-56c45fd5ff-2plsv       1/1     Running   0          7m59s
nginx-56c45fd5ff-f9j86       1/1     Running   0          7m59s
nginx-56c45fd5ff-jfwd7       1/1     Running   0          7m59s
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
cyberguard   NodePort    10.96.118.100    <none>        5000:30359/TCP   7m41s
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          38m
nginx        NodePort    10.109.228.237   <none>        80:32009/TCP     7m2s



┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ minikube service nginx
┌───────────┬───────┬─────────────┬───────────────────────────┐
│ NAMESPACE │ NAME  │ TARGET PORT │            URL            │
├───────────┼───────┼─────────────┼───────────────────────────┤
│ default   │ nginx │ 80          │ http://192.168.49.2:32009 │
└───────────┴───────┴─────────────┴───────────────────────────┘
🎉  Ouverture du service default/nginx dans le navigateur par défaut...
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~/Téléchargements/kube/CyberGuard]
└─$ minikube service cyberguard
┌───────────┬────────────┬─────────────┬───────────────────────────┐
│ NAMESPACE │    NAME    │ TARGET PORT │            URL            │
├───────────┼────────────┼─────────────┼───────────────────────────┤
│ default   │ cyberguard │ 5000        │ http://192.168.49.2:30359 │
└───────────┴────────────┴─────────────┴───────────────────────────┘
🎉  Ouverture du service default/cyberguard dans le navigateur par défaut...

```

```
┌──(shrekye㉿anon)-[~]
└─$ kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > nginx-deployment.yaml                     
kubectl scale deployment nginx --replicas=3 --dry-run=client -o yaml >> nginx-deployment.yaml
kubectl expose deployment nginx --type=NodePort --port=80 --dry-run=client -o yaml > nginx-service.yaml

kubectl create deployment cyberguard --image=ghcr.io/shrekye/cyberguard:latest --dry-run=client -o yaml > cyberguard-deployment.yaml
kubectl scale deployment cyberguard --replicas=5 --dry-run=client -o yaml >> cyberguard-deployment.yaml
kubectl expose deployment cyberguard --type=NodePort --port=5000 --dry-run=client -o yaml > cyberguard-service.yaml


┌──(shrekye㉿anon)-[~]
└─$ cat cyberguard-deployment.yaml  
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: cyberguard
  name: cyberguard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cyberguard
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cyberguard
    spec:
      containers:
      - image: ghcr.io/shrekye/cyberguard:latest
        name: cyberguard
        resources: {}
status: {}
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "3"
  creationTimestamp: "2026-04-27T14:26:25Z"
  generation: 4
  labels:
    app: cyberguard
  name: cyberguard
  namespace: default
  resourceVersion: "6510"
  uid: c21d07bf-59bd-4b55-bcdf-ec52bf733dec
spec:
  progressDeadlineSeconds: 600
  replicas: 5
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: cyberguard
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      annotations:
        kubectl.kubernetes.io/restartedAt: "2026-04-27T16:33:24+02:00"
      labels:
        app: cyberguard
    spec:
      containers:
      - image: ghcr.io/shrekye/cyberguard:main
        imagePullPolicy: Always
        name: cyberguard
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 5
  conditions:
  - lastTransitionTime: "2026-04-27T14:26:25Z"
    lastUpdateTime: "2026-04-27T14:33:32Z"
    message: ReplicaSet "cyberguard-7679bdcbf" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  - lastTransitionTime: "2026-04-28T12:07:57Z"
    lastUpdateTime: "2026-04-28T12:07:57Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  observedGeneration: 4
  readyReplicas: 5
  replicas: 5
  terminatingReplicas: 0
  updatedReplicas: 5
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~]
└─$ cat cyberguard-service.yaml   
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: cyberguard
  name: cyberguard
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    app: cyberguard
  type: NodePort
status:
  loadBalancer: {}
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~]
└─$ cat nginx-service.yaml 
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: nginx
  name: nginx
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx
  type: NodePort
status:
  loadBalancer: {}
                                                                                                                                                                                                                                            
┌──(shrekye㉿anon)-[~]
└─$ cat nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2026-04-27T14:26:22Z"
  generation: 2
  labels:
    app: nginx
  name: nginx
  namespace: default
  resourceVersion: "6528"
  uid: 722570bd-5cc0-4d9c-b552-50fc2259bf89
spec:
  progressDeadlineSeconds: 600
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: nginx
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 3
  conditions:
  - lastTransitionTime: "2026-04-27T14:26:22Z"
    lastUpdateTime: "2026-04-27T14:26:31Z"
    message: ReplicaSet "nginx-56c45fd5ff" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  - lastTransitionTime: "2026-04-28T12:07:59Z"
    lastUpdateTime: "2026-04-28T12:07:59Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  observedGeneration: 2
  readyReplicas: 3
  replicas: 3
  terminatingReplicas: 0
  updatedReplicas: 3

┌──(shrekye㉿anon)-[~]
└─$ kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
kubectl apply -f cyberguard-deployment.yaml
kubectl apply -f cyberguard-service.yaml

┌──(shrekye㉿anon)-[~]
└─$ kubectl create configmap nginx-proxy-config --from-literal=default.conf='
server {
    listen 80;
    
    location / {
        proxy_pass http://cyberguard:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Désactiver la mise en cache pour le développement
        proxy_buffering off;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Health check endpoint
    location /nginx-health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
'

┌──(shrekye㉿anon)-[~]
└─$ kubectl rollout restart deployment nginx

┌──(shrekye㉿anon)-[~]
└─$ kubectl create configmap nginx-proxy-config \
  --from-literal=default.conf='server { listen 80; location / { proxy_pass http://cyberguard:5000; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; proxy_buffering off; proxy_connect_timeout 30s; proxy_send_timeout 30s; proxy_read_timeout 30s; } location /nginx-health { access_log off; return 200 "healthy\n"; add_header Content-Type text/plain; } }' \
  --dry-run=client -o yaml > nginx-conf.yaml

┌──(shrekye㉿anon)-[~]
└─$ cat nginx-conf.yaml      
apiVersion: v1
data:
  default.conf: server { listen 80; location / { proxy_pass http://cyberguard:5000;
    proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header
    X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto
    $scheme; proxy_buffering off; proxy_connect_timeout 30s; proxy_send_timeout 30s;
    proxy_read_timeout 30s; } location /nginx-health { access_log off; return 200
    "healthy\n"; add_header Content-Type text/plain; } }
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: nginx-proxy-config

┌──(shrekye㉿anon)-[~]
└─$ kubectl rollout restart deployment nginx

```