---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.add-tool-approval-ui-to-usechat
name: add-tool-approval-ui-to-usechat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot-tool-usage, tool-approval, toolapproval, addtoolapprovalresponse, usechat, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Require user approval before a server-side tool runs using toolApproval, render approve and deny buttons in useChat, and auto-continue after the response."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-tool-usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add a tool approval UI to useChat

Goal: sensitive server-side tools (payments, deletes, external calls) execute only after the user approves.

## Server

```ts
const result = streamText({
  model, messages,
  tools: { getWeather: tool({ description: '...', inputSchema: z.object({ city: z.string() }), execute: async ({ city }) => fetchWeather(city) }) },
  toolApproval: { getWeather: 'user-approval' },
});
```

`toolApproval` on `streamText` is the current mechanism; the older `needsApproval` property on tools is deprecated.

## Client

When approval is needed the tool part state is `approval-requested`. Render `part.approval.requestReason` if present and call `addToolApprovalResponse({ id: part.approval.id, approved: true })` or `approved: false`.

```tsx
case 'approval-requested':
  if (part.approval.isAutomatic) return <div>Checking approval...</div>;
  // show Approve / Deny buttons
case 'approval-responded': // part.approval.approved, part.approval.reason, isAutomatic
case 'output-available': ...
case 'output-denied': ...
```

- Automatic approvals/denials flow through the same states with `part.approval.isAutomatic === true` and optional `part.approval.reason`; do NOT call `addToolApprovalResponse` for them.
- A denial reason you pass to `addToolApprovalResponse` is included in the `execution-denied` result the model sees. An approval reason is only recorded on the part: it is not added to the prompt or tool input. To collect input from the user, use a client-side tool and `addToolOutput` instead.
- `part.approval.descriptor` carries opaque server metadata (from `approvalDescriptor`) in `approval-requested` and later states; it must not be used to decide whether the tool was approved.

## Continue automatically

If nothing happens after approval, you have neither called `sendMessage` nor configured auto-submit:

```tsx
useChat({ sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithApprovalResponses });
```

## Securing sensitive tools

The client sends full history each turn, so a modified client could forge an approval. Add `experimental_toolApprovalSecret: process.env.TOOL_APPROVAL_SECRET` to `streamText` so the server verifies it issued the approval (details in the agents tool-approvals docs).

## Gotchas

- Typed tool parts include `approval-requested`, `approval-responded` and `output-denied` even for tools without approval; include them when switching exhaustively on `part.state`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
