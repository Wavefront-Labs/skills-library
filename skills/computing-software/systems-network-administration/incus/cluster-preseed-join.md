---
id: computing-software.systems-network-administration.incus.cluster-preseed-join
name: cluster-preseed-join
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cluster, preseed, member-config, cluster-token, automation]
level: advanced
status: docs-checked
description: "Automate Incus cluster formation with per-server preseed files: bootstrap keys and joiner keys (server_address, cluster_token, member_config)."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/cluster_form.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster preseed

Each server needs its own file: `cat <preseed-file> | incus admin init --preseed`.

Bootstrap server:
- `config.core.https_address`
- `cluster.server_name` and `cluster.enabled: true`
- storage pools, networks and profiles as needed

Joining server:
- `cluster.enabled: true`
- `cluster.server_address`
- `cluster.cluster_token`
- `member_config` entries for member-specific settings, such as storage pool sources and drivers

Generate the token with `incus cluster add <name>` on an existing member.

## Checked

2026-11-09. Confirmed against the Incus doc howto/cluster_form.md (Configure the cluster through preseed files): one file per server, required bootstrap and joiner fields, member_config and the token command. Removed: nothing needed removing.

Method: documentation only; no commands were run.
