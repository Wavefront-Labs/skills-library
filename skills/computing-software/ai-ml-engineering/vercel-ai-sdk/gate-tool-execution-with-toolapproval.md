---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.gate-tool-execution-with-toolapproval
name: gate-tool-execution-with-toolapproval
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, tool-approval, human-in-the-loop, user-approval, tool-approval-response]
level: advanced
status: docs-checked
description: "Require human approval before sensitive tools run using toolApproval statuses and functions, then answer tool-approval-request parts in a second call."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop dangerous tool calls (shell, payments, data changes) until a person approves them.

## Configure
`toolApproval` goes on `generateText`, `streamText` or `ToolLoopAgent`. Either a per-tool map or one generic function.
```ts
toolApproval: {
  runCommand: { type: 'user-approval', reason: 'filesystem changes require operator review' },
}
```
Statuses (string or `{ type, reason }`): `'not-applicable'` (default, run normally), `'approved'` (auto-approve but emit request/response parts), `'denied'` (auto-deny, surface a denied output), `'user-approval'` (emit a request and wait). Returning `undefined` from a function equals `'not-applicable'`.

Dynamic per-tool: `processPayment: async ({ amount }) => amount > 1000 ? 'user-approval' : undefined`. A `SingleToolApprovalFunction` receives the input plus `toolCallId`, `messages`, `toolContext`, `runtimeContext`; it may return `{ type: 'denied', reason: 'blocked by policy' }`. Generic form: `toolApproval: ({ toolCall, tools, toolsContext, messages, runtimeContext }) => ...`; check `!toolCall.dynamic` before using typed input. The old `needsApproval` on `tool()` is deprecated.

## Manual flow needs two calls
`generateText`/`streamText` do not pause; they return `tool-approval-request` parts in `result.content`.
1. Call with `toolApproval`; push `result.responseMessages` onto `messages`.
2. Find parts with `part.type === 'tool-approval-request' && !part.isAutomatic` (fields: `approvalId`, `toolCall`, `reason`).
3. Collect a decision per request and append `{ role: 'tool', content: approvals }` where each approval is `{ type: 'tool-approval-response', approvalId, approved: true | false, reason? }` (type `ToolApprovalResponse`).
4. Call again with the updated messages: approved tools execute; denied ones show the model the denial.

## Reason semantics
Denied: the reason goes into the `execution-denied` tool result the model sees. Approved: it stays in the approval response (UI, audit logs); it is not sent to the model or changed in the tool input, though `execute` can read it from `options.messages` in manual continuations. It is not a data channel; to get user input use a tool without `execute` and supply the result from the client.

## Gotchas
- Add an instruction such as "When a tool execution is not approved, do not retry it" so the model does not repeat denied calls.
- Provider-executed tools ignore `toolApproval`; it only covers tools the SDK runs locally.
- With `useChat`, approvals are answered via `addToolApprovalResponse` (see the UI docs).

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
