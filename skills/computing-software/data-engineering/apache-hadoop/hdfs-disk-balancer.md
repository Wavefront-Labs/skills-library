---
id: computing-software.data-engineering.apache-hadoop.hdfs-disk-balancer
name: hdfs-disk-balancer
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, diskbalancer, datanode, disks, balancing]
level: advanced
status: docs-checked
description: "HDFS Disk Balancer for evening data across disks within one DataNode: plan, execute, query, cancel, report, and the dfs.disk.balancer.* defaults."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSDiskbalancer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk Balancer

Distributes data evenly across the disks of one DataNode; the cluster-wide Balancer is a different tool. Unevenness comes from heavy writes and deletes or a disk replacement. It builds a plan (move steps of source disk, destination disk and bytes) and executes it on an operational DataNode, throttling copy rate. The page says it is enabled by default.

```
hdfs diskbalancer -plan <datanode> [-out] [-bandwidth] [-thresholdPercentage] [-maxerror] [-v] [-fs]
hdfs diskbalancer -execute /system/diskbalancer/<nodename>.plan.json [-skipDateCheck]
hdfs diskbalancer -query <node1>,<node2>,... [-v]
hdfs diskbalancer -cancel <plan.json>        # or: -cancel <planID> -node <nodename>
hdfs diskbalancer -fs http://namenode.uri -report -node <file://>|<DataNodeID|IP|Hostname>,...
hdfs diskbalancer -fs http://namenode.uri -report -top <topnum>
```

`-plan` writes `<nodename>.before.json` (cluster state read from the NameNode) and `<nodename>.plan.json`. Execute is asynchronous and can take a long time; use `-query` for status (`-v` shows each move step). The plan ID can be read from the DataNode with query. Cancelling is equivalent to restarting the DataNode, since plan information there is transient. `-skipDateCheck` forces execution regardless of the plan's date check. `-thresholdPercentage` sets the tolerance within which a move counts as successful, e.g. 18 GB of a 20 GB move at 10%.

Settings in hdfs-site.xml:
- `dfs.disk.balancer.enabled`: default true; if false, the DataNode rejects execute
- `dfs.disk.balancer.max.disk.throughputInMBperSec`: default 10 MB/s
- `dfs.disk.balancer.max.disk.errors`: default 5; a move exceeding it is abandoned and the next step starts
- `dfs.disk.balancer.block.tolerance.percent`: when a copy step is good enough (10% in the page's example and default case)
- `dfs.disk.balancer.plan.threshold.percent`: volume data density threshold, default 10
- `dfs.disk.balancer.plan.valid.interval`: plan validity, default 1d

All moves run sequentially on a single thread; after each block it sleeps if the move was faster than the bandwidth would allow.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HDFSDiskbalancer.md in the apache/hadoop repo). Added the cancel-by-ID and report forms, removed an unsupported "Verify" step.
