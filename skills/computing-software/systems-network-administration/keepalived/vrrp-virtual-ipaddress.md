---
id: computing-software.systems-network-administration.keepalived.vrrp-virtual-ipaddress
name: vrrp-virtual-ipaddress
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, virtual-ipaddress, vip, virtual-ipaddress-excluded]
level: practitioner
status: docs-checked
description: "virtual_ipaddress block (up to 20 VIPs, protocol VIPs) versus virtual_ipaddress_excluded (unlimited, not protocol VIPs), with an example."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual IP addresses

```
virtual_ipaddress {
    192.168.200.10
    192.168.200.11
}
```
- `virtual_ipaddress`: block of VIPs for the instance; the synopsis says up to 20.
- `virtual_ipaddress_excluded`: block with no limit on count; these are not protocol VIPs.

Whichever node is MASTER owns the VIPs as interface addresses; a BACKUP does not. In the failover case study, ip address list on director 1 with only itself running shows all VIPs, and after the peer starts it keeps only the VIPs of its MASTER instances.

Verify: ip address list on MASTER shows each VIP and the BACKUP shows none of that instance's VIPs.

## Checked

2026-11-04. Confirmed the 20-address limit, the unlimited excluded block and its description as not protocol VIPs on the configuration synopsis page, and the ip address list ownership behaviour on the Failover case study page. Removed the unsourced claim that excluded addresses are not carried in advertisements.

Method: documentation only; no commands were run.
