---
id: computing-software.systems-network-administration.cisco-networking.acl-tcam-exhaustion
name: acl-tcam-exhaustion
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, sdm-template, acl-scale, security-aces, qos-aces]
level: practitioner
status: docs-checked
description: "Catalyst 9300 ACL scale limits are set by the SDM template: reading Security and QoS ACE counts with show sdm prefer, changing template with a reload, and caveats."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_sdm_templates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL capacity on Catalyst 9300: SDM templates

Hardware switches hold ACL entries in finite tables whose sizes depend on the active SDM (switching database management) template. The Cisco 9300 17.9 chapter is the only source used here.

## What the template controls
`show sdm prefer` output lists, among others, these ACL-related capacities:
- Security Access Control Entries
- QoS Access Control Entries
- Policy Based Routing ACEs (on some models "Policy Based Routing ACEs / NAT ACEs")
- Netflow Input and Output ACEs, Flow SPAN ACEs

Examples from the chapter (illustrative, they vary by model and release; read them on your switch):
- Access template, standard 9300 sample: Security ACEs 5120, QoS ACEs 5120, PBR ACEs 1024.
- NAT template, same sample: Security ACEs 5120, QoS ACEs 1024, PBR ACEs 5120.
- C9300-24UB, C9300-24UXB and C9300-48UB (17.3.1 and later): Security ACEs 18432, QoS ACEs 6144, PBR/NAT ACEs 14336.

So moving between the `access` and `nat` templates trades QoS ACEs against PBR ACEs on the standard sample.

The sample output also states that its numbers are typical for L2 and IPv4 features and that features such as IPv6 use double the entry size, so only half as many entries can be created.

## Check and change
```
show sdm prefer
configure terminal
 sdm prefer access          ! or nat
 end
reload
```
- The 9300 supports the `access` and `nat` templates. The change needs a `reload`; until then `show sdm prefer` shows both the template in use and the one that becomes active.

## Rewrite before you resize
These points are general design practice rather than statements from the cited chapter: fewer, summarised prefixes and fewer object-group and range combinations mean fewer entries consumed. Check how your platform expands them before relying on a multiplier.

## Not covered by the cited page
TCAM utilisation commands, expansion rules for object groups and port ranges, log message names, software-switching symptoms and sharing of entries between interfaces. The two earlier sources (a TCAM explainer returning 404 and an unfetched page) were not usable. Look these up in the platform's ACL and troubleshooting guides.

## Verify
- [ ] `show sdm prefer` after the reload shows the template you chose and an ACE count that fits your policy.

## Checked
Date: 2026-11-08. Read in full: Configuring SDM Templates (Catalyst 9300, 17.9.x).
Confirmed: access and nat templates, `sdm prefer access | nat`, reload and `show sdm prefer` behaviour, ACE counts quoted from the sample outputs, IPv6 double-entry note.
Removed: object-group cross-product arithmetic and range expansion claims, `%ACL_ERRMSG`/`FED_ACL` messages, FED TCAM utilisation commands, 3750/3850 commands, SGT/VACL/PACL fixes, the 80 percent threshold (none on the cited page), and the 404 source.
Method: documentation only; no commands were run.
