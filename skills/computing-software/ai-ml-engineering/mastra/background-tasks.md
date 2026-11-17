---
id: computing-software.ai-ml-engineering.mastra.background-tasks
name: background-tasks
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, harness, background-tasks, untilidle, subagents, suspend-resume, tools]
level: sme
status: docs-checked
description: "Run long Mastra tool calls and subagents as background tasks: enabling, eligibility layers, dispositions, untilIdle, suspend/resume, callbacks and manager streams."
sources:
  - https://mastra.ai/docs/harness/background-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let an agent dispatch long tool calls without blocking the loop; the result lands in memory and the agent reports it. Added in `@mastra/core@1.29.0`. Needs a configured storage backend (tasks persist across restarts).

## Enable (off by default)
```typescript
export const mastra = new Mastra({
  storage: new LibSQLStore({ id: 'storage', url: 'file:mastra.db' }),
  backgroundTasks: { enabled: true, globalConcurrency: 10, perAgentConcurrency: 5, backpressure: 'queue', defaultTimeoutMs: 300_000 },
})
```
Enabling alone runs nothing in the background; tools must be made eligible.

## Eligibility
- Tool level: `background: { enabled: true, defaultDisposition: 'deferred', timeoutMs: 600_000, maxRetries: 1 }` in `createTool`.
- Agent level: `backgroundTasks: { tools: { researchTool: { enabled: true, timeoutMs: 600_000 }, summarizeTool: false } }`; `tools: 'all'` opts in everything; `disabled: true` forces every call synchronous.
- Eligible tools default to `deferred`; set `defaultDisposition: 'foreground'` to merely allow the LLM to choose.
- The model may pass `_background` in args (stripped before the tool runs): `{ "_background": { "disposition": "awaited", "timeoutMs": 900000 } }`. Dispositions: `foreground` (sync), `deferred` (agent continues; `untilIdle` streams wait), `awaited` (dispatched, but the branch waits for the result). `enabled: true` maps to deferred, `false` to foreground; `disposition` wins. `_background` cannot enable a tool that is not already eligible.

## Stream chunks
Agent stream: `background-task-started`, `background-task-progress`. Manager stream: `-running`, `-output`, `-completed`, `-failed`, `-cancelled`, `-suspended`, `-resumed`. `agent.stream()` with `untilIdle: true` pipes the manager chunks into `fullStream` as well.

## untilIdle
```typescript
const stream = await agent.stream('Research solana for me', {
  memory: { thread: 't1', resource: 'u1' },
  untilIdle: true,            // or { maxIdleMs: 30_000 }; default 5 minutes
})
```
Keeps the stream open until tasks finish and the LLM responds. Global default: `backgroundTasks.untilIdleMaxIdleMs` (make it longer than your slowest task). Aggregate properties (`text`, `toolCalls`, `getFullOutput()` ...) reflect only the first turn; consume `fullStream` to aggregate.

## Reporting without untilIdle
A `notification` signal tagged `background-task` wakes an idle thread (or reaches the active run's next request). Not sent when an `untilIdle` stream is open, when that stream was cancelled, or for awaited tasks. Needs memory thread and resource. Set `notifyAgentOnFinish: false` if you send your own completion (e.g. in `onTaskComplete`). `wokenRunsEndAfterTurn: true` ends signal-woken runs after their turn (temporary option); with `notifyAgentOnFinish: false` nothing reports those tasks.

## Subagents
Opt them in on the supervisor: `backgroundTasks.tools: { researchAgent: { enabled: true, timeoutMs: 900_000 } }`. If not listed but the subagent has background-eligible tools, the whole subagent call is still dispatched in the background (config such as `waitTimeoutMs` comes from the subagent). Only one nested background-tool level is supported; a second delegation edge runs foreground.

## Suspend and resume
Inside `execute`, `const { suspend, resumeData } = context.agent`; if no `resumeData`, `await suspend?.({ awaiting: 'approval', draft })` and return. Suspending persists the payload, saves the workflow snapshot and frees the concurrency slot. Resume: `await mastra.backgroundTaskManager?.resume(taskId, resumeData)`; `context.agent.suspendPayload` holds the suspend data. `{ onNoSlot: 'queue' }` queues the resume (in-memory only; lost if the process exits). Default with no free slot: throws `Concurrency limit reached`.
- HTTP: `POST /api/background-tasks/:backgroundTaskId/resume`, or `client.resumeBackgroundTask(taskId, resumeData, { suspendedAt })`. Returns `409` for stale `suspendedAt`, not suspended, or no free slot; `404` if missing or another resource's. Requires `background-tasks:execute`.
- Open requests appear in `metadata.suspendedTools[toolCallId]` (written only by the dispatching process).
- With `untilIdle` the stream closes on suspend; continue with `agent.resumeStream(resumeData, { runId, toolCallId, memory, untilIdle: true })`.
- After a restart, re-register the executor with `manager.registerTaskContext(taskId, ...)` before `resume()`. `manager.cancel(taskId)` works on suspended tasks.

## Callbacks
Tool `background.onComplete/onFailed`, agent `backgroundTasks.onTaskComplete/onTaskFailed`, manager-level `onTaskComplete/onTaskFailed` (global, includes non-agent owners). They do not replace one another.

## Manager streams and lookups
`mastra.backgroundTaskManager.stream({ allResources: true, abortSignal })` (snapshot of running tasks, then live events; always pass an abort signal). Filters: `agentId`, `runId`, `threadId`, `resourceId`, `taskId`. Without `resourceId` or `allResources` it only delivers tasks with no `resourceId`. `allResources` exposes every user's args and results: trusted server code only. `getTask(id)` and `listTasks({ status, agentId })` read storage.

## Non-agent owners
Use a namespaced `agentId` like `mcp-server:<serverId>`; register `registerStaticExecutor(name, { execute })`; `enqueue({...})` with optional `expiresAt` (cleanup only runs if you set `cleanup`; never deletes pending/running/suspended) and `metadata`. `perOwnerConcurrency: { 'mcp-server:ops': 50 }` still counts toward `globalConcurrency`. `pinToWorker: true` (third `enqueue` arg, needs a task context) leases a pending task to this worker; if the worker dies it counts as a lost attempt (retry on another worker if `retryCount < maxRetries`, else fails with `Worker process terminated before task completed`). Make pinned work idempotent. Limitations: recovered tasks lack the original request; unpinned pending tasks hold no lease and fail with `No executor registered` if the executor existed only in the original process; the end-of-step wait ignores `pending` tasks.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
