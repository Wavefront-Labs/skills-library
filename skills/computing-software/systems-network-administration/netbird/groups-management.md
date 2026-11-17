---
id: computing-software.systems-network-administration.netbird.groups-management
name: groups-management
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, groups, all-group, auto-grouping, idp-synced-groups]
level: intro
status: docs-checked
description: "Create and manage NetBird groups: tag-like semantics, the immutable All group, assigning peers, auto-assignment via setup keys or IdP sync, and delete restrictions."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/access-control/manage-network-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Groups work like tags: names are unique, a group holds many peers and a peer can be in several. Groups serve as policy Source or Destination.

The `All` group automatically contains every peer and cannot be modified or deleted.

Create: type a name into any group input field and press Enter, or Access Control > Groups > Create Group.

Assign: a new group does nothing until peers are added. Open the peer in Peers and pick the group under Assigned Groups.

Automatic assignment: setup keys can auto-assign groups at registration, and identity provider sync can assign them. NetBird recommends IdP integration for managing user groups.

Rename or delete from the three-dot menu on the Groups page, with restrictions:
- Groups synced from an identity provider cannot be renamed or deleted.
- A group with active dependencies cannot be deleted until they are removed.

## Checked

2026-11-04. Confirmed against the NetBird manage-network-access page: tag-like groups, All group, creation, assignment, rename and delete steps and restrictions, IdP recommendation. Removed the design tip about routed network resources and All, and the list of dependency types, which the page does not state.
Method: documentation only; no commands were run.
