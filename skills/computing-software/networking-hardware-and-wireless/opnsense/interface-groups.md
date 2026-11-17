---
id: computing-software.networking-hardware-and-wireless.opnsense.interface-groups
name: interface-groups
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [interface-groups, firewall-rules, multiwan]
level: intro
status: docs-checked
description: "Group interfaces in OPNsense so one rule set applies to all members; group processing order and the multi-WAN reply-to caveat."
sources: ["https://docs.opnsense.org/manual/firewall_groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Interface groups

Interface groups (Firewall > Groups) combine interfaces so a single set of firewall rules applies to every member. The form has Name (technical, restricted by the underlying OS naming rules), Description (informational) and Members.

Group rules are processed before rules on individual interface tabs, so overlap with per-interface rules is predictable; the firewall's rule processing order page has the details. Groups are a building block for zone-style designs; the Security Zones how-to describes a deployment strategy built on them.

Multi-WAN caution: a group is not bound to one interface, so when the group is applied to WAN-type interfaces the traffic uses normal routing to pick the next hop, because reply-to is not used there.

## Checked

2026-11-03. Read the Interface Groups manual page (firewall_groups.html) on docs.opnsense.org and confirmed the claims above against them. Removed: the unsupported advice to move reply-to-dependent rules onto the individual WAN interface, and a repeated sentence.
Method: documentation only; no commands were run.
