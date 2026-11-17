---
id: computing-software.cloud-infrastructure-engineering.kubernetes.create-static-pod-on-node
name: create-static-pod-on-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, create-static-pod, staticpodpath, mirror-pod]
level: practitioner
status: docs-checked
description: "Create a static pod on a specific node: find staticPodPath, generate the manifest, place it, and confirm the mirror pod; the common CKA task."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/static-pods/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a static pod

## 1. Find the manifest directory on the target node
```bash
ssh node01
sudo grep -i staticPodPath /var/lib/kubelet/config.yaml       # usually /etc/kubernetes/manifests
ps -o args= -C kubelet | tr ' ' '\n' | grep -E 'config|pod-manifest-path'   # if not default
```
If `staticPodPath` is missing, add it to the KubeletConfiguration and restart the kubelet. (The
`--pod-manifest-path` kubelet flag is the deprecated alternative.)

## 2. Generate the manifest (from any machine with kubectl)
```bash
kubectl run static-web --image=nginx --port=80 --dry-run=client -o yaml > static-web.yaml
```
Edit if needed (resources, command). Do not set `nodeName`; the kubelet that reads the file
owns the pod.

## 3. Place it
```bash
sudo cp static-web.yaml /etc/kubernetes/manifests/
```
The kubelet scans the directory periodically (`fileCheckFrequency`, default 20s; on Linux the
source also uses an inotify watch) and starts the pod.

## 4. Verify
```bash
kubectl get pods -A -o wide | grep static-web       # name is static-web-node01
sudo crictl ps | grep static-web                    # on the node
```
The API object is a mirror pod: name suffixed with the node name, annotation
`kubernetes.io/config.mirror`, and an ownerReference to the Node.

## Gotchas
- Change a static pod by editing its manifest file; the mirror pod is only a read-only view.
- The kubelet processes every file in the directory that does not start with a dot, whatever the
  extension, so a `.bak` copy or an editor swap file is read as a manifest. Edit outside the
  directory and copy in.
- A static pod's spec cannot refer to other API objects such as ServiceAccounts, ConfigMaps or
  Secrets, and static pods do not support ephemeral containers.
- Set `metadata.namespace` if the pod should not land in `default`.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: `staticPodPath` in the kubelet configuration (and the deprecated `--pod-manifest-path`), that files starting with a dot are ignored while every other file is read, the default `fileCheckFrequency` of 20s and the inotify watcher (source `file_linux.go`), mirror pod naming `<name>-<node>`, the `kubernetes.io/config.mirror` annotation and the Node ownerReference (source `mirror_client.go`), and that static pods cannot refer to ServiceAccounts, ConfigMaps or Secrets. Removed as unconfirmed: the pinned nginx tag and the claim about `kubectl edit` on the mirror pod.

Method: documentation only; no commands were run.
