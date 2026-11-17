---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.unit-test-with-mock-models
name: unit-test-with-mock-models
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [testing, mocklanguagemodelv4, simulatereadablestream, toolloopagent, vitest]
level: practitioner
status: docs-checked
description: "Unit test AI SDK code deterministically with MockLanguageModelV4 from ai/test, simulateReadableStream, structured output mocks and multi-step agent tests."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: test code that calls `generateText`, `streamText` or an agent without hitting a provider.

Helpers from `ai/test`: `MockLanguageModelV4`, `MockEmbeddingModelV4`, `mockId` (incrementing integer ids), `mockValues` (iterates an array per call, returning the last value once exhausted). From `ai`: `simulateReadableStream`.

generateText mock: pass `new MockLanguageModelV4({ doGenerate: async () => ({ content: [{ type: 'text', text: 'Hello, world!' }], finishReason: { unified: 'stop', raw: undefined }, usage: { inputTokens: { total: 10, noCache: 10, cacheRead: undefined, cacheWrite: undefined }, outputTokens: { total: 20, text: 20, reasoning: undefined } }, warnings: [] }) })` as `model`.

streamText mock: `doStream: async () => ({ stream: simulateReadableStream({ chunks: [...] }) })` with chunks `{ type: 'text-start', id: 'text-1' }`, `{ type: 'text-delta', id: 'text-1', delta: 'Hello' }`, ..., `{ type: 'text-end', id: 'text-1' }`, then `{ type: 'finish', finishReason: { unified: 'stop', raw: undefined }, logprobs: undefined, usage: {...same shape...} }`.

Structured output: return JSON text (`{"content":"Hello, world!"}`) and pass `output: Output.object({ schema: z.object({ content: z.string() }) })`; for streaming split the JSON across several `text-delta` chunks.

Agent test: give `doGenerate` an array of results to script a sequence. First result has `content: [{ type: 'tool-call', toolCallId: 'call-1', toolName: 'weather', input: '{"city":"San Francisco"}' }]` and `finishReason: { unified: 'tool-calls', raw: undefined }`; second has text and `unified: 'stop'`. Build `new ToolLoopAgent({ model, tools: { weather: tool({ description, inputSchema, execute }) } })`, run `agent.generate({ prompt })`, then assert tool side effects, `result.text`, and `model.doGenerateCalls` length (2 in the example).

UI message stream route mock: return `new Response(simulateReadableStream({ initialDelayInMs: 1000, chunkDelayInMs: 300, chunks: ['data: {"type":"start","messageId":"msg-123"}\n\n', ..., 'data: {"type":"finish"}\n\n', 'data: [DONE]\n\n'] }).pipeThrough(new TextEncoderStream()), { status: 200, headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive', 'x-vercel-ai-ui-message-stream': 'v1' } })`.

Note: the docs examples always give `finishReason` as `{ unified, raw }` and usage as nested `inputTokens` / `outputTokens` objects; copy that shape.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
