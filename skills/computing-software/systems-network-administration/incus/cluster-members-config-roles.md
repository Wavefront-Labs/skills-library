---
id: computing-software.systems-network-administration.incus.cluster-members-config-roles
name: cluster-members-config-roles
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cluster, members, cluster-set, roles, event-hub, max-voters, cluster-edit]
level: practitioner
status: docs-checked
description: "Inspect and configure Incus cluster members: cluster list/show/info, global vs local options, cluster set, role add and cluster edit."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/cluster_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster members and config

```
incus cluster list
incus cluster show <member>
incus cluster info <member>
incus config set cluster.max_voters=5
incus cluster set <member> scheduler.instance=manual
incus cluster role add server1 event-hub
incus cluster edit <member>
```

- `list` shows roles, architecture, failure domain and status; `info` shows state and usage.
- Global options propagate through the distributed database. Local options affect only the server they are set on, or the one chosen with `--target`.
- `cluster edit` covers member config, roles, failure domain and cluster groups.
- Only roles that Incus does not assign automatically can be changed.

## Checked

2026-11-09. Confirmed against the Incus doc howto/cluster_manage.md (top sections): list, show and info commands, global versus local options, cluster set, role add, cluster edit scope and the automatic-role note. Removed: nothing needed removing.

Method: documentation only; no commands were run.
