---
id: computing-software.networking-hardware-and-wireless.check-point.anti-spoofing-and-topology
name: anti-spoofing-and-topology
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, anti-spoofing, topology, interface-groups]
level: practitioner
status: draft
description: "Configure Check Point anti-spoofing by defining interface topology correctly (internal, external, specific group) and fixing Anti-Spoofing drops."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anti-spoofing and interface topology

- Anti-spoofing checks that a packet arriving on an interface has a source address that is expected there. Set per interface in **Gateway > Network Management > Topology > Edit**: **Leads To** (Internet/External, or "This Network" - Internal) and **Security Zone**, plus **Anti-Spoofing** action `Prevent` and (recommended) `Log`.
- For internal interfaces, choose **Network defined by the interface IP and Net Mask** or **Specific** (a group of networks routed behind this interface). For external interfaces, "Not defined (Internet)" means "anything not belonging to another interface".
```
mgmt_cli -r true set simple-gateway name "gw1" interfaces.1.name "eth1" interfaces.1.anti-spoofing true interfaces.1.anti-spoofing-settings.action "prevent" interfaces.1.topology "INTERNAL" interfaces.1.topology-settings.specific-network "grp_internal"
fw ctl zdebug + drop | grep -i spoof
```
- Log in SmartConsole: `Anti-Spoofing` as the rule/`Info`. In Logs, drops show `Spoofing Detection`/`Anti Spoofing`, with the interface and address.
- Typical causes: a routed network behind an internal router was not added to the specific group; a VPN Office Mode pool or NAT range missing; asymmetric routing; dynamic routing changes adding new networks.
- Use **Don't check packets from** and select an exception group for management stations if needed (e.g. a monitor).
- Gotcha: if you set Anti-Spoofing to `Detect` instead of `Prevent`, you must also be sure it is on; `Disabled` hides problems and is not recommended.

Verify: generate traffic from a host in the problematic subnet; the log shows no spoofing drop; `fw ctl zdebug + drop` stays quiet for that source. `fw ctl iflist` shows interface numbers used in the logs.
