---
id: computing-software.data-engineering.apache-hadoop.hadoop-cluster-setup-key-properties
name: hadoop-cluster-setup-key-properties
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, configuration, core-site, hdfs-site, yarn-site, mapred-site]
level: practitioner
status: docs-checked
description: "The key site-config properties for a Hadoop cluster across core, hdfs, yarn and mapred: fs.defaultFS, dfs.blocksize, node memory, log aggregation, MapReduce memory and sort."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key properties (ClusterSetup)

Site files are `etc/hadoop/core-site.xml`, `hdfs-site.xml`, `yarn-site.xml` and `mapred-site.xml`; read-only defaults live in the matching `*-default.xml` files.

core-site.xml: `fs.defaultFS` (NameNode URI, `hdfs://host:port/`), `io.file.buffer.size` 131072 (buffer for SequenceFiles).

hdfs-site.xml:
- NameNode: `dfs.namenode.name.dir` (a comma-delimited list replicates the name table in every directory), `dfs.hosts` / `dfs.hosts.exclude` (permitted/excluded DataNodes), `dfs.blocksize` 268435456 (256 MB for large file systems), `dfs.namenode.handler.count` 100 (more RPC threads for many DataNodes).
- DataNode: `dfs.datanode.data.dir` (comma-separated list; data is stored in all directories, typically on different devices).

yarn-site.xml:
- Both daemons: `yarn.acl.enable` (default false), `yarn.admin.acl` (default `*`, anyone; a single space means no one), `yarn.log-aggregation-enable` (false).
- ResourceManager: `yarn.resourcemanager.hostname` (one hostname instead of the per-service `*.address` properties, which override it if set), `yarn.resourcemanager.scheduler.class` (CapacityScheduler recommended, FairScheduler also recommended, or FifoScheduler; fully qualified class name), `yarn.scheduler.minimum-allocation-mb` / `maximum-allocation-mb`, `yarn.resourcemanager.nodes.include-path` / `exclude-path`.
- NodeManager: `yarn.nodemanager.resource.memory-mb`, `yarn.nodemanager.vmem-pmem-ratio`, `yarn.nodemanager.local-dirs` / `log-dirs` (multiple paths spread disk I/O), `yarn.nodemanager.log.retain-seconds` 10800 (only when aggregation is off), `yarn.nodemanager.remote-app-log-dir` /logs and `-suffix` logs (only when aggregation is on; logs go to dir/user/suffix), `yarn.nodemanager.aux-services` = `mapreduce_shuffle`, `yarn.nodemanager.env-whitelist` (add HADOOP_MAPRED_HOME for MapReduce).
- History server: `yarn.log-aggregation.retain-seconds` -1 (disabled; too small a value spams the NameNode) and `retain-check-interval-seconds`.

mapred-site.xml: `mapreduce.framework.name` = yarn; `mapreduce.map.memory.mb` 1536 with `-Xmx1024M`; `mapreduce.reduce.memory.mb` 3072 with `-Xmx2560M`; `mapreduce.task.io.sort.mb` 512; `mapreduce.task.io.sort.factor` 100; `mapreduce.reduce.shuffle.parallelcopies` 50. JobHistory: `mapreduce.jobhistory.address` (port 10020), `.webapp.address` (19888), `intermediate-done-dir` /mr-history/tmp, `done-dir` /mr-history/done.

Most listed values (131072, 256 MB, 100, 1536, 3072, 512, 50) are the page's example settings for large clusters; the page states defaults only where noted above.

## Checked

Method: 2026-11-08 compared against the ClusterSetup page (apache/hadoop trunk markdown source). Property names and values now follow its tables; the draft's `io.sort.factor` is corrected to `mapreduce.task.io.sort.factor`, and the unsupported "Verify" step is removed.
