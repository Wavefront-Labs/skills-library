---
id: computing-software.ai-ml-engineering.mastra.setup-agent-memory-threads
name: setup-agent-memory-threads
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, memory, thread, resourceid, message-history, scopes, subagents, request-context]
level: intro
status: docs-checked
description: "Give a Mastra agent memory: storage and Memory quickstart, resource/thread identity, scopes, what the model sees, subagent memory isolation, and per-request memory."
sources:
  - https://mastra.ai/docs/memory/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: enable memory on a Mastra agent and control which conversations and agents share it.

## Quickstart
1. `npm install @mastra/memory@latest`, plus a storage provider (the page uses `npm install @mastra/libsql@latest`). Memory requires storage.
2. Add storage to the Mastra instance (give `LibSQLStore` an `id`):
```typescript
export const mastra = new Mastra({ storage: new LibSQLStore({ id: 'mastra-storage', url: ':memory:' }) })
```
3. Pass a `Memory` to the agent:
```typescript
export const memoryAgent = new Agent({
  id: 'memory-agent',
  name: 'Memory Agent',
  memory: new Memory({ options: { lastMessages: 20 } }),
})
```
Skip memory for single-turn, independent requests.

## Message history: resource and thread
Pass `memory: { resource, thread }` on each call. `resource` is a stable id for the user or entity; `thread` isolates one conversation. Reuse both values to recall.

```typescript
await memoryAgent.generate('Remember my favorite color is blue.', {
  memory: { resource: 'user-123', thread: 'conversation-123' },
})
```
Gotcha: a thread's owner (`resourceId`) cannot change after creation; do not reuse a thread ID across owners, which causes query errors.

## Scopes instead of a memory object
Pass `scopes: ['org:acme', 'resource:user-123', 'thread:conversation-123']`. Memory reads the resource from the `resource:` scope and thread from `thread:`; other scopes go to tools and processors. An agent-level `scopes` option can add a list, or a function `({ scopes, requestContext }) => ...` that returns the final set. Rules: inputs to the resolver must come from the server (request bodies can set unreserved request-context keys; trusted middleware can set `MASTRA_SCOPES_KEY`; clients cannot send scopes). `resource:`/`thread:` scopes must agree with `memory.resource`/`memory.thread` or the call throws, and a scopes function must return every `resource:` and `thread:` scope it receives. Tools, processors and subagents get the other scopes but not these two.

## What the model sees
Message history is on by default; other features add context only when configured. Working memory is a system message (or a state signal with `useStateSignals`). Semantic recall matches from the current thread interleave with history by timestamp; matches from other threads go into a system message. Observational Memory replaces old raw history with observations in a system message. Optional `context` messages on a call (`agent.generate(msg, { context: [...] })`) are one-off and never saved. Messages are ordered by timestamp and deduplicated by ID. Use tracing and the LLM call spans in Studio to see the exact context.

## Observational Memory switch
`memory: new Memory({ options: { observationalMemory: true } })` needs a storage provider. See the observational-memory-setup skill for tuning.

## Subagent memory isolation
Delegation to a subagent happens with no flag. Each delegation gets a fresh thread ID (clean history) and resource ID `{parentResourceId}-{agentName}` (stable, so resource-scoped memory persists across delegations). A subagent without its own memory inherits the supervisor's `Memory`; its own takes precedence. `generateTitle` is not applied to inherited subagent threads. Only the delegation prompt and subagent response are saved; filter what reaches the subagent with `messageFilter`.

## Sharing memory between agents
When calling agents directly, matching `resource` shares resource-scoped working memory and semantic embeddings across threads (each agent keeps its own thread history). Matching `resource` and `thread` shares full message history, which Observational Memory (thread scope by default) relies on.

## Switch memory per request
`memory` accepts a function: `memory: ({ requestContext }) => requestContext.get('user-tier') === 'enterprise' ? premiumMemory : standardMemory`.

## Observational Memory failure modes the page lists
Thread scope throws without a `threadId`; on an existing thread the first turn loads every stored message until the first observation finishes; `lastMessages` does nothing under OM; keep `observation.observeOnContextOverflow` at its default `true`; call `await memory.settled()` before shutdown when async buffering is on; some invalid options only fail on first use.

## Checked
Method: 2026-11-08 read the cited Mastra memory overview page in full (served as markdown) and compared each claim. All claims matched; no content changes.
