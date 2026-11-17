---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.write-text-system-and-message-prompts
name: write-text-system-and-message-prompts
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [prompts, instructions, messages, allow-system-in-messages, prompt-injection]
level: practitioner
status: docs-checked
description: "Choose between prompt, messages and instructions in generateText or streamText, and avoid the system-message rejection and injection risk."
sources:
  - https://ai-sdk.dev/docs/foundations/prompts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: supply the right prompt shape to `generateText` / `streamText`: a text `prompt`, a `messages` array, and system `instructions`.

## Three prompt shapes
- **Text prompt**: a string in `prompt`; build it with template literals for dynamic data.
  ```ts
  const result = await generateText({
    model,
    prompt: `I am planning a trip to ${destination} for ${lengthOfStay} days. Suggest activities.`,
  });
  ```
- **System prompt**: the `instructions` property. It works with both `prompt` and `messages`.
  ```ts
  await generateText({ model, instructions: 'You help plan travel itineraries.', prompt });
  ```
- **Message prompt**: `messages: [{ role: 'user', content: 'Hi!' }, { role: 'assistant', content: 'Hello, how can I help?' }, ...]`. Each message has `role` and `content`; content is a string or an array of parts (`{ type: 'text', text }`, file parts, tool-call parts, tool-result parts).

## System messages are rejected by default
A message with `role: 'system'` inside `prompt` or `messages` is rejected unless you set `allowSystemInMessages: true`. Use that opt-in only to replay existing histories that already contain system messages:
```ts
await generateText({
  model,
  allowSystemInMessages: true,
  messages: [
    { role: 'system', content: 'You help plan travel itineraries.' },
    { role: 'user', content: 'Plan 3 days in Berlin.' },
  ],
});
```
The docs warn that opting in can create a prompt-injection risk, because users could override or set the system prompt by injecting system messages. Normally only trusted server-side code should set system text, through `instructions`.

## UIMessage vs ModelMessage
`useChat` returns `UIMessage` objects, which do not support provider options. Convert them with `convertToModelMessages` to `ModelMessage` objects before adding `providerOptions` to messages or parts.

## Gotchas
- Not all models support all message and content types (multi-modal input, tool messages); see the model capabilities page the docs link to.
- Choose `prompt` for repeated generation from variants of one text, `messages` for chat and multi-modal input.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the "capabilities table" pointer with the model capabilities page the docs link to.

Method: documentation only; no commands were run.
