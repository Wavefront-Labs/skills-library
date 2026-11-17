---
id: computing-software.cloud-infrastructure-engineering.netdata.ephemeral-nodes
name: ephemeral-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, ephemeral-node, remove-stale-node, disconnect-alerts]
level: practitioner
status: docs-checked
description: "Handle disconnects of short-lived nodes: mark them ephemeral in netdata.conf, understand the 24 hour removal, and force-forget nodes with netdatacli."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/faq.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/nodes-ephemerality.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Permanent nodes are the default: a disconnect triggers an alert, and Netdata Cloud sends disconnection notifications.

For autoscaling or short-lived nodes, set on the node in `netdata.conf`:

```
[global]
    is ephemeral node = yes
```

The setting propagates to Parents and Cloud. A Parent removes an ephemeral node that stays disconnected for more than 24 hours; if it reconnects it is revived with its data.

Force a node into the forgotten state by running this on the Parent it is connected to (or a previous Parent):

```
netdatacli remove-stale-node <node_id | machine_guid | hostname | ALL_NODES>
```

Set the option in the node's `netdata.conf`, then restart the Netdata Agent.

Keep history queryable and clear active alerts instead of deleting: `netdatacli mark-stale-nodes-ephemeral <node_id | machine_guid | hostname | ALL_NODES>`.

On Parents, `[db] cleanup ephemeral hosts after = 1d` auto-removes ephemeral nodes (restart after editing). The `streaming_never_connected` and `streaming_disconnected` alerts default to `to: silent` and apply only to permanent nodes.

Gotchas:
- A node marked ephemeral via CLI reverts to permanent if it reconnects without ephemeral config.
- A deleted child is recreated on reconnect; its history on the Parent stays accessible.

## Checked

2026-11-04. Confirmed against the Netdata Nodes ephemerality page and the metrics centralization FAQ: permanent as the default, the [global] setting and restart, propagation to Parents and Cloud, the 24-hour removal and revival, remove-stale-node and mark-stale-nodes-ephemeral syntax, cleanup ephemeral hosts after = 1d, the silent streaming alerts, the revert-to-permanent behaviour and node recreation. Removed the invented confirm step and the ALL_NODES gotcha.

Method: documentation only; no commands were run.
