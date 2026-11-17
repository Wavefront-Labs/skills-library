---
id: computing-software.data-engineering.apache-hadoop.hdfs-replica-placement
name: hdfs-replica-placement
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, replication, rack-awareness, block-placement]
level: practitioner
status: docs-checked
description: "How HDFS places block replicas across racks for replication factor 3 and above, how reads pick a replica, and when replicas are re-created or removed."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDFS replica placement

Block size and replication factor are configurable per file; the factor can be given at creation and changed later. A typical block size is 128 MB. The NameNode does not allow a DataNode to hold multiple replicas of the same block, so the maximum number of replicas is the number of DataNodes at that time. The NameNode learns each DataNode's rack through the Hadoop Rack Awareness process.

Default policy (replication factor 3):
- Replica 1: the local machine if the writer is a DataNode, otherwise a random DataNode in the writer's rack.
- Replica 2: a node in a different (remote) rack.
- Replica 3: a different node in that same remote rack.

This cuts inter-rack write traffic; the page says it does not harm reliability or availability, but a block sits in only two racks, so aggregate read bandwidth is not reduced the way unique-rack placement would allow, and replicas are not evenly spread over racks. For a factor above 3, the 4th and later replicas are placed randomly, keeping replicas per rack below roughly `(replicas - 1) / racks + 2`.

With storage policies, the NameNode picks by rack awareness first, then checks the candidate has the storage type the policy needs, otherwise looks elsewhere and finally uses fallback storage types.

Reads: HDFS tries to read from the replica closest to the reader, preferring one in the reader's rack, and in a multi-data-centre cluster one in the local data centre.

Re-replication: the NameNode initiates it when a DataNode becomes unavailable, a replica is corrupted, a disk fails, or the file's factor is raised. DataNodes without recent Heartbeats are marked dead; the time-out is conservatively long (over 10 minutes by default) to avoid a replication storm from flapping, and a shorter interval can mark nodes stale for performance-sensitive work. When the factor is lowered, the NameNode picks excess replicas and the next Heartbeat tells the DataNode to delete them; free space may appear after a delay.

Writes are pipelined: the client sends data to the first DataNode, which forwards it to the next.

Four pluggable block placement policies are supported; `BlockPlacementPolicyDefault` is the default. `bin/hdfs dfsadmin -printTopology` prints the tree of racks and DataNodes as the NameNode sees it. The page calls the default policy a work in progress.

## Checked

Method: 2026-11-08 compared against the HDFS Design and HDFS User Guide pages (apache/hadoop trunk markdown). Placement rules, formula, reads and re-replication triggers match; the unsupported "Verify: fsck" step was removed and the printTopology and storage-policy details added from the pages.
