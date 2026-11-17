---
id: computing-software.ai-ml-engineering.mastra.schedule-workflows
name: schedule-workflows
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workflows, schedule, cron, scheduler, timezone, pause-resume, inngest]
level: practitioner
status: docs-checked
description: "Run a Mastra workflow on cron via the schedule field: single and multiple schedules, delivery guarantees, pausing at runtime, redeploy behaviour, hosting topology and Inngest."
sources:
  - https://mastra.ai/docs/workflows/scheduled-workflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: fire a Mastra workflow on one or more cron schedules and operate those schedules safely.

## Declare a schedule
Add `schedule` to `createWorkflow`. Register the workflow on `Mastra` as usual; the scheduler reads `schedule` off the workflow at boot, so there is no separate "register schedule" call. `workflow.start()` still works, and scheduled and manual runs share one execution path.

```typescript
export const dailyReport = createWorkflow({
  id: 'daily-report',
  inputSchema: z.object({ userId: z.string() }),
  outputSchema: z.object({ ok: z.boolean() }),
  schedule: { cron: '0 9 * * *', timezone: 'America/New_York', inputData: { userId: 'system' } },
}).then(sendReport).commit()
```

Fields: `cron` (required; 5, 6 or 7 parts; validated at construction), `timezone` (IANA; defaults to the host's local zone, so set it explicitly in production), `inputData`, `initialState`, `requestContext`, `metadata` (persisted with the schedule row).

## Multiple schedules
Pass an array; each entry needs a unique stable `id`:

```typescript
schedule: [
  { id: 'morning', cron: '0 9 * * *', inputData: { window: 'morning' } },
  { id: 'evening', cron: '0 18 * * *', inputData: { window: 'evening' } },
]
```
Each entry is an independent schedule row and shows separately in Studio.

## Delivery guarantees
Publication is best-effort. An occurrence is claimed before its start event is published, with up to three publish attempts. Exhausted attempts or a publisher crash can skip that occurrence; skipped ones are not replayed automatically, though later fires continue. A schedule marked `completed` has exhausted its cadence, which does not confirm execution.

## Execution engine
Scheduled fires run in-process on the host running the scheduler. Exception: when the `MASTRA_WORKERS` environment variable is set to any value (including `false`), `createWorkflow` builds scheduled workflows on the evented engine and fires run on the orchestration worker. Evented runs need a storage adapter with atomic concurrent updates such as `@mastra/libsql` or `@mastra/pg`, otherwise `createRun()` throws. If you split workers with the `workers` option instead of the variable, import `createWorkflow` from `@mastra/core/workflows/evented`.

## Pause and resume at runtime
```typescript
const client = new MastraClient({ baseUrl: 'http://localhost:4111' })
await client.pauseSchedule('wf_daily-report')
await client.resumeSchedule('wf_daily-report')
```
Schedule ids: `wf_<workflowId>` for a single schedule, `wf_<workflowId>__<scheduleId>` for array entries. Studio has Pause/Resume on the schedule detail page. Rules: pause is durable (survives restarts and redeploys); resume recomputes `nextFireAt` from now (no backlog burst); editing `schedule` config does not unpause; pause and resume are idempotent. HTTP routes are `POST /api/schedules/:scheduleId/pause` and `/resume`, requiring `schedules:write`.

## Redeploying with changes
- `cron` or `timezone` changed: `nextFireAt` recomputed (a cadence with no future occurrence completes the schedule; a still-firing cadence reactivates a completed one).
- Only `inputData`, `initialState` or `metadata` changed: row patched, next fire time kept.
- User-set status and fire history are not overwritten. Removing an entry from the array deletes its row at next boot.

## Where it can run
The built-in scheduler is a `setInterval` tick loop that assumes a long-lived process. Long-lived hosts work (the server from `mastra build` starts the scheduler). With a server adapter, call `mastra.startWorkers()` after the server starts listening, or schedules never fire. Serverless platforms (Vercel, Netlify, Lambda, Cloudflare Workers) do not fire declared schedules with the built-in scheduler; direct `run.start()` still works. For cron there, use `@mastra/inngest`.

## Inngest
With `@mastra/inngest`, scheduling uses Inngest's own `cron` on `createFunction`. Those schedules do not appear in Studio's schedules view, the header Schedules action is hidden, and `pauseSchedule`/`resumeSchedule` do not control them; manage them in the Inngest dashboard.

## Studio
`/workflows/schedules` lists all schedules (append `?workflowId=<id>` to filter); `/workflows/schedules/:scheduleId` shows detail, Pause/Resume and trigger history, including `pending` and `publish failed` badges.

## Checked
Method: 2026-11-08 read the cited Mastra scheduled-workflows page in full (served as markdown) and compared each claim. All claims matched; no content changes.
