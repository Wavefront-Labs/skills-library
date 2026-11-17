---
id: computing-software.data-engineering.apache-spark.thread-dumps-for-hung-tasks
name: thread-dumps-for-hung-tasks
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-thread-dump, jstack, hung-tasks, deadlock, troubleshooting, spark-monitoring]
level: advanced
status: docs-checked
description: "Diagnose stuck Spark tasks and drivers with thread dumps: the Executors tab dump link, jstack on executors, what blocked threads look like, and common culprits."
sources:
  - https://spark.apache.org/docs/latest/web-ui.html#executors-tab
  - https://docs.oracle.com/en/java/javase/17/troubleshoot/diagnostic-tools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread dumps for hung tasks and drivers

**Symptoms:** a stage stuck at 199/200 tasks with no progress for a long time; a driver that stops scheduling; a job that never finishes but uses no CPU.

## Get dumps
- **Spark UI > Executors > Thread Dump** link per executor row (the page also offers Heap Histogram and Flame Graph links). Take several dumps a few seconds apart; a thread in the same frame each time is the stuck one.
- Task-specific: Stages > task row shows the executor; dump that executor and look for the thread named `Executor task launch worker for task <TID>`.
- Shell: `jcmd <pid> Thread.print` (Oracle recommends jcmd over the older jstack; `Thread.print -l` adds java.util.concurrent locks) on the executor host or inside the executor pod.

## Reading them
Look at the top frames of the same thread across dumps: network reads point at an external system, repeated lock waits at contention, and a runnable frame in your own code at a loop or skewed group.

## Mitigation while investigating
Speculative execution (`spark.speculation`) launches backup copies of slow tasks; see the Spark configuration page.

## Verify
- [ ] Root cause identified from repeated identical frames; fix applied (timeout, skew, regex) and the stage completes in normal time.

## Checked

2026-11-01. Confirmed against the Spark web UI Executors tab (Thread Dump, Heap Histogram, Flame Graph links) and the Oracle JDK 17 diagnostic tools page (`jcmd`, `Thread.print`, `-l`, jstack advice). Removed: version gate, YARN/kubectl/py-spy recipes, the stack-frame to cause table and driver-hang specifics.

Method: documentation only; no commands were run.
