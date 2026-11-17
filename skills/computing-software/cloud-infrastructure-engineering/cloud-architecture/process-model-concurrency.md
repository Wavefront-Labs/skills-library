---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.process-model-concurrency
name: process-model-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, process-model-concurrency, process-types, procfile, horizontal-scaling, worker-processes, scale-out]
level: practitioner
status: docs-checked
description: "Apply factor VIII: scale out via the process model with named process types (web, worker, scheduler) scaled independently, instead of daemonising or growing one giant process."
sources: ["https://12factor.net/concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor VIII — Scale out via the process model

**Rule:** different work types are different **process types** (for example `web` and `worker`),
each scaled by running more processes, horizontally rather than by making one process bigger.
The set of process types and counts is the factor's "process formation".

## Steps
1. Enumerate process types and give each its own entry point:
   ```text
   web:    gunicorn app:wsgi --workers 4 --bind 0.0.0.0:$PORT
   worker: celery -A app worker --concurrency 8
   clock:  python -m app.scheduler     # exactly one instance
   ```
2. Map each to a separately scaled unit: Kubernetes Deployment per type, ECS service per type,
   Container Apps app per type, Cloud Run service + jobs.
3. Scale each on its own signal: web on RPS/CPU/latency, worker on queue depth, clock fixed at 1
   (or use the platform's scheduler instead).
4. Inside a process, threads and async are fine, but never daemonise or write PID files; rely on
   the platform's process manager (systemd, a cloud platform's manager, Foreman in development)
   for output streams, crash restarts and shutdowns.
5. Size in-process concurrency against the container's CPU limit and load-test it, so horizontal
   scaling stays close to linear.

## Gotchas
- Running web + worker in one container via supervisord couples their scaling and crashes.
- Singleton process types need leader election or a platform singleton to stay at one.

## Checked
2026-10-28. Confirmed against 12factor.net/concurrency: process types per work kind (web, worker), internal threads and async allowed, scale out across processes and machines, process formation, no daemonising or PID files, process manager handles crashes and restarts. Removed: the "clock" process type as a named convention and the Gunicorn/Node worker-count rules of thumb. The code block is an illustration, not a claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Each process type can be scaled to zero/N independently.
- [ ] Doubling replicas roughly doubles throughput (load test).
