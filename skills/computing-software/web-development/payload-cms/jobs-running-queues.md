---
id: computing-software.web-development.payload-cms.jobs-running-queues
name: jobs-running-queues
category: computing-software
field: web-development
product: payload-cms
tags: [run-jobs, jobs-autorun, jobs-run-endpoint, processing-lease]
level: advanced
status: docs-checked
description: "Execute queued jobs with the jobs:run bin script, jobs.autoRun, the /api/payload-jobs/run endpoint or the Local API, and tune leases and order."
sources:
  - https://payloadcms.com/docs/jobs-queue/queues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running job queues

Goal: make queued jobs actually execute.

Bin script (recommended for dedicated servers, runs as a separate process):

```bash
pnpm payload jobs:run
pnpm payload jobs:run --queue myQueue --limit 15
pnpm payload jobs:run --cron "*/5 * * * *" --queue myQueue --handle-schedules
pnpm payload jobs:run --all-queues
```

`autoRun` runs inside the app process (needs a long-running server, not serverless). The queues page says it only runs jobs and never queues them, but the overview and schedules pages say it also handles schedules (queues due scheduled jobs) unless `disableScheduling: true` is set, so set that flag if another process handles schedules:

```ts
jobs: { tasks: [...], autoRun: [{ cron: '*/5 * * * *', queue: 'default', limit: 50 }] }
```

Endpoint for serverless (for example Vercel Cron): `GET /api/payload-jobs/run?limit=100&queue=nightly` with `Authorization: Bearer <token>`. Parameters: `limit` (default 10), `queue` (default `default`), `allQueues=true`.

Leases: running jobs hold a renewable lease; defaults are 20 minutes duration and a 30 second safety buffer. Change with `jobs.processingLease: { duration, safetyBuffer }` (buffer must be below duration).

Order is FIFO by default; set `jobs.processingOrder: '-createdAt'` for LIFO, or per queue.

Verify: queue a job, run `jobs:run`, and see it finish.

## Checked

2026-11-04. Read jobs-queue/queues (docs/jobs-queue/queues.mdx). Confirmed: bin script commands and flags, autoRun example, the /api/payload-jobs/run endpoint with its limit (default 10), queue and allQueues parameters, the 20 minute lease and 30 second safety buffer defaults with the safetyBuffer-below-duration rule, and FIFO default with '-createdAt' for LIFO, global or per queue. Conflict noted in the skill: the queues page says autoRun does not queue jobs, while jobs-queue/overview and jobs-queue/schedules say it handles schedules by default.
Method: documentation only; no commands were run.
