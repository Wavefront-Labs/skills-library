---
id: computing-software.cloud-infrastructure-engineering.kubernetes.configmap-creation-and-size-limits
name: configmap-creation-and-size-limits
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, configmap, kubectl-create-configmap, binarydata, configmap-size-limit, envfrom, ckad]
level: practitioner
status: docs-checked
description: "Create ConfigMaps from literals, files, directories and env files; consume via env, envFrom and volumes; handle binaryData, key naming rules and the 1 MiB limit."
sources: ["https://kubernetes.io/docs/concepts/configuration/configmap/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_configmap/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create", "https://kubernetes.io/docs/reference/using-api/server-side-apply/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ConfigMap creation, consumption and limits

## Create
```bash
kubectl create configmap app --from-literal=LOG_LEVEL=info --from-literal=FEATURE_X=true
kubectl create configmap nginx --from-file=nginx.conf                 # key = nginx.conf
kubectl create configmap nginx --from-file=default.conf=./site.conf   # custom key
kubectl create configmap static --from-file=./conf.d/                 # each file -> key
kubectl create configmap app-env --from-env-file=app.env              # KEY=VALUE lines -> keys
kubectl create configmap app --from-file=... --dry-run=client -o yaml > cm.yaml   # for git
```
Files that are not valid UTF-8 (images, keystores) are placed in **`binaryData`** automatically (base64).

## Consume
```yaml
env:
- name: LOG_LEVEL
  valueFrom: {configMapKeyRef: {name: app, key: LOG_LEVEL, optional: false}}
envFrom:
- configMapRef: {name: app-env}
  prefix: APP_
volumes:
- name: conf
  configMap:
    name: nginx
    items: [{key: default.conf, path: default.conf}]   # select/rename keys
    defaultMode: 0444
```
- ConfigMaps consumed as env vars are not updated automatically and need a pod restart. Mounted volumes are
  eventually updated (up to the kubelet sync period plus cache propagation delay) except `subPath` mounts, which never update.
- `envFrom` skips keys that are not valid env var names; the pod still starts and the kubelet records a Warning event listing the skipped keys.

## Limits and rules
- A ConfigMap cannot exceed **1 MiB**. For larger settings consider mounting a volume or a separate data store. Total annotation size is limited to 256 KiB
  (262144 bytes); client-side apply stores the manifest in the `last-applied-configuration` annotation, so use server-side apply for big objects.
- Keys: alphanumerics, `-`, `_`, `.`; data and binaryData keys must not overlap.
- A referenced ConfigMap that does not exist is an error for the pod unless the reference is marked `optional: true`.

## Rollouts on change
ConfigMap edits don't restart pods. A Deployment rolls out only when its pod template changes, so put a hash of the config in a pod-template annotation or reference a new ConfigMap name, or run `kubectl rollout restart`.

## Verify
- [ ] `kubectl exec <pod> -- env` and the mounted files show the expected values.
- [ ] No ConfigMap is close to the 1 MiB limit.

## Checked
Checked 2026-10-24 against the Kubernetes ConfigMap and Configure a Pod to Use a ConfigMap pages (website main, v1.37) and kubectl source (main): 1 MiB limit, key character rules, data and binaryData must not overlap, automatic binaryData placement for non-UTF-8 files, env vars not updated, subPath not updated, update delay = kubelet sync period plus cache propagation, skipped invalid env names with a Warning event, 262144-byte annotation limit, `create configmap` source flags. Removed the etcd 1.5 MiB figure, error names, tool names and the jq check.
Method: documentation only; no commands were run.
