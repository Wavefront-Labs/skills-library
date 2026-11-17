---
id: computing-software.cloud-infrastructure-engineering.kubespray.add-or-replace-worker-node
name: add-or-replace-worker-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [scale, worker, add-node, scale-yml, facts]
level: practitioner
status: docs-checked
description: "Add a worker with scale.yml and --limit after refreshing facts, then retire the old one with remove-node.yml; includes the offline-node flags."
sources:
  - https://kubespray.io/docs/operations/nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adding or replacing a worker is the simplest case.

1. Add the new node to the inventory.
2. Run `scale.yml`. Use `--limit=NODE_NAME` so other nodes are not disturbed. Before using `--limit`, run the `facts.yml` playbook without a limit to refresh the facts cache for all nodes.
3. To remove the old node, keep it in the inventory and run `remove-node.yml` with `-e node=NODE_NAME`, which limits the run to that node.
4. Remove the node from the inventory.

If the node being removed is offline, add `reset_nodes` and `allow_ungraceful_removal` to the extra vars:

```
-e node=NODE_NAME -e '{"reset_nodes": false, "allow_ungraceful_removal": true}'
```

The page says to use this form even for control plane or etcd nodes that are down. For an offline etcd node also set `ip` or `access_ip` in the inventory, because no facts can be gathered from it.

The same page says `scale.yml` cannot be used to add control plane nodes; those go through `cluster.yml`.

## Checked

2026-11-04. Steps and flag spellings were confirmed on the Adding/replacing a node page, worker section.

Method: documentation only; no commands were run.
