---
id: computing-software.web-development.payload-cms.jobs-schedules
name: jobs-schedules
category: computing-software
field: web-development
product: payload-cms
tags: [job-schedules, cron-schedule, waituntil, handle-schedules]
level: advanced
status: docs-checked
description: "Queue jobs on a cron schedule with the schedule property, and pair it with a runner; use waitUntil for one-off future jobs."
sources:
  - https://payloadcms.com/docs/jobs-queue/schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Job schedules

Goal: queue recurring jobs automatically.

```ts
{
  slug: 'generateReport',
  schedule: [{ cron: '0 0 * * *', queue: 'nightly' }],   // daily at midnight
  handler: async () => ({ output: { reportId: '123' } }),
}
```

A schedule only enqueues the job; it does not run any logic. You also need a runner on the same queue name:

```bash
pnpm payload jobs:run --cron "* * * * *" --queue nightly --handle-schedules
```

or `jobs: { autoRun: [{ cron: '* * * * *', queue: 'nightly' }] }` on a long-running server (by default autoRun also handles schedules; `disableScheduling: true` turns that off; the queues page describes autoRun as running jobs only). The CLI also has `jobs:handle-schedules` to queue due schedules without running them.

Choose the right approach:

- Schedule - recurring tasks (daily reports, hourly syncs).
- `waitUntil` - one-time future job: `payload.jobs.queue({ task: 'publishPost', input, overrideAccess: true, waitUntil: new Date('2024-12-25T15:00:00Z') })`.
- Collection hook - react to document changes.
- Manual queue - triggered by a user action.

Checklist: task has `schedule`; a runner exists; both use the same `queue`; not on serverless for `autoRun`.

Verify: after one cron tick a job document with that queue name appears.

## Checked

2026-11-04. Read jobs-queue/schedules (docs/jobs-queue/schedules.mdx). Confirmed: the schedule shape with cron and queue, that a schedule only enqueues, the bin script and autoRun runners, jobs:handle-schedules, the waitUntil one-off example, the approach comparison and the four-point checklist. Added: the autoRun scheduling default and the conflict with the queues page.
Method: documentation only; no commands were run.
