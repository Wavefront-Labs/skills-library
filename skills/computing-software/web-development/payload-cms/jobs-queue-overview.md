---
id: computing-software.web-development.payload-cms.jobs-queue-overview
name: jobs-queue-overview
category: computing-software
field: web-development
product: payload-cms
tags: [jobs-queue, tasks, workflows, payload-jobs]
level: practitioner
status: docs-checked
description: "Understand the jobs queue model: tasks, workflows, jobs and queues, plus how to queue, schedule and run them."
sources:
  - https://payloadcms.com/docs/jobs-queue/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Jobs queue overview

Goal: run background work outside the request.

Concepts: a Task is a function with business logic; a Workflow groups tasks that run in order and can retry from the point of failure; a Job is an instance of a task or workflow to be executed; a Queue segments jobs into groups (nightly, every 10 minutes).

Use cases: non-blocking work (embeddings, third-party sync, emails), scheduled actions (publish or unpublish at a time, reminders, nightly rebuilds) and offloading heavy operations (PDF generation, headless browser).

The flow in three steps:

```ts
// 1. define a task
jobs: { tasks: [{ slug: 'sendEmail', handler: async () => ({ output: {} }) }] }
// 2. queue a job
await payload.jobs.queue({ task: 'sendEmail', input: { to: 'user@example.com' }, overrideAccess: true })
// 3. run the queue (bin script, autoRun, endpoint or Local API)
// pnpm payload jobs:run --cron "*/5 * * * *" --queue default
```

Schedules queue jobs automatically (`schedule: [{ cron: '0 8 * * *', queue: 'emails' }]` on a task), but only once something executes the schedules (the `jobs:handle-schedules` bin script, the `/api/payload-jobs/handle-schedules` endpoint, or `autoRun`, which does it by default unless `disableScheduling: true`). The queued jobs still need a runner on the same queue name.

Gotcha: queuing and running are different; a queued job with no runner never executes. Using both the `handle-schedules` bin script and `autoRun` for one queue queues duplicate jobs; the `payload-jobs` collection is hidden from the Admin Panel by default.

Verify: after running the queue, the job document (read with the Local API and `overrideAccess: true`) has `completedAt` set and `hasError` not true.

## Checked

2026-11-04. Read jobs-queue/overview (docs/jobs-queue/overview.mdx in payloadcms/payload). Confirmed: task, workflow, job and queue definitions, the three use-case groups, the queue and run option examples, the bin script, autoRun, endpoint and Local API runners, and the hidden payload-jobs collection. Corrected: schedules need something to execute them (handle-schedules or autoRun), not only a runner. Added: the duplicate-scheduling pitfall. Page conflict: the overview and schedules pages say autoRun also handles schedules by default, while the queues page says autoRun does not queue jobs; see jobs-running-queues.
Method: documentation only; no commands were run.
