---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-top-containers-and-sort-by
name: kubectl-top-containers-and-sort-by
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metrics-pipeline, top-sort-by, kubectl-top, metrics-server, resource-usage]
level: practitioner
status: docs-checked
description: "Use kubectl top with --containers, --sort-by, --sum, label selectors and namespaces to find the biggest CPU and memory consumers quickly."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/kubectl_top_pod/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/kubectl_top_node/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/top", "https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl top --containers and --sort-by

Requires metrics-server (the `metrics.k8s.io` API).

```bash
kubectl top nodes --sort-by=cpu
kubectl top nodes -l node.kubernetes.io/instance-type=<type>
kubectl top pods -A --sort-by=memory
kubectl top pods -n shop --containers --sort-by=cpu       # per container rows
kubectl top pods -n shop -l app=web --sum                 # totals at the bottom
kubectl top pod web-7c9 --containers
kubectl top pods -A --no-headers
```
`--sort-by` accepts only `cpu` or `memory`.

## Reading the numbers
- Metrics come from a metrics pipeline with a delay, so new pods may show no values for a while.
- `kubectl top nodes` reports against allocatable by default; `--show-capacity` uses capacity.
- Compare with requests: `kubectl describe node` shows requested; `top` shows used. Big gaps are
  rightsizing targets.

## Errors
| Message | Cause |
|---|---|
| `error: Metrics API not available` | the Metrics API is not served (for example metrics-server is not installed) |
| `metrics not available yet` | new pod; the metrics pipeline delay can be a few minutes after pod creation |

## Verify
`kubectl get apiservices` lists the `metrics.k8s.io` APIService (served as `metrics.k8s.io/v1` in current documentation) as Available.

## Checked
Checked 2026-10-24 against the kubectl top pod and top node source (main) and the resource metrics pipeline page (v1.37): `--containers`, `--sum`, `--sort-by` limited to cpu or memory, `-l`/`-A`/`--no-headers`, `--show-capacity`, the `Metrics API not available` and `metrics not available yet` errors, metrics-server implements the Metrics API (`metrics.k8s.io/v1`), the pipeline delay after pod creation. Removed the unconfirmed working-set, window, node-percentage and APIService version claims and the shell pipes.
Method: documentation only; no commands were run.
