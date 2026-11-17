---
id: computing-software.data-engineering.apache-hadoop.hdfs-erasure-coding-policies
name: hdfs-erasure-coding-policies
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, erasure-coding, reed-solomon, storage-efficiency]
level: advanced
status: docs-checked
description: "HDFS erasure coding: built-in RS and XOR policies, the RS-6-3-1024k default, hdfs ec commands, cluster size needs, tuning keys, and limits on EC files."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Erasure coding

EC storage overhead is typically no more than 50%, against 200% for 3x replication: a 6-block file at 3x uses 18 blocks, but with EC (6 data, 3 parity) only 9. The replication factor of an EC file is always 1 and cannot be changed with `-setrep`.

Built-in policies (named codec-data-parity-cellsize): `RS-3-2-1024k`, `RS-6-3-1024k`, `RS-10-4-1024k`, `RS-LEGACY-6-3-1024k`, `XOR-2-1-1024k`. `REPLICATION` is always enabled and can only be set on a directory, forcing 3x replication instead of inheriting an EC ancestor policy. All built-in EC policies are disabled except the one in `dfs.namenode.ec.system.default.policy` (default `RS-6-3-1024k`), which `-setPolicy` also uses when no policy is named.

Policies are set on directories; a new file inherits its nearest ancestor's policy. Existing files keep their policy (even if renamed into a directory with a different one); to convert, rewrite the data, e.g. by copying with distcp.

```
hdfs ec -setPolicy -path <dir> [-policy <name>] [-replicate]   # -policy and -replicate are mutually exclusive
hdfs ec -getPolicy -path <path>
hdfs ec -unsetPolicy -path <dir>
hdfs ec -listPolicies
hdfs ec -enablePolicy -policy <name>     # also -disablePolicy, -removePolicy (user-defined)
hdfs ec -addPolicies -policyFile <file>  # see user_ec_policies.xml.template; max cell size 4MB by default
hdfs ec -listCodecs
hdfs ec -verifyClusterSetup [-policy <name>...]
```

Cluster needs: at least as many DataNodes as the stripe width (9 for RS(6,3)); extra CPU on clients and DataNodes; good network bisection bandwidth since most operations are off-rack. For rack fault tolerance you need (data + parity) / parity racks, rounded up: 3 for RS(6,3), ideally 9 or more. RS-10-4 for node-level tolerance needs at least 14 DataNodes.

Tuning (DataNode reconstruction): `dfs.datanode.ec.reconstruction.threads` (8), `...stripedread.timeout.millis` (5000), `...stripedread.buffer.size` (64KB), `...xmits.weight` (0.5). Codecs are chosen with `io.erasurecode.codec.rs.rawcoders`, `rs-legacy`, `xor`. ISA-L native acceleration needs ISA-L built into Hadoop and present on clients and DataNodes; check with `hadoop checknative`.

Limits: `append()` and `truncate()` throw IOException (append with the `NEW_BLOCK` flag to a closed striped file is supported); `concat()` throws on mixed policies or replicated files; `setReplication()` is a no-op; `hflush()`/`hsync()` are no-ops, so no persistence guarantee. For such needs create the file as 3x replicated in a non-EC directory, or use `FSDataOutputStreamBuilder#replicate()`.

## Checked

Method: 2026-11-08 compared against the HDFS Erasure Coding page (apache/hadoop trunk markdown, read in full). Policies, commands, defaults, rack formula and limits match; the NEW_BLOCK append exception, concat limit and command details were added, and the invented "Verify" step removed.
