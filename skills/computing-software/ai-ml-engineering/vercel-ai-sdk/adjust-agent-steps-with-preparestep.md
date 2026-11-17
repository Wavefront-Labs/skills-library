---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.adjust-agent-steps-with-preparestep
name: adjust-agent-steps-with-preparestep
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [loop-control, preparestep, activetools, prunemessages, context-compaction, dynamic-model]
level: advanced
status: docs-checked
description: "Use prepareStep to switch models, per-step settings and active tools, and to compact the message history with pruneMessages between agent steps."
sources:
  - https://ai-sdk.dev/docs/agents/loop-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change model, settings, tools or messages between steps of an agent loop (also works with `generateText` and `streamText`).

`prepareStep` runs before each step and defaults to the initial settings if you return `{}` (or nothing). Arguments include `model`, `stepNumber` (0-indexed), `steps` (previous steps with results), `messages` (what will be sent), plus `initialMessages` and `responseMessages`, and `runtimeContext`.

Per-step overrides (return any of these):
- `model`: for example upgrade after `stepNumber > 2 && messages.length > 10`.
- Provider-agnostic settings: `maxOutputTokens`, `temperature`, `topP`, `topK`, `presencePenalty`, `frequencyPenalty`, `stopSequences`, `seed`, `reasoning`. They apply to the current step only; omitted or `undefined` falls back to the top-level value; defined falsy values (`temperature: 0`, `seed: 0`, empty `stopSequences`) are kept.
- `activeTools: ['search']` and `toolChoice: 'required'` or `{ type: 'tool', toolName: 'search' }` to run phases (search steps 0-2, analyze 3-5, summarize 6+).
- `experimental_sandbox`: applies to tool execution in that step only; later steps use the top-level one.
- `messages`: see below.

Decide from history, for example `steps.flatMap(step => step.toolCalls).some(call => call.toolName === 'dataAnalysis')` then force `reportGenerator`.

Context compaction:

```ts
prepareStep: async ({ messages }) => {
  if (estimateTokens(messages) > COMPACTION_THRESHOLD) {
    return { messages: pruneMessages({ messages, reasoning: 'all', toolCalls: 'before-last-3-messages', emptyMessages: 'remove' }) };
  }
},
```
A returned `messages` array persists as the base for later steps; new assistant and tool response messages are appended after it. The docs' estimator (`JSON.stringify(messages).length / 4`) is deliberately simple.

Gotchas:
- Build `messages` overrides from `messages`, not from `initialMessages` plus `responseMessages`, or steering messages are dropped (reported as not delivered with reason `removed-by-prepare-step`).
- Unlike `runtimeContext` and `toolsContext`, a sandbox override is step-local.
- The summarize example maps `msg.role === 'tool'` messages longer than 1000 and replaces content; the helper `summarizeToolResult` is yours to write.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
