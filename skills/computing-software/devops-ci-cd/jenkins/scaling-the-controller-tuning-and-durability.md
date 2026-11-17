---
id: computing-software.devops-ci-cd.jenkins.scaling-the-controller-tuning-and-durability
name: scaling-the-controller-tuning-and-durability
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkins-performance, controller-tuning, jvm-tuning, g1gc, heap-sizing, java-opts, pipeline-durability, durability-hint, performance-optimized, max-survivability, build-discarder, log-rotation, build-history, jenkins-home-disk, nfs-latency, lazy-loading, metrics-plugin, prometheus-plugin, monitoring-plugin, support-core, thread-dump, slow-ui, too-many-jobs, folder-sharding, multiple-controllers, cloudbees-ci, queue-length, executor-utilisation, weekly-restart]
level: advanced
status: docs-checked
description: "Keep a busy Jenkins controller responsive: JVM heap, Pipeline durability hints, build retention, fast JENKINS_HOME storage, Prometheus metrics, when to shard."
sources: ["https://www.jenkins.io/doc/book/scaling/", "https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/", "https://www.jenkins.io/doc/book/system-administration/monitoring/", "https://plugins.jenkins.io/prometheus/", "https://www.jenkins.io/doc/book/system-administration/diagnosing-errors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling the controller: tuning and durability

**Goal:** the UI stays snappy at thousands of jobs, builds don't pause on controller
I/O, and you know *why* before users file "Jenkins is slow" tickets.

## 1. JVM
- Size the heap from measurement (GC log, heap use). The Pipeline scaling guide says to use
  its suggested garbage-collection tuning options when the heap is over 6 GB.
- In containers prefer a percentage-based heap setting (`-XX:MaxRAMPercentage`) over a fixed
  `-Xmx` and give the pod a memory limit above the heap.
- Use a supported Java LTS (see the Jenkins Java support policy page).
- For a slow UI, take several thread dumps a few seconds apart and look for many threads in
  the same plugin method; take a heap dump when memory is the suspect.

## 2. Pipeline durability
Pipelines write transient data to disk frequently so running builds can survive a restart or
crash; that I/O is a main Pipeline bottleneck, worst on NFS, magnetic storage or heavy
concurrency.
```groovy
options { durabilityHint('PERFORMANCE_OPTIMIZED') }
```
or globally: Manage Jenkins -> System -> *Pipeline Speed/Durability Settings*; per job via
*Custom Pipeline Speed/Durability Level* or the `properties` step (applies to the NEXT run);
per branch in a multibranch project via a Branch Property Strategy. Modes:
- `MAX_SURVIVABILITY` (default, slowest, for the most critical pipelines)
- `SURVIVABLE_NONATOMIC` (writes with every step but avoids atomic writes; faster on network filesystems)
- `PERFORMANCE_OPTIMIZED` (greatly reduces disk I/O; if a pipeline has not finished and Jenkins is
  not shut down gracefully it may lose data)
The guide suggests performance-optimized for most pipelines and maximum durability (or the
non-atomic mode) where you need a guaranteed execution record. See the scaling-pipeline page
for requirements (all Pipeline plugins up to date, controller restart).

## 3. Build history and logs
Use build discarders everywhere (`buildDiscarder(logRotator(...))`) and keep large output in
artifacts rather than the console log. Prune orphaned multibranch branches with
`orphanedItemStrategy`.

## 4. Storage
Put `JENKINS_HOME` on fast, local or provisioned-IOPS storage; the scaling guide names NFS as
a case where durability settings help. Do not run two controllers on one volume.

## 5. Observing
- The **Prometheus** plugin exposes an endpoint (default `/prometheus/`) with metrics from the
  Metrics plugin and from itself; read the plugin page for metric names and the namespace prefix.
- *Manage Jenkins -> Load statistics* for executor/queue history.
- The Jenkins monitoring page covers further tooling.

## 6. Reduce controller work
- Do the building on agents: set the built-in node's executors to 0 (Manage Jenkins -> Nodes ->
  Built-In Node -> Configure), per the controller-isolation security page.
- Keep heavy work out of Pipeline (CPS) code, which runs on the controller; use `sh` steps and
  scripts on agents.
- Remove unused plugins and keep Pipeline plugins and Script Security current.

## 7. When to shard
When one team's load starves another, startup or UI latency stays unacceptable after tuning, or
trust boundaries differ, split by team/trust boundary: one controller per domain, each managed
as code from the same platform repo, with shared agent clouds.

## Verify
- [ ] GC log shows no repeated full GCs at peak.
- [ ] Prometheus shows the build queue draining outside peak.
- [ ] Controller restart is acceptable and no builds are lost with the chosen durability.
- [ ] Largest job build-history directories are bounded by discarders.

## Checked
2026-11-02. Confirmed against the Pipeline scaling guide (durability modes and where to set them, default, performance trade-offs, 6 GB heap GC tuning note, executors), the Prometheus plugin page and the controller-isolation page (built-in node executors). Removed: JVM flag set and heap sizing figures, JENKINS_OPTS values, inode/build-count thresholds, metric names, thread-dump URLs and class names, startup-performance flag, sharding thresholds, CPU and timing targets, USE_WATCHING property.
Method: documentation only; no commands were run.
