---
id: computing-software.messaging-and-integration.celery.celery-worker-prefetch-and-concurrency
name: celery-worker-prefetch-and-concurrency
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-prefetch, celery, prefetch-multiplier, worker-concurrency, disable-prefetch, eta-task-limit, acks-late, throughput]
level: practitioner
status: docs-checked
description: "Tune Celery worker prefetch, concurrency and late acks: prefetch multiplier, worker_disable_prefetch, ETA task limit and reconnection behavior."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/optimizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Worker prefetch and concurrency tuning

Goal: balance throughput against fair distribution of tasks between workers.

## Prefetch basics
The prefetch limit is the number of messages a worker can reserve for itself. Default prefetch count = `worker_prefetch_multiplier` (default 4) x concurrency slots. CLI: `--prefetch-multiplier`. `0` lets the worker consume as many as it wants, ignoring other workers and memory.
- Many long tasks: multiplier `1`.
- Many short tasks where throughput or latency matters: large, e.g. 50 or 150 (also "64, 128"); experiment.
- Mix of long and short: two separately configured worker nodes, routed by run time.
- With the default (4), the first worker started takes four times the messages per process, so long tasks may not distribute fairly.

## Reserve at most one task per process
With early acks and multiplier 1, `-c 10` may reserve 20 tasks (10 executing acknowledged, 10 reserved unacknowledged), because an early-acked task stops counting as unacknowledged. To reserve only as many tasks as processes, ack late so running tasks keep occupying prefetch slots:

```python
task_acks_late = True
worker_prefetch_multiplier = 1
```
Tasks must be idempotent, since a started task is retried after power failure or abrupt kill.

## worker_disable_prefetch (5.6+, default False)
If tasks cannot be acked late, enable this (or `--disable-prefetch`): the worker only fetches when a process is free, still with early acks. Currently Redis broker only; other brokers warn and ignore it.

## ETA tasks
`worker_eta_task_limit` (5.6+, default none): max ETA/countdown tasks held in memory; at the limit the worker stops receiving tasks from the broker. ETA/countdown tasks sit on an internal timer outside the per-process prefetch window, so `--prefetch-multiplier=1` can seem to do nothing. The limit also caps unacknowledged messages (kombu QoS `max_prefetch`); a prefetch count above it stops consumption until acks.

## After connection loss
`worker_enable_prefetch_count_reduction` (5.4+, default enabled): after a connection loss the prefetch count is reduced by the number of running tasks and restored gradually as pre-loss tasks complete. Disable it for a fixed prefetch count. It reconnects only if `broker_connection_retry_on_startup` or `broker_connection_retry` is not False.

## Concurrency
`worker_concurrency` (default CPU cores; CLI `--concurrency`). Mostly I/O: more; mostly CPU: near CPU count. 5.7+ accepts `"auto"` on Linux prefork: affinity mask and the smallest cgroup CPU quota found, `ceil(quota)`, min 1, max affinity count. For gevent, eventlet, thread and solo pools it resolves to the affinity CPU count.

## Monitoring
If a task takes 10 minutes and 10 new tasks arrive per minute, the queue never empties: monitor queue lengths and alert (docs suggest Munin), then add workers or revoke tasks.

## Checked

2026-11-07. Re-read the cited page(s) (configuration, optimizing) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
