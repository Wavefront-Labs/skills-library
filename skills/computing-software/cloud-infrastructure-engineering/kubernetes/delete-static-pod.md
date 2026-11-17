---
id: computing-software.cloud-infrastructure-engineering.kubernetes.delete-static-pod
name: delete-static-pod
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, delete-static-pod, mirror-pod, static-pod]
level: practitioner
status: docs-checked
description: "Delete a static pod correctly by removing its manifest on the owning node, since kubectl delete only removes the mirror pod, which immediately comes back."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/#dynamic-addition-and-removal-of-static-pods", "https://kubernetes.io/docs/concepts/workloads/pods/static-pods/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/types/pod_update.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting a static pod

## Why kubectl delete does not work
```bash
kubectl delete pod static-web-node01
kubectl get pod static-web-node01      # back within seconds
```
The kubelet owns static pods; the API object is only a mirror. Deleting the mirror makes the
kubelet recreate it. The container never stopped.

## Find the node and file
```bash
kubectl get pod static-web-node01 -o jsonpath='{.spec.nodeName}{"\n"}'
kubectl get pod static-web-node01 -o jsonpath='{.metadata.annotations.kubernetes\.io/config\.source}{"\n"}'   # prints "file" (or "http" for staticPodURL)
ssh node01 'sudo grep -i staticPodPath /var/lib/kubelet/config.yaml'
ssh node01 'sudo grep -l "name: static-web" /etc/kubernetes/manifests/*'
```
The annotation names the source type, not the file. The file name need not match the pod name; grep for it.

## Remove
```bash
ssh node01 'sudo mv /etc/kubernetes/manifests/static-web.yaml /root/'
```
Moving (not deleting) keeps a copy for rollback. The kubelet stops the containers and removes
the mirror pod.

## Verify
```bash
kubectl get pods -A | grep static-web      # gone
ssh node01 'sudo crictl ps -a | grep static-web'   # no running container
```

## Control-plane caution
On control-plane nodes the same directory holds kube-apiserver, etcd, controller-manager and
scheduler manifests. Moving `kube-apiserver.yaml` out takes the API down on that node: this is
also the standard way to restart a control-plane component, so double-check the file name.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: `kubectl delete` of the mirror pod leaves the static pod running and the kubelet recreates the mirror; moving the manifest out of the directory and waiting stops the container (the docs use `sleep 20` and `crictl ps`); the `kubernetes.io/config.source` annotation exists with values `file`, `http` and `api` (source). Wrong and fixed: the annotation holds the source type, not the file path.

Method: documentation only; no commands were run.
