---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.replay-tool-calls-and-results-in-messages
name: replay-tool-calls-and-results-in-messages
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [prompts, tool-messages, tool-call, tool-result, multimodal-tool-results]
level: advanced
status: docs-checked
description: "Write assistant tool-call parts and tool-result messages by hand, including parallel calls, id matching and multi-part tool outputs."
sources:
  - https://ai-sdk.dev/docs/foundations/prompts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: construct or replay a conversation that contains tool calls and their results in `messages`.

## Shape
An assistant message holds `tool-call` parts; a following message with `role: 'tool'` holds `tool-result` parts. One assistant message can call several tools (parallel calling) and one tool message can hold several results.

```ts
messages: [
  { role: 'user', content: 'How many calories are in this block of cheese?' },
  {
    role: 'assistant',
    content: [{
      type: 'tool-call',
      toolCallId: '12345',
      toolName: 'get-nutrition-data',
      input: { cheese: 'Roquefort' },
    }],
  },
  {
    role: 'tool',
    content: [{
      type: 'tool-result',
      toolCallId: '12345', // must match the tool call id
      toolName: 'get-nutrition-data',
      output: { type: 'json', value: { name: 'Cheese, roquefort', calories: 369, fat: 31, protein: 22 } },
    }],
  },
]
```
Note the field names: the call carries `input`, the result carries `output` with a discriminator `type`.

## Multi-part / multi-modal results
For models that support it, use `output: { type: 'content', value: [...] }` with parts such as `{ type: 'text', text: '...' }` and `{ type: 'file-data', data: <base64 string>, mediaType: 'image/png' }`. For models that do not support multi-part tool results, include a regular `output: { type: 'json', value }` result instead (the docs show both result forms side by side).

## Related
- Assistant content may also contain text and reasoning parts.
- Tools themselves are documented separately; here you only replay history.

## Gotchas
- The `toolCallId` in the tool message must match the assistant tool call.
- Not all models handle tool messages; check model capabilities first.
- If messages come from `useChat`, convert them with `convertToModelMessages` first.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "(function tools, execute)" aside.

Method: documentation only; no commands were run.
