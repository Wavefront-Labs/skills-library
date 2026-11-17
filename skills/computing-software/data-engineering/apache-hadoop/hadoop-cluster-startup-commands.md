---
id: computing-software.data-engineering.apache-hadoop.hadoop-cluster-startup-commands
name: hadoop-cluster-startup-commands
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, startup, daemons, workers, namenode-format, web-ports]
level: intro
status: docs-checked
description: "Starting a Hadoop cluster: format the NameNode, per-daemon start commands for HDFS, YARN and the JobHistory Server, the workers file, and default web UI ports."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Starting the cluster

Run as the named user with `$HADOOP_HOME` set. The page recommends HDFS and YARN run as separate users (typically `hdfs` and `yarn`), and the history server as `mapred`.

```
$HADOOP_HOME/bin/hdfs namenode -format              # first time only (hdfs)
$HADOOP_HOME/bin/hdfs --daemon start namenode       # hdfs
$HADOOP_HOME/bin/hdfs --daemon start datanode       # hdfs, on each worker
$HADOOP_HOME/bin/yarn --daemon start resourcemanager  # yarn
$HADOOP_HOME/bin/yarn --daemon start nodemanager      # yarn, each worker
$HADOOP_HOME/bin/yarn --daemon start proxyserver      # WebAppProxy (each server if load balanced)
$HADOOP_HOME/bin/mapred --daemon start historyserver  # mapred
```

Helpers `sbin/start-dfs.sh` and `sbin/start-yarn.sh` start all processes of HDFS or YARN respectively (`stop-dfs.sh` / `stop-yarn.sh` stop them); they read `etc/hadoop/workers` (one hostname or IP per line) and need SSH trust (passphraseless ssh or e.g. Kerberos) for the accounts running Hadoop. The workers file is not used for Java-based Hadoop configuration. Stopping an individual daemon uses `--daemon stop`.

Default web UIs: NameNode 9870, ResourceManager 8088, JobHistory Server 19888. The page says to check these UIs once the cluster is up.

## Checked

Method: 2026-11-08 compared against the ClusterSetup page (apache/hadoop trunk markdown). Commands, users and ports match; the draft's invented "Verify" step was removed and shutdown and user notes added from the page.
