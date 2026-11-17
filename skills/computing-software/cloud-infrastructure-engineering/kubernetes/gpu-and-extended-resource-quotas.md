---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gpu-and-extended-resource-quotas
name: gpu-and-extended-resource-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, gpu-quota, extended-resources, device-plugins, dra]
level: practitioner
status: docs-checked
description: "Cap GPUs and other extended resources per namespace with ResourceQuota requests keys, and handle quotas for DRA device classes."
sources: ["https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-for-extended-resources", "https://github.com/NVIDIA/k8s-device-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU and extended resource quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: gpu, namespace: ml-team}
spec:
  hard:
    requests.nvidia.com/gpu: "4"
    requests.amd.com/gpu: "0"        # forbid a vendor entirely
```
Extended resources cannot be overcommitted, so for them only quota items with the `requests.` prefix are
allowed (the docs: it makes no sense to specify both requests and limits in a quota).

## Scope it
```yaml
spec:
  hard: {requests.nvidia.com/gpu: "2"}
  scopeSelector:
    matchExpressions:
    - {scopeName: PriorityClass, operator: In, values: [interactive]}
```
Separate quotas for interactive notebooks and batch training stop one from starving the other.

## DRA devices
With dynamic resource allocation, quota counts resource claims per device class, using the key
`<device-class-name>.deviceclass.resource.k8s.io/devices` (the docs use a class named `examplegpu`):
```yaml
hard:
  examplegpu.deviceclass.resource.k8s.io/devices: "8"
```
When extended-resource allocation by DRA is enabled, a class can also be counted through
`requests.<extended-resource-name>` or the derived `requests.deviceclass.resource.kubernetes.io/<class>`.

## Gotchas
- With the NVIDIA device plugin's `mixed` MIG strategy, MIG devices appear as separate resources of the form
  `nvidia.com/mig-<slice_count>g.<memory_size>gb`; quota each name.
- Quota counts what pods request; it does not stop idle reservations: a notebook holding a GPU for days counts fully.

## Verify
```bash
kubectl describe quota gpu -n ml-team
kubectl -n ml-team apply -f gpu-pod-requesting-5.yaml    # a pod requesting 5 nvidia.com/gpu
```
The pod must be rejected by quota admission.

## Checked
2026-10-23, against the Kubernetes website resource-quotas page (extended resources: only `requests.` items allowed; DRA device-class quota keys and the extended-resource forms) and the NVIDIA k8s-device-plugin README (MIG mixed strategy resource names). The time-slicing count claim and the pinned CUDA image were removed as unconfirmed.
Method: documentation only; no commands were run.
