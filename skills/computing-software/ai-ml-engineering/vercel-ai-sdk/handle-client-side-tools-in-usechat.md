---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.handle-client-side-tools-in-usechat
name: handle-client-side-tools-in-usechat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot-tool-usage, usechat, ontoolcall, addtooloutput, tool-parts, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Run server, automatic client-side and user-interaction tools in a useChat app with onToolCall, addToolOutput, sendAutomaticallyWhen and typed tool parts."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-tool-usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handle server and client-side tools in useChat

Goal: let the model call tools whose results come from the server, the browser, or the user.

## Three patterns

1. Server tool: has `execute` in the `streamText` `tools` object; the result is streamed to the client.
2. Automatic client tool: no `execute` on the server; handled by `onToolCall` in `useChat`.
3. User-interaction tool: no `execute`; render a UI and call `addToolOutput` when the user answers.

## Server route

```ts
const result = streamText({
  model, messages: await convertToModelMessages(messages),
  tools: {
    getWeatherInformation: { description: '...', inputSchema: z.object({ city: z.string() }), execute: async ({ city }) => 'sunny' },
    askForConfirmation: { description: 'Ask the user for confirmation.', inputSchema: z.object({ message: z.string() }) },
    getLocation: { description: 'Get the user location.', inputSchema: z.object({}) },
  },
});
return createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) });
```

## Client

```tsx
const { messages, sendMessage, addToolOutput } = useChat({
  transport: new DefaultChatTransport({ api: '/api/chat' }),
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
  async onToolCall({ toolCall }) {
    if (toolCall.dynamic) return; // check first, for type narrowing
    if (toolCall.toolName === 'getLocation') {
      addToolOutput({ tool: 'getLocation', toolCallId: toolCall.toolCallId, output: 'New York' }); // no await
    }
  },
});
```

- Do not `await` `addToolOutput` inside `onToolCall` (deadlock risk).
- Without the `toolCall.dynamic` check TypeScript reports `Type 'string' is not assignable to type '"toolName1" | ...'`.
- `sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls` submits automatically once all tool results are available.

## Rendering

Assistant `parts` contain parts named `tool-<toolName>` (for example `tool-askForConfirmation`) with `part.state`: `input-streaming`, `input-available`, `approval-requested`, `approval-responded`, `output-available`, `output-error`, `output-denied`. Handle all states exhaustively. On `input-available` for a user-interaction tool, show buttons that call `addToolOutput({ tool: 'askForConfirmation', toolCallId: part.toolCallId, output: 'Yes, confirmed.' })`. Tool inputs stream by default, so `input-streaming` parts carry partial `input`.

## Client tool errors

```tsx
addToolOutput({ tool: 'getLocation', toolCallId: toolCall.toolCallId, state: 'output-error', errorText: 'Unable to get the user location' });
```

Render failures with `isToolOutputErrorUIPart(part)` then `part.errorText`.

## Other part types

- `dynamic-tool` (with `part.toolName`) is used for tools unknown at compile time (MCP tools without schemas, runtime-loaded functions).
- Multi-step tool calls add `step-start` parts; render them as separators (skip index 0).
- Server-only multi-step loops: add `stopWhen: isStepCount(5)` to `streamText`; it works when every tool has `execute`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the "nothing is resubmitted without sendAutomaticallyWhen" bullet with the docs statement.

Method: documentation only; no commands were run.
