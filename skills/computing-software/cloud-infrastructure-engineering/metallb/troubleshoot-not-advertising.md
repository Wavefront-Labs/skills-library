---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-not-advertising
name: troubleshoot-not-advertising
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, not-advertising, exclude-lb, ignore-exclude-lb, control-plane, troubleshooting, speaker, endpoints]
level: practitioner
status: docs-checked
description: "Why a MetalLB speaker does not announce a Service: no endpoints, Local policy, missing advertisement, network unavailable, or exclude-from-external-load-balancers label."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service not advertised

Remember: MetalLB only attracts traffic to the nodes. Reaching the LoadBalancer IP from a node proves the CNI works, not MetalLB. Pinging the service IP will not work; access the service itself.

See who announces: each speaker publishes an event `announcing from node "xxx" with protocol "bgp"` (or l2). Check:
```bash
kubectl describe svc <service-name>
```
L2 has one announcer; BGP has many.

A speaker will not advertise a Service if:
- the Service has no active endpoints,
- `externalTrafficPolicy=local` and no running endpoint on that speaker's node,
- no L2Advertisement/BGPAdvertisement matches the node (when node selectors are used),
- the Kubernetes API reports "network not available" on the node.

Control-plane or single-node cluster: MetalLB honours the label `node.kubernetes.io/exclude-from-external-load-balancers` and will not announce from such nodes. Remove the label, or give the speakers `--ignore-exclude-lb` (via Helm or Kustomize).

Also confirm an advertisement instance exists: an `L2Advertisement` (for L2) or `BGPAdvertisement` (for BGP) must be created.

Next: `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-l2-arping` or `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-bgp-session`. Status resources help: `computing-software.cloud-infrastructure-engineering.metallb.service-status-resources`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page: component roles, the announcing event text, the four no-advertise conditions, the exclude-from-external-load-balancers label and --ignore-exclude-lb. Reworded the advertisement-required line to the page's own statement.
Method: documentation only; no commands were run.
