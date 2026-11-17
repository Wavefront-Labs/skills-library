---
id: computing-software.devops-ci-cd.concourse-ci.gc-grace-periods-and-web-worker-ratio
name: gc-grace-periods-and-web-worker-ratio
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [garbage-collection, grace-period, failed-builds, scaling, web-worker-ratio, tuning]
level: advanced
status: docs-checked
description: "Tune how long failed and finished containers linger with the CONCOURSE_GC grace period variables, and size web nodes to workers using the documented 1:6 starting ratio."
sources:
  - https://concourse-ci.org/docs/operation/tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failed or errored builds do not release their containers and storage immediately; they linger on the worker until garbage collected. Tune this on the web node.

`CONCOURSE_GC_FAILED_GRACE_PERIOD` applies only to containers from failed jobs and is the longest grace period, default `120h` (five days), so someone can investigate a weekend failure on Monday. Failed containers are collected as soon as a new build of the job starts, so they only persist the full period if they belong to the job's latest build. If many containers and volumes are held by failed jobs, reduce it to fewer days or a few hours.

Three more variables default to `5m`:
- `CONCOURSE_GC_ONE_OFF_GRACE_PERIOD`: one-off build containers
- `CONCOURSE_GC_MISSING_GRACE_PERIOD`: containers and volumes that were created but went missing from the worker
- `CONCOURSE_GC_HIJACK_GRACE_PERIOD`: hijacked containers

If workers crash from CPU or memory pressure, consider a custom placement strategy or chain (see the placement skills).

**Web to worker ratio.** The page calls this anecdotal and says to adjust by watching metrics from the web nodes. A starting ratio is 1:6, one web node per six workers. The core Concourse team runs two web nodes and 16 workers (1:8), which works because fewer than ten people actively use the web UI daily and a single team has fewer pipelines.

## Checked

2026-11-04. Grace period variables and defaults, and the ratio guidance, confirmed on the Performance Tuning page (Garbage Collection and Web To Worker Ratio sections).

Method: documentation only; no commands were run.
