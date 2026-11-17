---
id: computing-software.cloud-infrastructure-engineering.calico.host-endpoints-failsafe-rules
name: host-endpoints-failsafe-rules
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [failsafe, host-endpoint, felix, failsafeinboundhostports, failsafeoutboundhostports, ssh, bgp, etcd]
level: practitioner
status: docs-checked
description: "Default failsafe ports open on every Calico host endpoint, the Felix parameters that change them, and the risk of emptying them."
sources:
  - https://docs.tigera.io/calico/latest/reference/host-endpoints/failsafe
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failsafe rules keep pinholes open on **all** host endpoints so a malformed policy cannot completely cut a host off.

Default open ports:

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 22 | TCP | Inbound | SSH |
| 53 | UDP | Outbound | DNS |
| 67 | UDP | Outbound | DHCP |
| 68 | UDP | Inbound | DHCP |
| 179 | TCP | In and out | BGP |
| 2379, 2380 | TCP | In and out | etcd |
| 5473 | TCP | In and out | listed as etcd access |
| 6443 | TCP | In and out | Kubernetes API server |
| 6666, 6667 | TCP | In and out | self-hosted etcd service |

**Changing them.** Set the Felix parameters `FailsafeInboundHostPorts` and `FailsafeOutboundHostPorts`. Setting either to `"[]"` disables that direction.

**Risks stated on the page.**
- Removing inbound failsafe rules can leave a host inaccessible.
- Removing outbound failsafe rules can leave Felix unable to connect to etcd.

Before disabling, write policy with more specific rules for your environment (the page points to a basic-connectivity policy guide).

Failsafe does not replace a restrictive host policy. It only guarantees the listed ports stay reachable.

## Checked

Read in full on 2026-11-08: the Failsafe rules page. The port table, the two Felix parameters, the "[]" setting and both warnings match it. The 5473 label is quoted as the page shows it. A comparison with another page was dropped as it was not cited.

Method: documentation only; no commands were run.
