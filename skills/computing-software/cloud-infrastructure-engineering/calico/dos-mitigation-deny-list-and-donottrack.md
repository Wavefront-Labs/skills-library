---
id: computing-software.cloud-infrastructure-engineering.calico.dos-mitigation-deny-list-and-donottrack
name: dos-mitigation-deny-list-and-donottrack
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [dos, xdp, donottrack, applyonforward, globalnetworkset, host-endpoint, conntrack, deny-list]
level: advanced
status: docs-checked
description: "Drop denied CIDRs early with a GlobalNetworkSet and doNotTrack policy, and bypass conntrack for extreme high-connection servers."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/extreme-traffic/defend-dos-attack
  - https://docs.tigera.io/calico/latest/network-policy/extreme-traffic/high-connection-workloads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Deny-list DoS defence.** Calico enforces deny-list policies as early as it can: NIC hardware (XDP offload), then NIC driver (XDP native), then kernel XDP generic (only if explicitly enabled; no benefit over raw), else iptables raw mode. XDP needs Linux 4.16 or later. Best practice is to build these before an attack.

1. HostEndpoint on the interface, labelled `apply-dos-mitigation: 'true'` (`interfaceName: eth0`, `node`, `expectedIPs`).
2. GlobalNetworkSet holding the CIDRs and a label:

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkSet
metadata:
  name: dos-mitigation
  labels:
    dos-deny-list: 'true'
spec:
  nets:
    - '1.2.3.4/32'
    - '5.6.0.0/16'
```

3. GlobalNetworkPolicy:

```yaml
spec:
  selector: apply-dos-mitigation == 'true'
  doNotTrack: true
  applyOnForward: true
  types:
    - Ingress
  ingress:
    - action: Deny
      source:
        selector: dos-deny-list == 'true'
```

**Extreme high-connection workloads.** If connections exceed what conntrack can track, `doNotTrack: true` bypasses it. These rules are stateless: ingress and egress must both be written (ingress covers all traffic through the host endpoint, egress only host-sent traffic), and `applyOnForward: true` is required. The page's example is a hostNetwork memcached server with a source-port egress rule mirroring the ingress rule.

## Checked

Read in full on 2026-11-08: the Defend against DoS attacks page (processing-mode order, Linux 4.16 for XDP, the three resources and the doNotTrack policy) and the Enable extreme high-connection workloads page (stateless ingress and egress rules, applyOnForward, hostNetwork memcached example). The policy name and metadata are abridged here.

Method: documentation only; no commands were run.
