---
id: computing-software.systems-network-administration.netbird.cli-profiles-and-networks
name: cli-profiles-and-networks
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, profiles, networks-select, routes-alias, multi-account]
level: practitioner
status: docs-checked
description: "Use netbird profile and netbird networks commands to switch accounts or management servers and to list, select and deselect routed networks."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Profiles (maintain different accounts in one client):
- `netbird profile list [--show-id]`
- `netbird profile add <name>`: names need not be unique; a unique ID is generated per profile.
- `netbird profile rename`, `remove`, `select`: each takes an exact ID, a unique name or a unique ID prefix. The default profile can be renamed.

`netbird up --profile <name>` and `netbird login --profile <name>` also pick a profile (the last used one if omitted). Installing the service with `--disable-profiles` (or `NB_DISABLE_PROFILES`) locks the client to the profile active at install time.

Networks (replaces the older `routes` command, which still works as an alias):
- `netbird networks list`: all available networks and their selection status.
- `netbird networks select [-a] <network...|all>`: default is replace; `-a` appends to the current selection; `all` clears selections and accepts all, including new networks.
- `netbird networks deselect <network...|all>`.

Installing the service with `--disable-networks` prevents users listing, selecting or deselecting networks (including exit nodes) via CLI or UI.

Example (substitute names from the list output):
```
netbird networks list
netbird networks select -a <network>
```

## Checked

2026-11-04: read the CLI page (get-started/cli) profile, networks and service-install sections. Confirmed subcommands, identifier rules, `--show-id`, replace/append semantics, the routes alias and the install-time disable flags. Corrected `networks list` (it lists all available networks with selection status, not only those routed to this peer) and the claim that every profile subcommand takes an ID (`add` takes a name).

Method: documentation only; no commands were run.
