---
id: computing-software.cloud-infrastructure-engineering.kubernetes.windows-node-storage-smb-csi
name: windows-node-storage-smb-csi
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, windows-storage, smb-csi, csi-proxy, windows-nodes, azure-files, csi]
level: advanced
status: docs-checked
description: "Give Windows pods persistent and shared storage: SMB CSI driver with csi-proxy, credentials secrets, NTFS block disks, path rules, and the Linux-only options to avoid."
sources: ["https://github.com/kubernetes-csi/csi-driver-smb", "https://github.com/kubernetes-csi/csi-proxy", "https://kubernetes.io/docs/concepts/storage/windows-storage/", "https://learn.microsoft.com/en-us/azure/aks/azure-csi-files-storage-provision"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows node storage (SMB CSI)

## What works and what does not (Kubernetes Windows storage docs)
Volume plugin classes supported on Windows: FlexVolume (deprecated since 1.23) and CSI. In-tree plugins named for persistent storage on Windows: `azureFile` and `vsphereVolume`.

Not supported on Windows nodes:
- subPath mounts (only the whole volume), including subPath for Secrets
- host mount projection; read-only root filesystem (volumes still support `readOnly`)
- block device mapping (raw block volumes); memory as storage medium (`emptyDir.medium: Memory`)
- uid/gid and per-user permissions, `defaultMode` secret permissions
- NFS based storage
- expanding a mounted volume (resizefs)

## csi-proxy versus HostProcess
The SMB driver's Helm chart deploys the Windows node plugin with HostProcess containers by default (`windows.useHostProcessContainers: true`), and in that mode csi-proxy is not needed. If you turn that off, csi-proxy is required (the chart can deploy it with `windows.csiproxy.enabled=true`). Check the driver README for the supported Kubernetes and csi-proxy version table.

## Install SMB CSI
The chart repository is `https://raw.githubusercontent.com/kubernetes-csi/csi-driver-smb/master/charts` or `https://kubernetes-csi.github.io/csi-driver-smb` (use only one). `windows.enabled` defaults to true.
```bash
helm repo add csi-driver-smb https://kubernetes-csi.github.io/csi-driver-smb
helm repo update csi-driver-smb
helm install csi-driver-smb csi-driver-smb/csi-driver-smb --namespace kube-system
kubectl -n kube-system get daemonset csi-smb-node-win        # default Windows DaemonSet name (windows.dsName)
```

## Credentials and class
Bring your own Samba/SMB server. The secret holds `username` and `password` (`domain` optional).
```bash
kubectl create secret generic smbcreds -n kube-system \
  --from-literal username='<user>' --from-literal password='<password>'
```
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: smb}
provisioner: smb.csi.k8s.io
parameters:
  source: //<smb-server-address>/<share-name>
  csi.storage.k8s.io/provisioner-secret-name: smbcreds
  csi.storage.k8s.io/provisioner-secret-namespace: kube-system
  csi.storage.k8s.io/node-stage-secret-name: smbcreds
  csi.storage.k8s.io/node-stage-secret-namespace: kube-system
reclaimPolicy: Retain
volumeBindingMode: Immediate
```
`source` and the node-stage secret are mandatory; the provisioner secret is optional, and when it is given the driver creates a subdirectory named after the PV under `source`. `subDir` and `onDelete` (`delete`, `retain`, `archive`; default `delete`) are optional parameters. Mount options such as `uid`, `gid`, `dir_mode` and `file_mode` are Linux mount flags; do not use them for Windows nodes.

## Pod side
```yaml
spec:
  nodeSelector: {kubernetes.io/os: windows}
  containers:
  - name: app
    image: mcr.microsoft.com/windows/servercore:ltsc2022
    volumeMounts: [{name: data, mountPath: /data}]
  volumes:
  - name: data
    persistentVolumeClaim: {claimName: data}
```
Windows container images range from about 300 MB to over 10 GB, and the container `C:` drive reports 20 GB of virtual free space by default; keep logs and caches on volumes.

## Verify
```bash
kubectl get pvc data -o jsonpath='{.status.phase}'
kubectl exec <win-pod> -- powershell -c "New-Item /data/probe.txt -Force; Get-ChildItem /data"
```

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) and csi-driver-smb docs (2026-10-24). Confirmed: unsupported Windows storage features, Helm chart defaults (windows.enabled, useHostProcessContainers, csi-smb-node-win), StorageClass parameters and which secrets are mandatory.

Method: documentation only; no commands were run.
