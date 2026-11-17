---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.instance-storage-selection
name: instance-storage-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, instance-storage, ephemeral-storage, local-nvme, block-storage]
level: practitioner
status: draft
description: "Choose instance (ephemeral NVMe) storage vs network block storage: performance, durability on stop/failure, suitable workloads and how to protect data on local disks."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html", "https://learn.microsoft.com/azure/virtual-machines/managed-disks-overview", "https://cloud.google.com/compute/docs/disks/local-ssd", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Instance (ephemeral) storage vs network storage

## Steps
1. **Know the semantics**: instance store / local SSD / Azure temp and local NVMe disks are
   physically attached, very high IOPS and low latency, but data is lost on stop, terminate,
   host failure or (for some) resize. Network block storage (EBS, Managed Disks, Persistent
   Disk/Hyperdisk) survives instance loss and supports snapshots.
2. **Use local storage for**: caches, scratch/temp space, shuffle and spill (Spark), replicated
   databases where the application replicates (Cassandra, Kafka with replication factor 3,
   Elasticsearch replicas), build workspaces.
3. **Use network storage for**: anything that is the only copy, boot volumes, single-node
   databases, data needing snapshots.
4. **Protect local data**: application-level replication across zones, frequent offload to
   object storage, automation that rebuilds nodes from peers.
5. **Initialise and mount**: local NVMe arrives unformatted; format/mount in user data or
   via Kubernetes local volume provisioners; RAID 0 multiple devices for throughput.
6. **Size network storage** for IOPS/throughput separately (gp3 and Hyperdisk let you
   provision performance independently of size).

## Gotchas
- Stopping an instance with local NVMe discards data; automation that stops/starts for cost wipes it.
- Kubernetes pods using local volumes are pinned to the node; plan for node loss.

## Verify
- [ ] No sole-copy data on ephemeral disks.
- [ ] Node-loss test shows data rebuilt from replicas.
