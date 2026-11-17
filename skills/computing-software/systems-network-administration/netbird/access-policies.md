---
id: computing-software.systems-network-administration.netbird.access-policies
name: access-policies
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, access-policies, default-policy, bidirectional, port-ranges, allow-only]
level: practitioner
status: docs-checked
description: "Design NetBird access control policies: replacing the Default allow-all policy, allow-only semantics, direction, protocols, port ranges and same-group access."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/access-control/manage-network-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies decide which peers or groups can connect, over which protocols and ports, and optionally whether posture checks must pass.

Default policy: new accounts have `Default`, with group `All` as source and destination, a full mesh over any protocol. New policies do not take effect while it is active, so delete it once your restricted policies exist.

Semantics:
- Only ALLOW policies exist; there is no priority or order. A peer's network map follows group membership in existing policies.
- Direction: bidirectional (either side initiates) or unidirectional (only source initiates).
- To let peers in one group talk to each other, add the group as both Source and Destination.
- Protocols and ports can be restricted; since version 0.48 port ranges use `start-end`, such as `8000-9000`.

Create: Access Control > Policies > Add policy; choose source and destination groups, protocol, ports, direction, optional posture checks, name and description.

Manage: click a policy name to edit; toggle the Active switch to disable; Delete to remove.

The Control Center shows an interactive graph of peers, groups and access relationships, helpful for review.

## Checked

2026-11-04. Confirmed against the NetBird manage-network-access docs page: Default policy with All group, allow-only with no priority, direction semantics, same group as source and destination, port ranges from version 0.48, create/edit/disable/delete steps, Control Center graph. Nothing removed.
Method: documentation only; no commands were run.
