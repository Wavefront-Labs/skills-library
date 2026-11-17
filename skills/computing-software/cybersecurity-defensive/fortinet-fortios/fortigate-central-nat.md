---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-central-nat
name: fortigate-central-nat
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [central-nat, fortios, central-snat-map, dnat-vip, nat-table, central-snat]
level: practitioner
status: draft
description: "Use FortiGate central NAT to separate NAT rules from policies with central SNAT maps and see the impact on policy configuration."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: manage translation in one table rather than per policy.

Enable it:
```
config system settings
    set central-nat enable
end
```
Then define maps:
```
config firewall central-snat-map
    edit 1
        set orig-addr "LAN-NET"
        set srcintf "port2"
        set dst-addr "all"
        set dstintf "port1"
        set nat-ippool "pool-out"
    next
end
```
In central NAT mode, the per-policy `nat` and `ippool` options disappear, and VIP objects are used through DNAT & Virtual IP entries (Policy & Objects > DNAT & Virtual IPs). Firewall policies still need to allow the traffic; for destination NAT the policy references the VIP as before.

Gotchas
- Switching to central NAT does not convert existing per-policy NAT; policies using `nat enable` lose translation until central-snat-map entries are created. Plan the migration carefully.
- Map order matters; first match is used.
- `central-nat` is a VDOM-level setting.

## Verify
```
show firewall central-snat-map
diagnose sys session list
```
New sessions show SNAT as defined by the map; confirm no outbound failures after enabling.
