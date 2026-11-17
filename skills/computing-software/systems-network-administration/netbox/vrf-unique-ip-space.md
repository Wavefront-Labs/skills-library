---
id: computing-software.systems-network-administration.netbox.vrf-unique-ip-space
name: vrf-unique-ip-space
category: computing-software
field: systems-network-administration
product: netbox
tags: [vrf, route-target, enforce-unique]
level: practitioner
status: docs-checked
description: "Model overlapping address space with route distinguishers and uniqueness control."
sources: ["https://netboxlabs.com/docs/netbox/features/ipam/", "https://netboxlabs.com/docs/netbox/configuration/miscellaneous/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VRFs and unique IP space

Goal: keep overlapping address space separate and prevent accidental duplicates.

NetBox models discrete virtual routing and forwarding instances to represent multiple routing tables, including ones with overlapping address space. Prefixes, IP ranges and IP addresses within the hierarchy can each be assigned to a VRF.

**Real-world fidelity.** Each VRF is assigned a standards-compliant route distinguisher. You can also create route targets to manage the import and export of routes between VRFs.

**Uniqueness.** Each VRF is independently configured to permit or prohibit duplicate IP objects. A VRF set to enforce unique space will not allow two `192.0.2.0/24` prefixes. The global table (no VRF) is protected by default; the `ENFORCE_GLOBAL_UNIQUE` configuration parameter can disable that validation.

**Workflow**

1. Create the VRF with its route distinguisher.
2. Create import and export route targets as needed.
3. Assign prefixes and addresses to the VRF when creating them.
4. Enable the unique-space option where overlaps would be a mistake.

**Checklist**

1. One VRF per routing table.
2. RD set on every VRF.
3. Uniqueness enforced unless overlap is intended.

## Checked

Method: docs-checked 2026-11-09 against the NetBox IP Address Management feature page and the miscellaneous configuration page (ENFORCE_GLOBAL_UNIQUE section). Removed the unconfirmed VRF filtering paragraph.
