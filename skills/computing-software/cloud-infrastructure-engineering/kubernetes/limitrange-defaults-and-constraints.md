---
id: computing-software.cloud-infrastructure-engineering.kubernetes.limitrange-defaults-and-constraints
name: limitrange-defaults-and-constraints
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, limitrange, limitrange-defaults, default-request, maxlimitrequestratio, admission, cka]
level: practitioner
status: docs-checked
description: "Use LimitRange to inject default requests/limits and enforce min/max and limit-to-request ratios per container, pod and PVC, and understand when defaults surprise you."
sources: ["https://kubernetes.io/docs/concepts/policy/limit-range/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LimitRange defaults and constraints

LimitRange is enforced by the `LimitRanger` admission plugin at **pod creation** (and PVC
creation). It never changes running pods.

```yaml
apiVersion: v1
kind: LimitRange
metadata: {name: defaults, namespace: team-a}
spec:
  limits:
  - type: Container
    defaultRequest: {cpu: 100m, memory: 128Mi}   # injected when request missing
    default: {memory: 512Mi}                     # injected limit when limit missing (omit cpu = no CPU limit)
    min: {cpu: 10m, memory: 32Mi}
    max: {cpu: "4", memory: 8Gi}
    maxLimitRequestRatio: {memory: "2"}          # limit <= 2x request
  - type: Pod
    max: {memory: 16Gi}                          # sum over containers
  - type: PersistentVolumeClaim
    min: {storage: 1Gi}
    max: {storage: 100Gi}
```

## Defaulting rules that surprise people
- Container sets a **limit but no request**: if no admission-time mechanism (such as a LimitRange
  `defaultRequest`) supplies a request, Kubernetes copies the limit as the request. Big limits can
  therefore become big requests → unschedulable pods.
- Container sets a request but no limit → limit = `default`; a LimitRange does not check that its
  defaults are consistent, so if the request exceeds that default limit the pod is **rejected**
  (`requests: Invalid value ... must be less than or equal to cpu limit`).
- Defaults apply to init containers too (native sidecars are init containers).
- Two or more LimitRange objects in a namespace: which default is applied is not deterministic — keep one.

## Why have one
- A ResourceQuota on `requests.cpu`/`limits.memory` **rejects pods without those fields**;
  LimitRange defaults make quota-enabled namespaces usable.
- Pods with no requests or limits are BestEffort; defaulted requests give them at least Burstable QoS.

## Debug
```bash
kubectl describe limitrange -n team-a
kubectl get pod p -o jsonpath='{.metadata.annotations.kubernetes\.io/limit-ranger}'   # what was injected
kubectl run t --image=<image> -n team-a --dry-run=server -o yaml
```
Rejections name the violated constraint (for example a maximum per Container) in a `forbidden` error.

## Verify
- [ ] Every tenant namespace has exactly one LimitRange; server dry-run of a bare pod shows sane defaults.

## Checked
2026-10-23, against the Kubernetes website LimitRange page (admission at creation only, unchanged running pods, non-deterministic with multiple LimitRanges, defaults not checked for consistency and the rejection error), the resource-management page (limit copied to request when no admission default applies), and the LimitRanger admission source (`kubernetes.io/limit-ranger` annotation, init containers). The BestEffort-first eviction aside and the exact forbidden message were removed or generalised as unconfirmed.
Method: documentation only; no commands were run.
