---
id: computing-software.cloud-infrastructure-engineering.kubernetes.endpointslice-inspection
name: endpointslice-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, endpointslice, kubernetes-io-service-name, service-troubleshooting, endpointslices]
level: practitioner
status: docs-checked
description: "Inspect a Service's EndpointSlices by the kubernetes.io/service-name label: addresses, ports, readiness conditions, zones and which controller manages them."
sources: ["https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/", "https://kubernetes.io/docs/reference/kubernetes-api/service-resources/endpoint-slice-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting EndpointSlices

A Service can have several slices (at most 100 endpoints each by default, configurable up to 1000
with the controller's `--max-endpoints-per-slice`), named `<service>-<random>`; find them by label,
not name.

```bash
kubectl get endpointslices -n shop -l kubernetes.io/service-name=web
kubectl get endpointslices -n shop -l kubernetes.io/service-name=web -o wide
kubectl describe endpointslice -n shop -l kubernetes.io/service-name=web
kubectl get endpointslices -n shop -l kubernetes.io/service-name=web -o yaml
```

## What to look for
| Observation | Meaning |
|---|---|
| no slices | Service has no selector (you manage slices) or the controller is not running |
| slice with no endpoints | selector matches no pods |
| endpoints all `ready: false` | pods failing readiness |
| `ports` empty or wrong | check the Service `targetPort` against the pods' port names |
| `serving: true`, `terminating: true` | pod shutting down but still passing readiness |
| no `zone` or `hints` | zone information or hints not populated; hints appear only when a zone-preference feature is active |

Label `endpointslice.kubernetes.io/managed-by` tells you who owns the slice:
`endpointslice-controller.k8s.io` (normal), `endpointslicemirroring-controller.k8s.io`
(mirrored from a manual Endpoints object), or another controller.

## Compare with pods
```bash
kubectl get pods -n shop -l app=web -o wide       # pod IPs should match the ready endpoint addresses
```

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed: default 100 and maximum 1000 endpoints per slice, label-based lookup, condition names, managed-by values (labels reference and source), hints behaviour (topology and Service pages). Removed the jq pipeline and the speculative reading of empty ports.

Method: documentation only; no commands were run.
