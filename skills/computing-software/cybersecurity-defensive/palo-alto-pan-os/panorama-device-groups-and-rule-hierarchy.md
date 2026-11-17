---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.panorama-device-groups-and-rule-hierarchy
name: panorama-device-groups-and-rule-hierarchy
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [device-groups, panorama, shared-objects, pre-rules, post-rules, push-to-devices, policy-hierarchy]
level: practitioner
status: draft
description: "Organise firewalls into Panorama device groups with shared and local objects, pre and post rules, and push policy safely."
sources: ["https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin/manage-firewalls/manage-device-groups"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: central policy for many firewalls with local exceptions.

Hierarchy: Shared > parent device groups > child device groups > firewall local config. Evaluation order: Shared pre-rules, device group pre-rules, local rules, device group post-rules, shared post-rules, then the default rules.

```
configure
set device-group DG-BRANCH devices 001122334455
set device-group DG-BRANCH pre-rulebase security rules block-bad from any to any source any destination any application any service any action deny
set device-group DG-BRANCH post-rulebase security rules deny-log from any to any source any destination any application any service any action deny log-end yes
commit
commit-all shared-policy device-group DG-BRANCH
```
`commit` saves to Panorama; `commit-all` (Push to Devices) sends to firewalls. Both are needed.

Gotchas
- Objects pushed from Panorama can be overridden locally only if override is enabled on the object.
- Name conflicts between shared and local objects: shared wins unless "Objects defined in ancestors take precedence" is toggled (confirm option).
- Push in stages: use Preview Changes and push to a test device group first.
- Deleting a device from a group does not remove pushed policy from the device until you detach.

## Verify
```
show devices connected
show devices all
```
Firewalls should show device group sync state `In Sync` (Panorama > Managed Devices) after push; check the firewall `show config pushed-shared-policy`.
