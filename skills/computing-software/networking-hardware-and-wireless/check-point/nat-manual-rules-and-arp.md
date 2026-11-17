---
id: computing-software.networking-hardware-and-wireless.check-point.nat-manual-rules-and-arp
name: nat-manual-rules-and-arp
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, manual-nat, proxy-arp, local-arp]
level: practitioner
status: draft
description: "Write manual NAT rules in Check Point R81 and publish proxy ARP entries via local.arp when automatic ARP does not apply."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manual NAT rules, proxy ARP and local.arp

```
mgmt_cli -r true add nat-rule package "Standard" position top original-source "any_net" original-destination "vip_pub" original-service "https" translated-source "Original" translated-destination "web1_priv" translated-service "Original" install-on "gw1"
# gateway side, expert mode:
echo "203.0.113.50 00:1c:7f:aa:bb:cc" >> $FWDIR/conf/local.arp
fw ctl arp
```
- Manual rules are needed for many-to-many translation, port translation, or for a public address that is not an object field. Rules are evaluated top-down: the first match applies only to the matching packet direction; there is no implicit reverse.
- When a manual rule uses a public address, the gateway will not answer ARP for it automatically; add it to `$FWDIR/conf/local.arp` (IP then the MAC of the interface, e.g. the gateway's external MAC) and reinstall the policy. In R80+ the same can come from Global Properties > NAT > Merge manual proxy ARP configuration (confirm).
- Routing: the translated internal address must be routable from the gateway; the public address needs a route on the upstream router to the gateway, or ARP.
- Cluster: use the cluster VIP's MAC, not a member MAC, so failover keeps the proxy ARP; this is the main gotcha.
- Disable "Automatic ARP" only if you manage everything by hand.

Verify: `fw ctl arp` lists the entry; `arping -I eth0 203.0.113.50` from the upstream segment returns the cluster MAC; test a connection and view translated IPs in the log.
