---
id: computing-software.devops-ci-cd.rundeck.tune-quartz-and-node-threads
name: tune-quartz-and-node-threads
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, quartz-threadcount, node-thread-count, job-timeout, concurrent-jobs]
level: advanced
status: docs-checked
description: "Control how many Rundeck jobs run at once: quartz.threadPool.threadCount, per-job node thread count, and job timeouts as guardrails."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/tuning-rundeck.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quartz thread pool. The default maximum for concurrent jobs is `10`. Take the Quartz setting name, replace the `org.quartz` prefix with `quartz`, and set it in `rundeck-config.properties`:

```properties
quartz.threadPool.threadCount = 20
```

Example from the page: 200 scheduled jobs fire together with a pool of 50. Only 50 run (sometimes fewer, because Rundeck uses some threads for background work); the other 150 wait for free threads, so they start late but do start. More threads need more heap. Start low (50 is a good starting number, then 100, 200). The pool also serves ad hoc commands, manual runs and health checks.

Node dispatch thread count. Each job has its own **Thread Count** (`nodeThreadcount`), separate from the Quartz pool. Each running execution holds one Quartz thread; parallel node dispatch adds extra threads up to the job's count, not counted against the pool. Rundeck enforces no maximum, so:
- keep node thread counts proportional to memory
- budget the total across all jobs that may run together
- review high values before production (SCM or Terraform review is a good gate)

Timeouts. A timeout is set per job; there is no system or project default, so a job without one can run forever holding its thread. Set timeouts on production jobs, especially long-running or externally dependent ones. The per-job log limit is a related guardrail against unbounded output.

## Checked

2026-11-04: the Quartz thread count default and property naming, the 200-jobs example, node thread count behaviour, timeout guidance and the log limit guardrail confirmed against the Rundeck Tuning page. Removed an unsourced verify step.

Method: documentation only; no commands were run.
