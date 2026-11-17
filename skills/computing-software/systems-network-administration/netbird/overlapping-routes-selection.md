---
id: computing-software.systems-network-administration.netbird.overlapping-routes-selection
name: overlapping-routes-selection
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, overlapping-routes, route-selection, networks-select, desktop-app-resources]
level: practitioner
status: docs-checked
description: "Resolve overlapping NetBird routes on a client by selecting which route to use via CLI or desktop app; requires client 0.27.4 or later."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/overlapping-routes.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When several routes share one IP range (overlapping VPCs or office LANs), the client needs to know which to use. Requires client 0.27.4+.

CLI (the page documents the `routes` command):
- `netbird routes list`: route ID, range, whether selected.
- `netbird routes select <route-id>`: selects it and deselects others.
- `netbird routes select route1 route2`: several at once.
- `netbird routes select -a route3`: add without deselecting.
- `netbird routes select all`: default behaviour, including routes added later.
- `netbird routes deselect all`: turn off every route, including future ones.

Desktop app: Advanced view > Resources > apply the Overlapping filter > toggle the resources you want; search by name; Enable all or Disable all for bulk.

Example: two AWS VPCs both using 172.17.0.0/16 with both routes selected conflict. Select only the one you need, e.g. `aws-vpc-ireland`.

## Checked

2026-11-04. Confirmed against the NetBird overlapping routes page: 0.27.4 requirement, `routes list`, `routes select` variants including `-a`, `all` and `deselect all`, desktop app Resources steps, Ireland and Ohio example. Removed the claim that the current CLI also exposes this as `networks`, which the page does not state.
Method: documentation only; no commands were run.
