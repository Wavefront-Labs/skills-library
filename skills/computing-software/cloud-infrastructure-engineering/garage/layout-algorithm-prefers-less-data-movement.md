---
id: computing-software.cloud-infrastructure-engineering.garage.layout-algorithm-prefers-less-data-movement
name: layout-algorithm-prefers-less-data-movement
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [layout-algorithm, usable-capacity, zone-redundancy, partition-assignment]
level: advanced
status: docs-checked
description: "Explain surprising layout results, such as a new node getting no data, and fix them by splitting capacity."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The layout algorithm prioritises moving as little data as possible over equalising load, and when it must move data it uses all node-to-node links in similar proportions. Results can look odd but are intended.

Documented example 1: three equal nodes in three zones (dc1 to dc3) each hold a full copy. A fourth equal node is added to dc1. `garage layout show` reports it with `0 B (0.0%)` usable capacity and "0 new copies of partitions need to be transferred". Reason: dc2 and dc3 still each need a full copy and their capacity is unchanged, so extra space in dc1 adds no storable data and moving data has a cost.

If the real goal was to halve the load of the slow old node, give each dc1 node only half the capacity (500M instead of 1G). Garage then needs 500M on each to store 1G.

Example 2: two dc1 nodes at 50% each, one node each in dc2 and dc3 at 100%. Moving a dc1 node to dc3 does not just swap roles. The remaining dc1 node must hold everything, so data is pulled equally from node3 and the moved node4. Result: node3 about 75% used, node4 about 25%, with 128 new copies to transfer.

The "COMPUTATION OF A NEW PARTITION ASSIGNATION" part of the `garage layout show` output lists partitions per zone and the effective capacity.

## Checked

2026-11-04. Read the Cluster layout management page in full. Confirmed both worked examples, their figures (0 B usable, 0 and 128 new copies, 75 and 25 percent), the explanations and the half-capacity remedy. Nothing removed.
Method: documentation only; no commands were run.
