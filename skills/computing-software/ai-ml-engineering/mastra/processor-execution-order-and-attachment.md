---
id: computing-software.ai-ml-engineering.mastra.processor-execution-order-and-attachment
name: processor-execution-order-and-attachment
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, processor, inputprocessors, outputprocessors, errorprocessors, guardrail, agent, memory]
level: practitioner
status: docs-checked
description: "Attach Mastra input, output and error processors to an agent, understand run order with memory, override per call, and write custom processors."
sources:
  - https://mastra.ai/docs/agents/processors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: wire processors into an agent correctly and predict the order they run.

## Attach
```typescript
import { Agent } from '@mastra/core/agent'
import { PrefillErrorHandler, TokenLimiter, ModerationProcessor } from '@mastra/core/processors'

const agent = new Agent({
  id: 'support-agent',
  name: 'support-agent',
  model: 'openai/<model>',
  instructions: '...',
  inputProcessors: [new TokenLimiter(4000), new ModerationProcessor({ model: 'openai/<small-model>' })],
  outputProcessors: [new ModerationProcessor({ model: 'openai/<small-model>' })],
  errorProcessors: [new PrefillErrorHandler()],
})
```
`inputProcessors` run before the LLM; `outputProcessors` during and after the response; `errorProcessors` when the LLM API call throws. Each array may be a function of `{ requestContext }` returning an array.

## Order
Processors run in array order. With memory enabled: input is `[Memory Processors] -> [your inputProcessors]` (history loads first); output is `[your outputProcessors] -> [Memory Processors]`. So an output guardrail calling `abort()` skips memory processors and nothing is saved.

## Error processors
Every agent adds whichever of `ProviderHistoryCompat`, `PrefillErrorHandler`, `UnsupportedFileHandler`, `StreamErrorRetryProcessor` your list lacks (matched by `id`; your instance wins). Error processors stop at the first one returning `{ retry: true }`; defaults put repairs ahead of the retrying one. Customize one by passing an instance with the same `id`, e.g. `new StreamErrorRetryProcessor({ maxRetries: 5 })` plus `maxProcessorRetries: 5` (a processor's `maxRetries` cannot raise the agent limit; error-processor retries stop after 3 by default). Set `errorProcessorDefaults: false` to disable all defaults. An empty list still gets the defaults.

## Per-call override
`generate()`/`stream()` accept the same three arrays and `maxProcessorRetries`; a passed array replaces the agent's array for that call only (memory/workspace processors still run). A per-call `errorProcessors` list replaces the resolved list, defaults included.
```typescript
await agent.stream('Summarize this', { inputProcessors: [new TokenLimiter(2000)], maxProcessorRetries: 5 })
```

## Custom processors
Implement `Processor` with an `id`. Hooks named on the page: `processInput` (once; gets `messages`, `systemMessages`, `abort()`), `processInputStep` (every loop step; return e.g. `{ model }` or `{ toolChoice: 'none' }`), `processLLMRequest`/`processLLMResponse`, `processOutputResult`, `processOutputStream` (return the part, or null/undefined to drop it), `processOutputStep`, `processAPIError`. Text is in `message.content.parts` (filter `part.type === 'text'`), not on `message.content`. `abort(reason, { retry: true })` in `processOutputStep` requests an LLM retry and needs `maxProcessorRetries` set; plain `abort()` yields a `tripwire` chunk (stream) or `result.tripwire` (generate). Output-method `state` persists for one request, keyed by processor id.

Related: computing-software.ai-ml-engineering.mastra.input-guardrails-injection-language

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
