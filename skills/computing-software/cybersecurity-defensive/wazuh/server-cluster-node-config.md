---
id: computing-software.cybersecurity-defensive.wazuh.server-cluster-node-config
name: server-cluster-node-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [cluster, node-type, master, worker, cluster-control, bind-addr]
level: advanced
status: docs-checked
description: "Configure a Wazuh server cluster node: cluster block fields, the shared 32-character key, one master only, and cluster_control to verify."
sources:
  - https://documentation.wazuh.com/current/user-manual/wazuh-server-cluster/cluster-nodes-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each node's `<cluster>` block in `/var/ossec/etc/ossec.conf` contains:
- `name`: cluster name (example `wazuh`).
- `node_name`: this server node's name.
- `node_type`: `master` or `worker`. Only one master is allowed.
- `key`: 32-character hex key, identical on all nodes. Generate with `openssl rand -hex 16`.
- `port`: cluster communication port (example 1516).
- `bind_addr`: IP the node listens on (`0.0.0.0` or a specific address).
- `nodes/node`: master address (IP or DNS). Include it on every node, including the master.
- `hidden`: toggles whether information about the cluster that generated an alert is shown.
- `disabled`: whether the Wazuh server is enabled in the cluster.

Apply with `systemctl restart wazuh-manager` on each node. Verify with `/var/ossec/bin/cluster_control -l`, which prints NAME, TYPE, VERSION and ADDRESS columns per node.

Gotchas:
- Changes to the master's `ossec.conf` are not synchronized to workers automatically. Replicate them manually and restart the nodes.
- The key must be the same on every node (master and workers).
- Restart each node after editing its own configuration.
- The `nodes/node` address can be an IP or a DNS name.

## Checked

2026-11-08: confirmed against the Wazuh cluster nodes configuration page (read in full): fields, one-master rule, key generation, restart and cluster_control output columns. Removed the unsupported "nodes will not join" consequence and the node-name and DNS-stability tip.
Method: documentation only; no commands were run.
