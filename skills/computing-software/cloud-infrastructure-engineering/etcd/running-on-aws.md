---
id: computing-software.cloud-infrastructure-engineering.etcd.running-on-aws
name: running-on-aws
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [aws, ec2, ebs, auto-scaling-group, availability-zones, instance-store, deployment, cloud]
level: practitioner
status: docs-checked
description: "Design notes for running etcd on AWS EC2: EBS vs instance storage, spreading over zones and why Auto Scaling Groups need care."
sources:
  - "https://etcd.io/blog/2017/etcd-deployments-on-aws/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

From the EC2 deployment guide (2017 blog post that replaced the old Platforms page).

Capacity planning: etcd is highly available and strongly consistent, so increasing the number of nodes will generally affect performance adversely. The most direct way to raise throughput and lower latency is more disk I/O, network I/O, CPU and memory for the members; scaling the EC2 instances one at a time may improve performance. The etcd hardware recommendation guide helps pick node count and instance type.

Auto Scaling Groups: using an ASG to dynamically scale an etcd cluster is not recommended, because performance is generally inversely proportional to the number of members (synchronous replication), and lifecycle hooks are needed to add and remove members by changing the runtime configuration. ASGs still help with spreading instances across Availability Zones, failing over instances across AZs and consolidated monitoring, and an ASG can keep the desired number of nodes after a node failure (self-healing).

Design criteria:

- Block device: EBS or instance store.
- Topology: how many nodes, and whether to spread them over multiple AZs.
- Member management: a static set of EC2 instances or an ASG.

Availability: for regional high availability a cluster needs at least three members with the instances spread over at least two AZs. Collocating members in one AZ (EC2 Placement Groups) cuts network latency but gives weaker fault tolerance.

Disk: EBS volumes are network attached and have a lifecycle independent of the instance (they can be detached and snapshotted). Instance store is attached to the host, has lower latency and higher throughput, but its lifecycle follows the instance. Inconsistent EBS performance can cause etcd instability; provisioned IOPS gives more consistent performance than general purpose SSD volumes.

Data durability: replication across members, point-in-time etcd snapshots (cheap enough to run frequently and store in S3), and EBS.

## Checked
2026-11-08: confirmed against the etcd EC2 deployment guide (capacity planning, ASG caveats, design criteria, availability, durability, network, disk, self-healing). Removed: the 3-node 3-zone zone-loss claim, security group ports 2379 and 2380, the same-region advice and the claim that EBS gives quicker member recovery (the page does not state them).
Method: documentation only; no commands were run.
