---
id: computing-software.cloud-infrastructure-engineering.graylog.install-multi-node-cluster
name: install-multi-node-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [multi-node, conventional-model, load-balancer, cluster, high-availability]
level: advanced
status: docs-checked
description: "Install a multi-node Graylog cluster (Conventional model: three Graylog/MongoDB nodes, three Data Nodes) with a load balancer."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/debian_installation_multi_node.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/configuration_settings.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install multi node cluster

The Debian 12 multi-node guide targets more than one Graylog and MongoDB node and more than one Data Node. The Conventional model (three Graylog and MongoDB nodes, three Data Nodes) fits most medium-to-large deployments, and the steps scale to other sizes.

Prerequisites: required ports open, a load balancer with a DNS record for Graylog is encouraged, XFS recommended.

Install MongoDB, Data Node and Graylog as in the single-node guide, with a MongoDB replica set across the MongoDB nodes. A connectivity problem while initiating the replica set may stem from DNS, firewall or TCP config; test TCP 27017 with `nc -vz <node_ip> 27017`.

Configuration consistency: some properties appear in both `server.conf` and `datanode.conf`, and each node has its own copy of both files. `password_secret` must be identical on every Graylog and Data Node node. The configuration page says some settings must match across nodes and others differ. On additional Graylog nodes set `is_leader = false`, and use the same `root_password_sha2`.

## Checked

2026-11-04. Confirmed against the Debian 12 multi-node guide and the configuration page. Removed: the claims that per-node values such as node_name must be unique and that changing password_secret invalidates sessions, which the pages do not state. Added is_leader and root_password_sha2 notes.

Method: documentation only; no commands were run.
