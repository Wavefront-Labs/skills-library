---
id: computing-software.data-engineering.apache-spark.standalone-cluster-manager
name: standalone-cluster-manager
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-standalone, cluster-manager, spark-master, spark-worker, zookeeper-recovery, spark-architecture]
level: practitioner
status: docs-checked
description: "Run Spark's built-in standalone cluster manager: start master and workers, size worker cores/memory, submit in client vs cluster mode, and make the master highly available."
sources:
  - https://spark.apache.org/docs/latest/spark-standalone.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark standalone cluster manager

**Use when:** you need a Spark cluster without YARN or Kubernetes (on-prem boxes, a lab, a single big VM).

## Start it
```bash
$SPARK_HOME/sbin/start-master.sh                      # web UI :8080 and service port 7077 by default
$SPARK_HOME/sbin/start-worker.sh spark://<master>:7077 # on every worker host
# or list hosts in conf/workers and run sbin/start-all.sh from the master (the master reaches workers over ssh)
```
`conf/spark-env.sh` on each worker:
```bash
SPARK_WORKER_CORES=30        # total cores applications may use on this machine (default: all)
SPARK_WORKER_MEMORY=110g     # total memory applications may use (default: total minus 1 GiB)
SPARK_WORKER_DIR=/data/spark/work   # application logs and scratch space (default SPARK_HOME/work)
SPARK_WORKER_OPTS="-Dspark.worker.cleanup.enabled=true -Dspark.worker.cleanup.appDataTtl=604800"
SPARK_LOCAL_DIRS=/data1/tmp,/data2/tmp   # scratch space incl. map output files; fast local disks, comma-separated
```

## Submit
```bash
spark-submit --master spark://m1:7077,m2:7077 --deploy-mode cluster \
  --total-executor-cores 40 --executor-cores 5 --executor-memory 18g \
  --supervise --class <main-class> app.jar
```
- By default an application acquires **all** cores in the cluster. Cap with `--total-executor-cores` (`spark.cores.max`) or set `spark.deploy.defaultCores` on the master (default Int.MaxValue).
- `--supervise` (cluster mode) restarts a driver that exits with a non-zero code.
- The standalone mode does not support cluster mode for Python applications.
- Scheduling across applications is simple FIFO; `spark.deploy.spreadOutApps` (default true) spreads applications over nodes, false consolidates them.

## High availability
ZooKeeper-based standby masters:
```bash
SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url=zk1:2181,zk2:2181,zk3:2181 -Dspark.deploy.zookeeper.dir=/spark"
```
Start a master on two or more hosts; clients list all of them (`spark://m1:7077,m2:7077`). Recovery takes between 1 and 2 minutes from when the first leader goes down; this affects only scheduling new applications, running ones are unaffected. `FILESYSTEM` recovery mode lets the Master be restarted and recover state from a directory.

## Gotchas
- Application work directories hold logs and jars; `spark.worker.cleanup.enabled` (default true in current docs) with `spark.worker.cleanup.appDataTtl` (default 604800 s = 7 days) cleans the directories of stopped applications only.
- With `spark.shuffle.service.db.enabled` (default true) the shuffle service state is reloaded after a restart; the docs recommend cleanup stays enabled with it.
- Resource sharing is limited to capping cores per application; there are no queues.

## Verify
- [ ] Master UI lists all workers ALIVE with expected cores/memory.
- [ ] After the active master stops, a standby becomes leader and `spark-submit` against the master list still works.
- [ ] Two concurrent apps both get executors (cores capped).

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in spark-standalone.md: start-master.sh / start-worker.sh / start-all.sh and conf/workers, ports 7077 and 8080, SPARK_WORKER_CORES / MEMORY / DIR / SPARK_LOCAL_DIRS semantics, spark.deploy.defaultCores, spreadOutApps (spark.deploy.spreadOut is not a documented key), --supervise, FIFO scheduling, ZooKeeper recovery settings and the 1-2 minute recovery time, FILESYSTEM mode, worker cleanup defaults. Confirmed in submitting-applications.md: standalone does not support cluster mode for Python. Removed unsourced sizing comments and the no-multi-tenant advice.

Method: documentation only; no commands were run.
