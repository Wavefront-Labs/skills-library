---
id: computing-software.messaging-and-integration.apache-zookeeper.ycsb-benchmarking
name: ycsb-benchmarking
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, benchmark, ycsb, zk-smoketest, byteman, jepsen, load-testing]
level: advanced
status: docs-checked
description: "Benchmark and test a ZooKeeper ensemble: YCSB binding build and parameters, zk-smoketest, and the Byteman and Jepsen fault-testing options."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking and testing

YCSB:
- Build the binding with Maven: `-pl site.ycsb:zookeeper-binding -am clean package -DskipTests`.
- Parameters: `zookeeper.connectString`, `zookeeper.sessionTimeout`, `zookeeper.watchFlag` (default false).
- Workflow: `load` with `recordcount`, then `run` with a workload such as `workloadb` (read-heavy). Other options: `fieldlength`, `fieldcount`, `threads`, `hdrhistogram.percentiles`, `measurementtype=timeseries`.
- Large znodes: pass `-Djute.maxbuffer` through `-jvm-args` (default 1048575, must match the servers).
- Many threads: raise `maxClientCnxns` in zoo.cfg.

Other:
- zk-smoketest verifies new, updated or existing installations.
- Byteman injects faults into running servers (`bminstall.sh`, `bmsubmit.sh`); Jepsen runs in Docker with `lein run test`.

Verify: with `hdrhistogram.percentiles` set, the run output reports the requested latency percentiles.

## Checked

Method: docs-checked 2026-11-09 against zookeeperTools.html (full page read)
