---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-interface-selection
name: l2-interface-selection
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, l2-interfaces, interfaces, l2advertisement, layer2, nic, union]
level: advanced
status: docs-checked
description: "Limit the interfaces MetalLB announces L2 IPs from using interfaces on L2Advertisement, how multiple advertisements union, and the leader-election trap."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_l2_configuration.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 interface selection

By default the speaker announces a LoadBalancer IP from all node interfaces. Choose a subset with `interfaces`:

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - third-pool
  interfaces:
  - eth0
  - eth1
```
Combine with `nodeSelectors`: add `nodeSelectors` matching hostname `NodeA` and `interfaces: [eth3]` to announce `fourth-pool` only from eth3 of NodeA.

Union rule: an IP is advertised via the union of all `L2Advertisements` referencing its pool. With one ad (`interfaces: [eno1]`, no pool selector, so all pools) and another (pool1, hostB, `ens18`): VIPs of pool1 go out of eno1 on every node, plus ens18 when hostB is the leader.

Warning: the interface selector does not influence leader election. If the elected leader lacks the selected interface, the service is not announced. You must combine interfaces with node selectors to avoid this. MetalLB records an event on the Service in that case (`kubectl describe svc <name>`).

See also `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-l2-arping`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced L2 configuration" page (interfaces, nodeSelectors combination, union note and example, leader-election warning) and the Troubleshooting page (event on the Service when no compatible interface exists). Removed an added verify command line.
Method: documentation only; no commands were run.
