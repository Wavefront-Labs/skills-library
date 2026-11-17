---
id: computing-software.networking-hardware-and-wireless.check-point.nat-automatic-hide-and-static
name: nat-automatic-hide-and-static
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, nat, hide-nat, static-nat]
level: practitioner
status: draft
description: "Configure Check Point automatic NAT on network objects (hide behind gateway or IP, static) with the required routes and ARP."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automatic NAT: hide and static

- Automatic NAT is set on an object (Network Object > NAT tab) and generates NAT rules at the bottom of the NAT rulebase. **Hide** many-to-one (source port translation); **Static** one-to-one both directions.
```
mgmt_cli -r true set network name "net_dmz" nat-settings.auto-rule true nat-settings.method hide nat-settings.hide-behind gateway nat-settings.install-on "gw1"
mgmt_cli -r true set host name "web1" nat-settings.auto-rule true nat-settings.method static nat-settings.ip-address "203.0.113.20"
mgmt_cli -r true publish
```
- Hide NAT can use the gateway's external IP ("hide behind gateway") or a specific IP. The hide range is limited by ports per IP; port exhaustion shows as dropped connections with "NAT" in `fw ctl zdebug drop`.
- For static NAT the inbound traffic to the public IP must arrive at the gateway, i.e. routes/ARP point to it. Automatic ARP is on by default (Global Properties > NAT > "Automatic ARP configuration"); verify with `fw ctl arp`.
- Policy rules reference the *original* (pre-NAT) addresses for source and the **public** (pre-NAT) address for inbound destination; that is a classic pitfall: with R80+ the rule uses the original destination (translated server IP is the internal one in rule).
- NAT order: static before hide, and manual rules before automatic ones.
- Gotcha: NAT'd traffic is still subject to anti-spoofing based on interface topology (internal addresses must be defined on the internal interface).

Verify: `fw ctl arp` lists the proxied public IPs; `fw monitor -e "accept host(203.0.113.20);" ` shows the translation in the `i`/`o`/`I`/`O` positions; the log shows `XlateSrc`/`XlateDst`.
