---
id: computing-software.data-engineering.apache-hadoop.hadoop-daemon-environment-hadoop-env
name: hadoop-daemon-environment-hadoop-env
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hadoop-env, jvm, heap, daemon-options, configuration]
level: practitioner
status: docs-checked
description: "Setting Hadoop daemon environment in hadoop-env.sh: JAVA_HOME, per-daemon _OPTS variables, HADOOP_HEAPSIZE_MAX precedence, pid and log directories, and the config file layout."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemon environment

Config: read-only defaults are `core-default.xml`, `hdfs-default.xml`, `yarn-default.xml`, `mapred-default.xml`; site files are `etc/hadoop/core-site.xml`, `hdfs-site.xml`, `yarn-site.xml`, `mapred-site.xml`. Script environment is set in `etc/hadoop/hadoop-env.sh` and optionally `mapred-env.sh` and `yarn-env.sh`. Logging is customised in `etc/hadoop/log4j.properties`; `etc/hadoop/workers` lists worker hosts for helper scripts.

In hadoop-env.sh:
- `JAVA_HOME`: at the very least you must specify it, correctly defined on each remote node.
- Per-daemon options: `HDFS_NAMENODE_OPTS` (example `-XX:+UseParallelGC -Xmx4g`), `HDFS_DATANODE_OPTS`, `HDFS_SECONDARYNAMENODE_OPTS`, `YARN_RESOURCEMANAGER_OPTS`, `YARN_NODEMANAGER_OPTS`, `YARN_PROXYSERVER_OPTS`, `MAPRED_HISTORYSERVER_OPTS`.
- `HADOOP_HEAPSIZE_MAX`: maximum heap; JVM-supported units work, a bare number is MB; by default the JVM decides. It can be overridden per daemon with the matching `_OPTS` variable: the page's example sets `HADOOP_HEAPSIZE_MAX=1g` and `HADOOP_NAMENODE_OPTS="-Xmx5g"` and states this gives the NameNode 5 GB.
- `HADOOP_PID_DIR` and `HADOOP_LOG_DIR`: pid and log directories (logs are created if missing). In most cases make them writable only by the users running the daemons, otherwise a symlink attack is possible.

It is traditional to set `HADOOP_HOME` in the system-wide shell environment, for example a script under /etc/profile.d.

## Checked

Method: 2026-11-08 compared against the ClusterSetup page (apache/hadoop trunk markdown). Variable names and the heap precedence example match; the unsupported "Verify: ps" step and the claim that HADOOP_HOME is "not set in hadoop-env.sh" were dropped.
