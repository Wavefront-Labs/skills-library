---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.fix-missing-tool-result-errors
name: fix-missing-tool-result-errors
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [troubleshooting, tool-calling, addtooloutput, missing-tool-results, tool-approval, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Resolve AI_MissingToolResultsError and ToolInvocation must have a result by supplying tool outputs or approvals for every tool call in history."
sources:
  - https://ai-sdk.dev/docs/troubleshooting/missing-tool-results-error
  - https://ai-sdk.dev/docs/troubleshooting/tool-invocation-missing-result
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fix missing tool result errors

Goal: every tool call in the conversation must be resolved before the next request to the model.

## Error 1: AI_MissingToolResultsError

Message: "Tool results are missing for tool calls: ...". The SDK validates that every `tool-call` part in history is resolved, meaning a `tool-result` exists or a `tool-approval-response` was recorded. A new message sent while a call is pending throws.

Fix when building `ModelMessage` history yourself: after the assistant message holding the `tool-call` (with `toolCallId`, `toolName`), include a `role: 'tool'` message with a `tool-result` carrying the same `toolCallId` and `toolName`, before the next user message. For approval flows include `{ type: 'tool-approval-response', approvalId, approved: true | false }` in a tool message.

## Error 2: "ToolInvocation must have a result"

Happens with `generateText()` or `streamText()` when a tool has no `execute` function and no result is supplied another way. Pick one:

1. Server-side: give the `tool({ description, inputSchema, execute })` an `execute` that returns data.
2. Client-side in `useChat`: omit `execute` and provide output with `addToolOutput({ tool, toolCallId, output })`. Set `sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls` so the chat resubmits once all outputs exist.

```tsx
onToolCall: async ({ toolCall }) => {
  try {
    const result = await getLocationData();
    addToolOutput({ tool: 'getLocation', toolCallId: toolCall.toolCallId, output: result });
  } catch {
    addToolOutput({ tool: 'getLocation', toolCallId: toolCall.toolCallId, state: 'output-error', errorText: 'Failed to get location' });
  }
}
```

For interactive UI (a Confirm button), call `addToolOutput` from the click handler and pass the `toolCallId`.

## Gotchas

- Do not `await` `addToolOutput` inside `onToolCall`; the docs warn this can deadlock.
- The docs example reports a failed client-side call with `state: 'output-error'` and `errorText`.
- The docs' hand-written message example uses `args` and `result` fields.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Reworded two gotchas as what the docs examples do.

Method: documentation only; no commands were run.
