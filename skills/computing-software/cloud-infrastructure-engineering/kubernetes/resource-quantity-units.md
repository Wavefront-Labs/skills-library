---
id: computing-software.cloud-infrastructure-engineering.kubernetes.resource-quantity-units
name: resource-quantity-units
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resource-requests, resource-units, millicores, resource-limits]
level: practitioner
status: docs-checked
description: "Write Kubernetes resource quantities correctly: CPU millicores, binary Mi/Gi vs decimal M/G, and the classic mistakes like 512m memory."
sources: ["https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes", "https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource quantity units

## CPU
- `1` = one physical core or one virtual core, depending on whether the node is a physical host or a VM. `500m` = 0.5; `0.1` equals `100m`.
- Kubernetes does not allow CPU precision finer than `1m` (`0.001`); `0.0005` is invalid.
- The CPU request typically defines a weighting between containers; the CPU limit throttles the container.

## Memory and storage
| Suffix | Meaning |
|---|---|
| `Ki`, `Mi`, `Gi`, `Ti`, `Pi`, `Ei` | binary: powers of two |
| `k`, `M`, `G`, `T`, `P`, `E` | decimal: powers of ten |
| no suffix | bytes |
| `m` | milli-units: **thousandths of a byte** |

So `128M` = 128,000,000 bytes (about 122 Mi), and `memory: 400m` is 0.4 bytes: the Kubernetes docs warn that "M" means megabytes and "m" millibytes, and that someone typing `400m` probably meant `400Mi` or `400M`.
Exponent notation is valid too: the docs list `128974848, 129e6, 129M, 128974848000m, 123Mi` as roughly the same value.

## Reading normalised values
```bash
kubectl get pod <p> -o jsonpath='{.spec.containers[0].resources}'
kubectl describe node <n> | sed -n '/Allocated resources/,/Events/p'
```
Compare quantities numerically with the quantity parsing in client libraries rather than as strings.

## Gotchas
- The API server restricts quantities of extended resources to whole numbers (for example `nvidia.com/gpu: 1`).
- If you set a limit but no request, and no default request is applied, Kubernetes copies the limit into the request.
- Ephemeral storage uses the same suffixes: `ephemeral-storage: 2Gi`.

## Checked
Checked 2026-10-24 against the Resource Management for Pods and Containers page (website main, v1.37): CPU units (1 physical or virtual core, `0.1` = `100m`, no finer than `1m`), request as weighting and limit as throttle, memory suffixes E, P, T, G, M, k and Ei to Ki, millibyte `m` warning, the equivalent-value example, whole-number extended resources, limit copied to request, `ephemeral-storage` in bytes. Removed the hyperthread, `0.25` normalisation, LimitRange, lowercase-suffix and requests-above-limits claims and the jq/numfmt hint.
Method: documentation only; no commands were run.
