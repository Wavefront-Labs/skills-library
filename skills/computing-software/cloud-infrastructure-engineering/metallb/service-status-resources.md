---
id: computing-software.cloud-infrastructure-engineering.metallb.service-status-resources
name: service-status-resources
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, servicel2status, servicebgpstatus, announcing-node, labels, bgpsessionstate]
level: practitioner
status: docs-checked
description: "Find which node announces a MetalLB Service with ServiceL2Status and ServiceBGPStatus resources and their labels, and why BGP status only shows intent."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/faq/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServiceL2Status and ServiceBGPStatus

Besides logs, events and metrics, the speakers maintain status resources:
```bash
kubectl get servicel2statuses -n metallb-system
# NAME  ALLOCATED NODE  SERVICE NAME  SERVICE NAMESPACE
kubectl get servicebgpstatuses -n metallb-system
# NAME  NODE  SERVICE NAME  SERVICE NAMESPACE
```
L2 shows the one node announcing; BGP shows one row per node announcing the Service.

Each resource carries labels `metallb.io/node`, `metallb.io/service-name` and `metallb.io/service-namespace`, so you can filter:
```bash
kubectl get servicebgpstatuses -n metallb-system \
  -l metallb.io/service-name="service3",metallb.io/service-namespace="ns3",metallb.io/node=kind-worker
```
Caveat from the API docs: `ServiceBGPStatus` records the node's intention to advertise to a set of peers. Real advertisement depends on BGP session state, which you read from metrics, logs, or in FRR-K8s mode the `BGPSessionState` resource.

Events: `kubectl describe svc <name>`. Advertising problems: `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-not-advertising`.

## Checked

2026-11-04. Confirmed against the MetalLB FAQ ("How can I understand which node advertises a given Service?": both resources, example columns, the three labels, filter example, ServiceBGPStatus intention caveat, BGPSessionState in FRR-K8s mode) and the Troubleshooting page (one L2 speaker, multiple BGP speakers; kubectl describe svc events). Removed the unsupported "no status row means not announced" rule.

Method: documentation only; no commands were run.
