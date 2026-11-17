---
id: computing-software.ai-ml-engineering.mastra.stream-agents-and-workflows
name: stream-agents-and-workflows
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, stream, fullstream, aisdk, textstream, writer, workflows]
level: practitioner
status: docs-checked
description: "Stream Mastra agents and workflows: Agent.stream properties, Run.stream events, AI SDK converters, and the writer API from tools and steps."
sources:
  - https://mastra.ai/docs/guides/streaming
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: consume incremental output from agents and workflow runs and emit custom events from tools and steps.

## Agent streaming
`agent.stream()` accepts a string, an array of strings, or message objects with `role` and `content`. It returns a `MastraModelOutput`:
```typescript
const stream = await testAgent.stream([{ role: 'user', content: 'Help me organize my day' }])
for await (const chunk of stream.textStream) process.stdout.write(chunk)
```
Properties: `textStream`, `text` (promise), `steps` (promise), `finishReason` (promise), `usage` (promise), `objectStream` / `object` (partial and final output when `structuredOutput` is passed). Iterate `stream.fullStream` to see all event chunks. For agents dispatching background tasks, `untilIdle: true` keeps the stream open until the tasks finish and the agent responds; it requires agent memory.

Common agent events: `start`, `text-start`/`text-delta`/`text-end`, `reasoning-start`/`reasoning-delta`/`reasoning-end`, `tool-call`, `tool-result`, `step-start`, `step-finish`, `finish` (not exhaustive; see the ChunkType reference).

## AI SDK integration
```typescript
import { toAISdkStream } from '@mastra/ai-sdk'
const aiSDKStream = toAISdkStream(stream, { from: 'agent', version: 'v7' })

import { toAISdkMessages } from '@mastra/ai-sdk/ui'
const initialMessages = toAISdkMessages([{ role: 'user', content: 'Hello' }], { version: 'v7' })
```
Converters default to AI SDK v5; pass the version matching your installed AI SDK (here `v7`). Use `toAISdkMessages()` for `useChat()`'s `initialMessages`. Route handlers (`handleChatStream()`, `handleWorkflowStream()`, `handleNetworkStream()`) also need the matching version.

## Workflow streaming
Create a run, then `run.stream({ inputData })` returns a `WorkflowRunOutput`; `fullStream` is a `ReadableStream` of events, each with `runId` and `from` at top level. Properties: `stream.status`, `stream.result`, `stream.usage`.
```typescript
const run = await testWorkflow.createRun()
const stream = run.stream({ inputData: { value: 'initial data' } })
for await (const chunk of stream.fullStream) console.log(chunk)
```
Events: `workflow-start`, `workflow-step-start`, `workflow-step-output`, `workflow-step-progress`, `workflow-step-result`, `workflow-finish`, `workflow-paused`, `workflow-step-suspended`, `workflow-canceled`.

## Writer API (tools and steps)
In a tool, `context.writer` is available in `execute(inputData, context)`: `await context?.writer?.write({ type: 'custom-event', status: 'pending' })`. In a workflow step the `writer` argument is passed to `execute({ inputData, writer })`. `writer.custom({ type: 'data-tool-progress', ... })` emits top-level stream chunks (useful for UI frameworks).

Gotcha: you must `await` `writer.write(...)`, otherwise you lock the stream and get a `WritableStream is locked` error.

Transient chunks: `data-*` chunks from `writer.custom()` are persisted to message history by default. Add `transient: true` to stream live without storing (progress, verbose logs); after a page refresh transient chunks are gone, only the tool's return value and non-transient chunks load from storage.

## Checked
Method: 2026-11-08 read the cited Mastra streaming guide in full (served as markdown) and compared each claim. All claims matched; no content changes.
