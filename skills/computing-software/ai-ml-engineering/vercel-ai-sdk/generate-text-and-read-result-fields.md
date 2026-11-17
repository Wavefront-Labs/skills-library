---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.generate-text-and-read-result-fields
name: generate-text-and-read-result-fields
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generate-text, result-fields, usage, performance, on-end]
level: practitioner
status: docs-checked
description: "Call generateText, read text, usage, steps, finalStep and performance metrics, access raw response headers, and use the onEnd callback."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-text
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a non-interactive generation and read everything useful from the result.

```ts
import { generateText } from 'ai';
const result = await generateText({
  model,
  instructions: 'You are a professional writer. You write simple, clear, and concise content.',
  prompt: `Summarize the following article in 3-5 sentences: ${article}`,
});
const { text } = result;
```
`generateText` suits non-interactive use (drafting, summarising) and tool-using agents.

## Result fields
- `content` (all steps), `text` (final step), `files`, `sources`, `toolCalls`, `toolResults` (all steps)
- `finishReason`, `rawFinishReason` (provider's raw value)
- `usage`: total across all steps; `warnings` (e.g. unsupported settings)
- `steps`: every step; `finalStep`: the last step
- `output`: structured output when `output` is configured

## Per-step performance
Each step has `performance`: `effectiveOutputTokensPerSecond`, `effectiveTotalTokensPerSecond`, `stepTimeMs` (model plus tool time), `responseTimeMs`, `toolExecutionMs` (keyed by tool call id). `outputTokensPerSecond`, `inputTokensPerSecond` and `timeToFirstOutputMs` are `undefined` for `generateText`, set only for streaming steps.

## Raw response
`result.finalStep.response.headers` and `.body` give provider headers and body.

## onEnd callback
Runs after the last step:
```ts
onEnd({ text, finishReason, usage, responseMessages, steps, totalUsage }) {
  const messages = responseMessages; // messages that were generated: persist chat history, record usage
}
```

## Gotchas
- Note the current naming: the system prompt is `instructions`, `finalStep` holds last-step data, `onEnd` is the completion callback.
- `usage` is the total across steps for multi-step generations.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
