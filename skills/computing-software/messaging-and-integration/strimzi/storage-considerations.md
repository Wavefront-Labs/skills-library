---
id: computing-software.messaging-and-integration.strimzi.storage-considerations
name: storage-considerations
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [block-storage, xfs-ext4, disk-usage]
level: practitioner
status: docs-checked
description: "Pick suitable block storage and file systems for Kafka brokers."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storage considerations

**Goal:** avoid unstable broker storage.

Strimzi has been tested with **block storage** as primary broker storage and strongly recommends it. File-system storage such as NFS is not guaranteed to work and may cause stability or performance issues. Supported block storage types include cloud block storage (Amazon EBS, Azure Disk Storage, Google Persistent Disk), local persistent volumes on bare metal, and SAN volumes over Fibre Channel or iSCSI. Strimzi does not require Kubernetes raw block volumes.

File systems: Strimzi is compatible with **XFS and ext4**.

Disk notes from the docs:

- SSDs are not essential but can improve performance in large clusters with many topics handled asynchronously.
- Replicated storage is not required, because Kafka provides built-in data replication.
- With tiered storage, primary storage (PVs or JBOD) holds recent data and remote storage such as object storage holds historical data. Custom tiered storage plugins must be validated for performance and compatibility before production.

```bash
kubectl get pvc -n my-namespace
kubectl get storageclass
```

**Checklist**

1. Use block storage, not NFS.
2. Use XFS or ext4.
3. Do not rely on storage-level replication; it is not required because Kafka replicates data.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Storage considerations section: block storage, file systems, tiered storage, disk usage). The kubectl listing commands are generic and not from the page.
