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
└─$ kubectl get pods
kubectl get services
NAME                         READY   STATUS    RESTARTS   AGE
cyberguard-b9ddc6c8c-2hztp   1/1     Running   0          21s
cyberguard-b9ddc6c8c-4qmjt   1/1     Running   0          16s
cyberguard-b9ddc6c8c-kcl8p   1/1     Running   0          16s
cyberguard-b9ddc6c8c-lh8qz   1/1     Running   0          16s
cyberguard-b9ddc6c8c-q4p5r   1/1     Running   0          16s
nginx-56c45fd5ff-2plsv       1/1     Running   0          24s
nginx-56c45fd5ff-f9j86       1/1     Running   0          24s
nginx-56c45fd5ff-jfwd7       1/1     Running   0          24s
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
cyberguard   NodePort    10.96.118.100   <none>        5000:30359/TCP   6s
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          30m
                                                                                                                                                                                                                                            
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