---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.run-multi-step-tool-loops-with-stopwhen-and-preparestep
name: run-multi-step-tool-loops-with-stopwhen-and-preparestep
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, stop-when, prepare-step, response-messages, prune-messages, tool-call-concurrency]
level: advanced
status: docs-checked
description: "Make generateText and streamText loop over tool results with stopWhen, vary settings per step with prepareStep, compact messages, and cap tool concurrency."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let the model call tools, receive results and continue, with explicit control of the loop.

## Multi-step with stopWhen
One generation is one step by default (`isStepCount(1)`). A step is one model generation plus execution of requested local tools. With `stopWhen`, the SDK feeds tool results back until there are no further tool calls or the condition is met.
```ts
import { generateText, isStepCount } from 'ai';
const { text, steps } = await generateText({ model, tools, stopWhen: isStepCount(5), prompt });
const allToolCalls = steps.flatMap(step => step.toolCalls);
```
Built-in conditions: `isStepCount(count)`, `hasToolCall(...toolNames)`, `isLoopFinished()` (never triggers, loop runs to natural end). Combine in an array or write custom ones (see agents Loop Control). Conditions are evaluated only when the last step contains tool results.

## prepareStep
Called before every step. Parameters: `model`, `stopWhen`, `stepNumber`, `steps`, `instructions`, `initialInstructions`, `messages`, `initialMessages`, `responseMessages`, `runtimeContext`, `toolsContext`, `experimental_sandbox`. Return overrides (or nothing for defaults):
```ts
prepareStep: async ({ stepNumber }) => stepNumber === 0
  ? { toolChoice: { type: 'tool', toolName: 'tool1' }, activeTools: ['tool1'] }
  : undefined,
```
Returned `instructions` and `messages` persist as the base for later steps. For long loops compact context with `pruneMessages`:
```ts
prepareStep: ({ messages }) => estimateTokens(messages) > 100_000
  ? { messages: pruneMessages({ messages, reasoning: 'all', toolCalls: 'before-last-3-messages', emptyMessages: 'remove' }) }
  : undefined,
```
To rebuild each step from scratch use `[...initialMessages, ...responseMessages.slice(-10)]`. `providerOptions` can also be returned (e.g. `prepareStep: forwardAnthropicContainerIdFromLastStep` from `@ai-sdk/anthropic` keeps a code-execution container).

## Observing steps
`onStepEnd({ stepNumber, text, toolCalls, toolResults, finishReason, usage, performance })` fires per step (zero-based `stepNumber`); `onToolExecutionStart/End` bracket each `execute`.

## Concurrency
Tool calls generated in one step run concurrently by default. `toolCallConcurrency: 1` forces sequential starts in generated order (when later calls depend on earlier side effects). It limits only SDK-executed calls, not provider-executed or client-side tools; on abort, active tools get the signal and queued ones do not start. `parallelToolCalls` provider options influence model generation instead.

## Carry history forward
`responseMessages` (also in `onEnd`) holds the assistant and tool messages: `messages.push(...responseMessages)`; for streamText `await result.responseMessages`.

## Gotchas
- Without `stopWhen` you get a single generation (default `isStepCount(1)`), so tool results are not sent back for a follow-up answer.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "structured output counts as a step" gotcha (it is on the structured-data page, not the cited one) and the otherModel placeholder.

Method: documentation only; no commands were run.
