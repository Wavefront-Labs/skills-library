---
id: computing-software.database-administration.patroni.patroni-raft-dcs
name: patroni-raft-dcs
category: computing-software
field: database-administration
product: patroni
tags: [patroni, raft, dcs, pysyncobj, deprecated]
level: advanced
status: docs-checked
description: "The deprecated built-in Raft DCS: settings and syncobj_admin operations including two-node setups."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: operate Patroni's embedded Raft consensus.

The Raft section is marked deprecated. Settings:
- `self_addr`: ip:port to listen on for Raft connections; must be reachable by other nodes. If not set, the node does not participate in consensus.
- `bind_addr` (optional): listen address; if absent `self_addr` is used.
- `partner_addrs`: list of other Patroni nodes, ['ip1:port', 'ip2:port'].
- `data_dir`: where the Raft log and snapshot are kept; the current working directory if omitted.
- `password` (optional): encrypts Raft traffic; requires the cryptography Python module.

FAQ from the docs:
- List the nodes providing consensus: `syncobj_admin -conn host:port -status`, using any cluster node's address.
- Remove a node that has gone and whose IP cannot be reused: `syncobj_admin -conn host:port -remove host2:port2`.
- `syncobj_admin` is installed with the pysyncobj module, a Patroni dependency.
- A node can run without joining the consensus by removing or commenting out `raft.self_addr`.
- Two Postgres nodes are possible: run `patroni_raft_controller` (without Patroni and PostgreSQL) on a third node. One node can then be lost temporarily without affecting the primary.

## Checked

2026-11-08: Read the full YAML Configuration Settings page (patroni.readthedocs.io, latest). Confirmed the Raft (deprecated) section: self_addr, bind_addr, partner_addrs, data_dir, password, and every FAQ item. Removed the README sentence about DCS decoupling because that page was not read.

Method: documentation only; no commands were run.
