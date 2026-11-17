---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-diskpool-create-and-device-links
name: mayastor-diskpool-create-and-device-links
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, diskpool, device-links, by-id, aio, uring, maxexpansion, topology, pool]
level: advanced
status: docs-checked
description: "Create Replicated PV Mayastor DiskPools: one disk per pool, stable by-id device links, aio or uring schemes, pool count versus replica count, and optional topology labels."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/configuration/rs-create-diskpool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A node allocates capacity for a volume replica from a **DiskPool**. A node may host zero, one or several pools, a pool is owned exclusively by one node, and **a pool manages exactly one block device**, which sets its maximum capacity. You define a pool declaratively with a `DiskPool` custom resource in the **same namespace** where Replicated PV Mayastor is deployed. Its fields include a unique name, the node name and the disk reference.

**Device references.** Use a link that survives reboots, such as `by-id` or `by-path`, and not `/dev/sdx`: a changed device name after a reboot can cause data corruption. `kubectl mayastor get block-devices <node>` lists candidates. The documented forms are `aio:///dev/disk/by-id/<id>` or `uring:///dev/disk/by-id/<id>` (best practice), plain `/dev/sdx`, `aio:///dev/sdx` and `uring:///dev/sdx`.

**Exclusive use.** Once pooled, the device must not be partitioned, formatted or shared; any data already on it is destroyed. A RAM drive is not for production, and its memory comes from hugepages, so allocate extra hugepages on nodes using one.

**How many pools.** At least one pool is required. The number of pools limits the replication factor you can configure, so have at least as many pools (on separate nodes) as the highest `repl` you plan to use.

**`maxExpansion`** (optional) sets the largest size the pool may grow to, as a factor such as `5x` or an absolute size such as `6TiB`. It **cannot be changed after creation**, and the default `1x` means no growth.

**Topology labels.** To use pool-based placement parameters, label pools either at creation under `spec.topology.labelled` or later with `kubectl mayastor label pool <pool> key=value -n openebs`, which does not affect existing volumes.

## Checked

2026-11-04. Confirmed against the Create DiskPool(s) page: one device per pool, same-namespace rule, device link forms, exclusive-use and RAM drive warnings, the pool-count guidance, `maxExpansion` rules and default, and both labelling routes. Nothing removed.

Method: documentation only; no commands were run.
