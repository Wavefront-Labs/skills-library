---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vpa-controlled-values
name: vpa-controlled-values
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, controlledvalues, resourcepolicy, resource-limits]
level: practitioner
status: docs-checked
description: "Choose VPA controlledValues RequestsOnly versus RequestsAndLimits, how limits scale proportionally, and the OOM and throttling traps of each."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/api.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/features.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/faq.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPA controlledValues

```yaml
spec:
  resourcePolicy:
    containerPolicies:
    - containerName: app
      controlledResources: [cpu, memory]
      controlledValues: RequestsOnly        # default RequestsAndLimits
```

## RequestsAndLimits (default)
VPA sets requests to the recommendation and scales limits to keep the original
limit/request ratio. Pod with request 100m / limit 200m and recommendation 300m gets
300m / 600m.
- Good: headroom stays proportional.
- Trap: a large ratio (request 50Mi, limit 2Gi) becomes huge limits. VPA tries to cap
  recommendations within LimitRange min and max, but if a LimitRange conflicts with the VPA
  resource policy, VPA follows its own policy and can set values outside the LimitRange.

## RequestsOnly
VPA changes requests, leaves limits as written.
- Good: you keep a fixed memory ceiling.
- Trap: the recommendation can approach or exceed the fixed limit, and the container keeps
  OOMing at the same ceiling. Watch for recommendations near the limit.
- With no limits set at all, `RequestsAndLimits` also sets limits when it updates a pod
  (FAQ), so `RequestsOnly` is how you keep them unset.

## Typical choices
| Workload | Setting |
|---|---|
| Fixed limits you manage yourself | `controlledResources: [cpu, memory]`, RequestsOnly |
| Memory-sensitive JVM with -Xmx tied to limit | RequestsOnly (heap flags depend on limit) |
| Simple stateless services | default |

## Verify
```bash
kubectl describe vpa app-vpa
kubectl get pod <new-pod> -o jsonpath='{.spec.containers[0].resources}'
```

## Checked

Checked 2026-10-24 against the kubernetes/autoscaler vertical-pod-autoscaler docs (master, default version VPA 1.8.1).
- `controlledValues` enum (`RequestsAndLimits` default, `RequestsOnly`) and the proportional-limit meaning: api.md.
- LimitRange interaction: features.md "Limits control" says VPA caps within LimitRange min and max but follows the VPA policy when they conflict.
- Behaviour with unset requests and limits under each mode: faq.md "How does VPA treat resource requests and limits?".

Method: documentation only; no commands were run.
