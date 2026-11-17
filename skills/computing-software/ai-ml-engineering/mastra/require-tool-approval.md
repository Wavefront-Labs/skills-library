---
id: computing-software.ai-ml-engineering.mastra.require-tool-approval
name: require-tool-approval
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, requireapproval, human-in-the-loop, tool-approval, suspend, approvetoolcall, agent, hitl]
level: practitioner
status: docs-checked
description: "Pause Mastra tool calls for human approval with requireApproval or requireToolApproval, approve or decline with a reason, and resume after restarts."
sources:
  - https://mastra.ai/docs/agents/human-in-the-loop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop sensitive tool calls before `execute` runs until a human approves.

Prerequisite: configure a storage provider on the Mastra instance, or you get a "snapshot not found" error. Suspended runs only survive restarts with persistent storage (the default in-memory store loses them).

## Flags (OR logic)
- `requireApproval: true` in `createTool()` pauses calls to that tool.
- `requireToolApproval: true` in `stream()`/`generate()` options pauses every tool call for that request.

## Stream flow
```typescript
const stream = await agent.stream('Delete record abc-123')
for await (const chunk of stream.fullStream) {
  if (chunk.type === 'tool-call-approval') {
    // chunk.payload has toolCallId, toolName, args
    const approved = await agent.approveToolCall({ runId: stream.runId })
    for await (const c of approved.textStream) process.stdout.write(c)
    // or: await agent.declineToolCall({ runId: stream.runId })
  }
}
```
`toolCallId` is optional on all four approve/decline methods; pass it when several calls may be pending (the default is the most recent suspended one).

## generate flow
`generate()` returns `finishReason: 'suspended'` with `suspendPayload` (`toolCallId`, `toolName`, `args`) and `runId`. Use `approveToolCallGenerate({ runId, toolCallId })` or `declineToolCallGenerate(...)`.

## Decline with a reason
`declineToolCall({ runId, toolCallId, reason })` returns the reason to the model in place of the tool result and stores it on the tool call's `approval` metadata. Without it the model sees `Tool call was not approved by the user`.

## Conditional approval
`requireToolApproval` can be a (possibly async) function receiving `toolName`, `args`, `requestContext`, `workspace`; return true to require approval:
```typescript
requireToolApproval: ({ toolName }) => /^delete_/.test(toolName)
```
If the function throws, approval is required. Returning true only pauses; it does not approve. A tool-level `requireApproval` function is authoritative for that tool. Durable and stored agents accept only a boolean (a function falls back to requiring approval for every call).

## Bind approval to exact arguments
For sensitive tools, fingerprint `toolName` + `args` when the approval is shown (production: a stable hash), record it on approve, and in an agent `hooks.beforeToolCall` return `{ proceed: false, output: '...' }` unless the fingerprint was approved (and consume it once).

## Resume after a restart
`await agent.listSuspendedRuns({ threadId, resourceId })` returns runs with `toolCalls` (`toolCallId`, `toolName`, `args`, `requiresApproval`). If `requiresApproval`, call `approveToolCall`/`declineToolCall`; otherwise the tool used `suspend()` and you call `agent.resumeStream(data, { runId })`.

## Supervisors
Approvals from subagent tools surface on the supervisor stream; pass the `toolCallId` from the chunk (the supervisor's delegation call). `delegatedToolName`/`delegatedToolCallId` identify the subagent tool that paused.

## Resume signals and auto-resume
- On resume the stream emits a `tool-call-resumed` chunk (same `toolCallId`, before the `tool-result`) with `payload.kind` of `'suspension'` or `'approval'`. With `@mastra/ai-sdk` it arrives as a `data-tool-call-approval` or `data-tool-call-suspended` part with `resumed: true`. Use it to mark a question answered; do not infer that from tool output.
- `autoResumeSuspendedTools: true` only resumes data-bearing `suspend()` tools (needs memory, same thread, and a `resumeSchema`). It never approves `requireApproval` tools; those stay suspended until an explicit approve or decline.
- `sendToolApproval()` also falls back to storage to find a suspended run; pass `toolCallId` when several runs match. HTTP: `GET /agents/:agentId/suspended-runs`, and the client SDK has `agent.listSuspendedRuns()`.
- A tool-level `suspend()` alternative to `requireApproval`: call `context?.agent?.suspend(payload)` and `return` it immediately (code after `await suspend()` still runs), then answer with `resumeStream(data, { runId })` or `resumeGenerate(data, { runId })`.
- Function-valued `requireToolApproval` can call a `Classifier` to decide; send argument names, not values, unless the decision model meets data-handling needs, and treat a missing probability as "require approval".

## Checked
Confirmed 2026-11-08 against the Mastra human-in-the-loop docs page (fetched as markdown, read in full): flags, stream and generate flows, decline reason, conditional approval, argument binding, restart recovery and supervisor behaviour. Added the resume signals, auto-resume limits and storage-backed discovery details. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
