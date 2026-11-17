---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-intermittent-traffic
name: troubleshoot-intermittent-traffic
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, intermittent, narrowing-scope, tcpdump, troubleshooting, ecmp, cni]
level: advanced
status: docs-checked
description: "Isolate a MetalLB Service that is announced but unreachable or flaky: tcpdump on node and pod, intermittent causes, and shrinking to one node and one pod."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Announced but not reachable, or intermittent

Networking has many failure points; use tcpdump to find where traffic stops, on the node and on the endpoint pod.
- Traffic does not reach the node: network infrastructure or MetalLB.
- Traffic reaches the node but not the pod: likely the CNI.

Intermittent causes:
- The entry point changes each time (especially BGP, which exposes ECMP routes).
- The L2 leader bounces between nodes.
- Endpoints constantly restart (all or some).
- Some endpoints reply and others do not.

Narrow the scope:
1. Limit the advertisement to one node with a node selector in the `BGPAdvertisement` or `L2Advertisement` (`computing-software.cloud-infrastructure-engineering.metallb.l2-node-selectors`, `computing-software.cloud-infrastructure-engineering.metallb.bgp-advertisement-scope`).
2. Limit the Service endpoints to one pod.
3. Capture on that node and that pod; the path is now clear and you can tell whether failures follow a particular node or a pod on a different node.

Always test the Service itself; pinging the IP is not valid, and reaching the IP from a node proves only the CNI.

Also check the return path: `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-rp-filter`. The bug-report section asks for `kubectl get endpointslices <service> -o yaml`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page: tcpdump locations and interpretation, the four intermittent causes, the single-node, single-pod scoping method, the pinging note, and the endpointslices command.
Method: documentation only; no commands were run.
