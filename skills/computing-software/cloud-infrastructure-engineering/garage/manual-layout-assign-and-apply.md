---
id: computing-software.cloud-infrastructure-engineering.garage.manual-layout-assign-and-apply
name: manual-layout-assign-and-apply
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-layout-assign, layout-apply, node-id, zone-capacity]
level: intro
status: docs-checked
description: "Give a fresh node a zone and capacity with garage layout assign and activate it with garage layout apply --version 1."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without the automatic flags, a freshly started node shows `NO ROLE ASSIGNED` in `garage status`. Building a layout tells Garage how much disk each node offers (`-c`) and which zone, for example a datacenter, it sits in (`-z`).

For the test node the guide runs:

`garage layout assign -z dc1 -c 1G <node_id>`

The node ID is the first column of `garage status`, and a prefix is enough, so `563e` can stand for the whole identifier. The capacity is ignored on a single-node deployment and can be changed later when nodes are added. Then activate the layout:

`garage layout apply --version 1`

The CLI needs to know where the configuration file is. Use `GARAGE_CONFIG_FILE`, or pass `-c` as in `garage -c ./garage.toml status`, when the file is not at `/etc/garage.toml`. For a containerised node, define `alias garage="docker exec -ti <container name> /garage"`.

The tool documents itself: `garage help` and `garage bucket allow --help` work anywhere.

This manual route is equivalent to `--single-node`, and it is the only route on Garage releases before v2.3.0.

## Checked

2026-11-04. Read the Quick Start page in full. Confirmed the NO ROLE ASSIGNED state, the assign and apply commands, the prefix rule, the ignored capacity, the config file options, the alias, the help commands and the v2.3.0 boundary. Removed the closing claim about what garage status shows after apply, which the page does not show.
Method: documentation only; no commands were run.
