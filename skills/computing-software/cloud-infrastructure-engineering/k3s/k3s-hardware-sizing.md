---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-hardware-sizing
name: k3s-hardware-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, server-sizing, agents-per-server, large-clusters]
level: practitioner
status: docs-checked
description: "Minimum CPU and RAM for K3s servers and agents, agent-count sizing, and database sizing for large clusters."
sources:
  - https://docs.k3s.io/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size nodes and the datastore.

Minimums (excluding workload): server 2 cores and 2 GB RAM; agent 1 core and 512 MB.

Server sizing by agent count:

- 2 CPU, 4 GB: 0-350 agents
- 4 CPU, 8 GB: 351-900
- 8 CPU, 16 GB: 901-1800
- 16+ CPU, 32 GB: 1800+

With HA of 3 servers, agents can scale roughly 50% more; for example 3 servers with 4 vCPU/8 GB scale to about 1200 agents. Join agents in batches of 50 or fewer because CPU spikes at join. Change the default cluster-cidr if you want more than 255 nodes.

Disks: K3s performance depends on database performance, so use SSDs. On Raspberry Pi or other ARM, use an external SSD: etcd is write intensive and SD cards and eMMC cannot handle the IO.

Large clusters: use HA with an external database (MySQL, PostgreSQL or etcd). Enlarge the cluster CIDR with --cluster-cidr so pods do not run out of IPs. Database sizing:

- Small: up to 10 nodes, 1 vCPU, 2 GB
- Medium: up to 100 nodes, 2 vCPU, 8 GB
- Large: up to 250 nodes, 4 vCPU, 16 GB
- X-Large: up to 500 nodes, 8 vCPU, 32 GB
- XX-Large: 500+ nodes, 16 vCPU, 64 GB

## Checked

2026-11-03: read docs.k3s.io installation/requirements. Confirmed: server 2 cores/2 GB and agent 1 core/512 MB minimums, the agent-count sizing table, the ~50% HA scaling and ~1200 agents example, joining in batches of 50, the 255-node cluster-cidr note, SSD and external SSD advice, and the database sizing table (Small to XX-Large).

Method: documentation only; no commands were run.
