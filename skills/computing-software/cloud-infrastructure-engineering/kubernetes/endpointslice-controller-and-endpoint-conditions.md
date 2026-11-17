---
id: computing-software.cloud-infrastructure-engineering.kubernetes.endpointslice-controller-and-endpoint-conditions
name: endpointslice-controller-and-endpoint-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, endpointslices, endpointslice-controller, max-endpoints-per-slice, terminating-endpoints, serving-condition, ready-condition, rollouts, publishnotreadyaddresses]
level: advanced
status: docs-checked
description: "Understand EndpointSlice mechanics: the controller, maxEndpointsPerSlice and churn, and the ready/serving/terminating conditions that make rolling updates drain gracefully."
sources: ["https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/", "https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/#conditions", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# EndpointSlice controller and endpoint conditions

## Controller
kube-controller-manager's EndpointSlice controller watches Services with selectors and Pods,
writing `EndpointSlice` objects labelled `kubernetes.io/service-name=<svc>` and
`endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io`.
- `--max-endpoints-per-slice` (default 100, at most 1000). Smaller slices mean smaller updates
  on each pod change. Leave the default unless you measured.
- `--concurrent-service-endpoint-syncs` (default 5) and `--endpointslice-updates-batch-period`
  (batches pod changes; default 0, meaning every pod update triggers an update) trade throughput
  against freshness.
- The legacy `Endpoints` object is capped at 1000 addresses (annotation
  `endpoints.kubernetes.io/over-capacity: truncated`); consumers that read Endpoints miss the
  rest. Migrate them to EndpointSlices.
- Selector-less Services: you manage slices yourself (use your own `managed-by` value).

```bash
kubectl get endpointslices -l kubernetes.io/service-name=web -o wide
kubectl get endpointslice <name> -o yaml
```

## Conditions per endpoint
| Condition | Meaning |
|---|---|
| `ready` | shortcut for `serving` and not `terminating`; always `true` when the Service sets `publishNotReadyAddresses: true` |
| `serving` | the endpoint is currently serving responses (for Pods: passing readiness), regardless of termination |
| `terminating` | set when the Pod is first deleted (it has a deletion timestamp) |

Serving and terminating conditions are stable since 1.26. Service proxies normally ignore
`terminating` endpoints, but may route to endpoints that are both `serving` and `terminating`
when all available endpoints are terminating. For `externalTrafficPolicy: Local` and
`internalTrafficPolicy: Local`, kube-proxy uses serving-and-terminating endpoints when all local
endpoints on the node are terminating (ProxyTerminatingEndpoints, stable in 1.28), which keeps
connections draining during rollouts.

Make it work for you:
- Keep readiness passing while the application still serves during graceful shutdown.
- `publishNotReadyAddresses: true` (for example on headless Services used for peer discovery)
  makes endpoints `ready` regardless of readiness.

## Verify
- [ ] During `kubectl rollout restart`, old endpoints show `terminating: true` while new ones become `ready`, and clients see no errors.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed: flag names and defaults (kubernetes/kubernetes controller options and defaults: 5 concurrent syncs, 100 per slice, batch period 0, maximum 1000 from the EndpointSlice page), condition definitions and 1.26 stability, ProxyTerminatingEndpoints stable in 1.28 (previous text said 1.26), the over-capacity truncation. Removed the 5000-pod anecdote, the yq pipeline and the preStop recommendation.

Method: documentation only; no commands were run.
