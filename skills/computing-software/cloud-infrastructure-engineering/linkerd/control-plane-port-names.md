---
id: computing-software.cloud-infrastructure-engineering.linkerd.control-plane-port-names
name: control-plane-port-names
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, control-plane, ports, reference, probes]
level: intro
status: docs-checked
description: "Look up the unique container port names Linkerd assigns to each control plane component for probes, Services and monitoring."
sources:
  - https://linkerd.io/2.19/reference/controlplane-port-names/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each Linkerd control plane container port has a unique name, so Services, probes and monitoring configurations can refer to ports by name instead of by number.

| Component | Port name | Protocol |
| --- | --- | --- |
| destination | `dest-grpc` | gRPC |
| destination | `dest-admin` | HTTP |
| sp-validator | `spval-admin` | HTTP |
| policy-controller | `policy-grpc` | gRPC |
| policy-controller | `policy-admin` | HTTP |
| identity | `ident-grpc` | gRPC |
| identity | `ident-admin` | HTTP |
| proxy-injector | `injector-admin` | HTTP |
| linkerd2-cni | `repair-admin` | HTTP |

Services, probes and monitoring configurations can refer to ports by these names.

```bash
kubectl -n linkerd get pods -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.containers[*].ports[*].name}{"\n"}{end}'
```

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/controlplane-port-names/.

Removed or reworded: NetworkPolicy/targetPort examples and the port-purpose commentary, which the page does not state.

Method: documentation only; no commands were run.
