---
id: computing-software.ai-ml-engineering.mastra.send-signals-to-threads
name: send-signals-to-threads
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, signals, notification, threads, sendmessage, queuemessage, subscribetothread, streaming]
level: advanced
status: docs-checked
description: "Send messages, queued follow-ups and typed signals to a Mastra agent thread, control delivery, and subscribe to the thread stream with history, run status and reconnect."
sources:
  - https://mastra.ai/docs/signals/sending-signals
  - https://mastra.ai/docs/signals/thread-streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: push input to an agent thread and read its output as one ordered stream.

## Send
All calls take `{ resourceId, threadId }` and return at once; `await result.accepted` for the routing decision.
```typescript
const result = agent.sendMessage('Compare that with the previous option.', { resourceId: 'user_123', threadId: 'thread_456' })
await result.accepted
```
- Idle thread starts a run; active run receives the message on its next model request; with memory it is stored.
- Shared threads: `sendMessage({ contents, attributes: { name: 'Jane', sentFrom: 'slack' } }, ids)` reaches the model as `<user name="Jane" sentFrom="slack">...</user>`.
- `queueMessage()` waits for the active run to finish, then starts a new run (immediate if idle). `cancelQueuedMessages()` removes queued input without stopping the run; best-effort across processes. `queueSignal()` is the typed equivalent.
- `sendSignal({ type: 'reactive', tagName: 'ci-result', contents: 'CI failed on main: 3 tests failed.' }, ids)`. `type`: `reactive` (your system or a processor) or `notification` (external event). Tag defaults to the type name, except `reactive` which defaults to `system-reminder`. Contents pass unchanged, attribute values are XML-escaped, a matching closing tag is escaped; this is not a prompt-injection defense. `tagName`/attributes: letters, numbers, `.`, `-`, `_`, starting with a letter or `_`. `transient: true` applies context to the current request only (not stored; cannot be a state signal).
- `sendNotificationSignal()` for durable inbox records; `sendStateSignal()` for named changing context (not exposed on `Session`). See the Notifications and State signals docs.

## Control delivery
Active thread default: deliver to the run (or persist / discard). Idle default: wake a run (or persist / discard). Set `ifActive.behavior` / `ifIdle.behavior`:
```typescript
const result = agent.sendSignal({ type: 'notification', contents: 'A new pull request is ready for review.' }, { ...thread, ifIdle: { behavior: 'persist' } })
const { action } = await result.accepted
if (action === 'persist') await result.persisted
```
`action` values: `wake` (result carries `output` stream), `deliver`, `persist`, `discard`, `blocked` (a paused run owns the thread). A routing failure rejects `accepted`.

## When the model sees input
Input during a model request can cancel and retry that request while the model has produced only reasoning/metadata or is awaiting its first token. Once text or a tool call appears, input waits for the next loop boundary; running tools are never cancelled. The retry adds nothing to `maxSteps`; usage totals exclude interrupted requests (providers may still bill). If `maxSteps` is hit first, queued input may be saved without a response. Signals appear as `<user>`, `<system-reminder>` or `<notification>`; with Memory, non-transient signals are stored.

## Abort
`subscription.abort({ clearPendingSignals: true })` (queue is preserved by default), or `agent.abortThreadStream()` without a subscription. Shared PubSub clears only the owning process's local queue.

## Subscribe
```typescript
const client = new MastraClient({ baseUrl: 'http://localhost:4111' })
const agent = client.getAgent('support-agent')
const subscription = await agent.subscribeToThread({ resourceId: 'user-123', threadId: 'thread-456' })
await agent.sendMessage({ message: 'Show the shorter version.', resourceId: 'user-123', threadId: 'thread-456' })
await subscription.processDataStream({ onChunk: chunk => console.log(chunk), reconnect: true })
```
Subscribe before sending. The stream persists across runs.
- `withInitialHistory: true`: first chunk `thread-history` (payload `{ messages, hasMore, activeRunId }`, oldest-first, `perPage` default 40, empty `runId`; empty `messages` without memory).
- `withRunStatus: true`: `thread-run-status` chunks, `payload.status` is `success`, `failed`, `aborted` or `suspended`. Both options default to `false`. An idle thread alone does not indicate success. Retained outcomes for finished runs are delivered to late subscribers; reconnect may redeliver, so group by `runId`.
- `subscription.activeRunId()`; queue counts via `subscribeThreadEvents()`.
- Approvals: `client.getAgent().sendToolApproval()`. A paused run keeps thread ownership; new-run signals get `blocked`. Pending approvals/suspensions replay on resubscribe; completed output does not.
- `hideSignals` (true/false/array of types) only on in-process core subscriptions, not HTTP/client-js; not a security boundary.
- `unsubscribe()` closes without aborting; `abort()` cancels the active run.

## Reconnect
`reconnect: true` retries indefinitely with a 1 s delay by default; a 4xx other than 408/429, or 501, stops and rejects. Resume only covers output the shared PubSub backend still retains; stored messages are not a record of every streamed fragment. Redis Streams recovery is bounded by stream length and idle TTL; upgrade both `@mastra/core` and `@mastra/redis-streams`.
Custom SSE endpoints: send heartbeats while idle, e.g. `controller.enqueue(encoder.encode(': keep-alive\n\n'))` every 25_000 ms, cleared on `request.signal` abort.

## Session equivalents
`session.sendMessage/queueMessage/sendSignal/queueSignal/sendNotificationSignal`; subscription managed by `Session`.

## Checked
Method: 2026-11-08 read the Mastra Sending signals and Thread streams docs pages in full (served as markdown). Send/queue/signal semantics, accepted actions, interruption window, abort, subscription options, reconnect and SSE heartbeat details all match the pages; no content changed.
