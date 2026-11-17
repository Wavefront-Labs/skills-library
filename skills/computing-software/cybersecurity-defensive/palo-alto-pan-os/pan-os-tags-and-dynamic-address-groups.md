---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-tags-and-dynamic-address-groups
name: pan-os-tags-and-dynamic-address-groups
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [dynamic-address-group, pan-os, tags, registered-ip, auto-quarantine, dag, address-group]
level: practitioner
status: draft
description: "Use PAN-OS tags and dynamic address groups that update from log actions or the API to automate quarantine and cloud workload policy."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/monitor-changes-in-the-virtual-environment/use-dynamic-address-groups-in-policy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: policy that follows tags rather than static IP lists.

```
configure
set address-group DAG-WEB-PROD dynamic filter "'web' and 'prod'"
set rulebase security rules allow-lb-to-web from lb to web source any destination DAG-WEB-PROD application ssl action allow
commit
```
Register an IP with tags from the CLI or API:
```
request object registered-ip register 10.1.1.5 tag web
request object registered-ip register 10.1.1.5 tag prod
request object registered-ip unregister 10.1.1.5 tag prod
show object registered-ip all
```
XML API user-id message with `<register><entry ip="10.1.1.5"><tag><member>web</member></tag></entry></register>` does the same remotely. VM-Series plugins and cloud connectors can register automatically.

Auto-quarantine: in a log forwarding match-list add an action to tag the source IP with `quarantine`, and have a high-priority deny rule use the DAG `dynamic filter "'quarantine'"` (see log-forwarding skill). Add a tag timeout so hosts are released automatically.

Gotchas
- Registered IPs are held in memory and lost after a reboot unless re-registered.
- A DAG used in policy updates without commit; do not rely on this for slow cloud sources.
- Filter syntax is boolean on tag names, not partial matches.

## Verify
```
show object registered-ip all
show object dynamic-address-group name DAG-WEB-PROD
```
The group lists the registered IP as a member.
