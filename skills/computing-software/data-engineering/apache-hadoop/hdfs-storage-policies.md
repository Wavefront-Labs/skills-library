---
id: computing-software.data-engineering.apache-hadoop.hdfs-storage-policies
name: hdfs-storage-policies
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, storage-policy, tiering, mover, archive]
level: advanced
status: docs-checked
description: "HDFS heterogeneous storage: storage types, the Hot, Warm, Cold, All_SSD and other policies, tagging dfs.datanode.data.dir, storagepolicies commands and the mover."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ArchivalStorage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage policies

Storage types: DISK (default), SSD, ARCHIVE (dense, little compute), RAM_DISK (single-replica in-memory writes) and, from Hadoop 3.4, NVDIMM. Tag each location in `dfs.datanode.data.dir`, e.g. `[SSD]file:///grid/dn/ssd0`, `[ARCHIVE]file:///grid/dn/archive0`; an untagged location is DISK. `dfs.datanode.storagetype.*.filesystem` can enforce a filesystem for a storage type.

Policies (ID; n = replicas; block placement):
- Lazy_Persist (15): RAM_DISK 1, DISK n-1; useful only for single-replica blocks, otherwise all replicas go to DISK
- All_NVDIMM (14): NVDIMM n
- All_SSD (12): SSD n
- One_SSD (10): SSD 1, DISK n-1
- Hot (7, default): DISK n
- Warm (5): DISK 1, ARCHIVE n-1
- Cold (2): ARCHIVE n
- Provided (1): PROVIDED 1, DISK n-1

Each policy also has fallback storage lists for file creation and for replication, used when a type is out of space. Striped erasure-coded files follow only All_SSD, Hot, Cold and All_NVDIMM.

Resolution: a new file or directory has an unspecified policy and inherits its parent's effective policy; the root falls back to the default (`dfs.storage.default.policy`, default HOT). `dfs.storage.policy.enabled` defaults to true.

```
hdfs storagepolicies -listPolicies
hdfs storagepolicies -setStoragePolicy -path <path> -policy <policy>
hdfs storagepolicies -getStoragePolicy -path <path>
hdfs storagepolicies -unsetStoragePolicy -path <path>   # nearest ancestor's policy then applies
hdfs storagepolicies -satisfyStoragePolicy -path <path>
hdfs mover [-p <files/dirs> | -f <local file name>]     # default path is root
```

Setting a policy changes the namespace only; it does not move existing blocks. Two options move them, and they cannot run simultaneously:
- Mover: scans, and moves replicas that violate the policy, preferring within the same node and otherwise copying over the network.
- Storage Policy Satisfier (SPS): `dfs.storage.policy.satisfier.mode` is `external` or `none` (default). After changing it, run `hdfs dfsadmin -reconfig namenode <host:ipc_port> start`; start the external service with `hdfs --daemon start sps`. If a Mover is running, SPS is disabled at start; to run the Mover, disable SPS first.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (ArchivalStorage.md in the apache/hadoop repo). Added NVDIMM and All_NVDIMM (omitted before, including from the erasure-coding list), SPS procedure and fallback lists; removed an unsupported "Verify" fsck step.
