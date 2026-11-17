---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.steer-and-queue-messages-in-running-agent
name: steer-and-queue-messages-in-running-agent
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [loop-control, steering, experimental-createsteering, queue, toolloopagent]
level: advanced
status: docs-checked
description: "Inject a correction or follow-up into a running agent loop with experimental_createSteering, steer and queue, and read delivery outcomes and saved steering messages."
sources:
  - https://ai-sdk.dev/docs/agents/loop-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a user add a message while an agent is still working. Experimental.

```ts
import { experimental_createSteering, isStepCount, streamText } from 'ai';

const steering = experimental_createSteering();
const result = streamText({ model, tools: { weather }, stopWhen: isStepCount(10), prompt: 'What is the weather in Paris?', experimental_steering: steering });

const outcome = await steering.steer('I meant Paris, Texas.');
```
Works the same with `generateText` and `ToolLoopAgent`: create the steering object before the call, pass `experimental_steering: steering` to `agent.generate(...)`, call `steer()` while it runs, then await the run.

Delivery rules:
- A steering message is added at the next step boundary, after the current step and its tool calls finish; running tools are never interrupted. Messages go in sent order, each its own user message; ones sent before the loop starts join the first step.
- If the model finishes while a message waits, the loop continues one more step. Stop conditions still apply: `generateText` and `streamText` stop after one step by default, so set `stopWhen`; agents default to 20 steps.
- A steering object serves one call only. `prepareStep` and `onStepStart` see steering messages inside `messages`. `createAgentUIStream` throws if given a steering object with an agent other than `ToolLoopAgent`.

Queue: `steering.queue('Then add tests for it.')` waits until the current task finishes (a final answer with no tool calls), one queued message per task, in queue order; waiting steering messages go first. A cut-off response (finish reason `length` or `content-filter`) does not finish a task, so the loop ends and the queued message is reported as not delivered.

Outcome: `steer()` and `queue()` never reject; they resolve with `{ type: 'delivered', stepNumber }` or a not-delivered result with `reason` and `message`. Reasons: `finished`, `removed-by-prepare-step`, `stop-condition`, `waiting-for-tool-results` (for example a tool approval), `aborted`, `error`. Pass `{ id: messageId }` as the second argument so a retry with the same id returns the first outcome.

Saving: steering messages are not in `responseMessages`. Rebuild the conversation with `[...initialMessages, ...result.steps.flatMap(step => [...(step.experimental_steeringMessages ?? []), ...step.response.messages])]`.

Gotcha: if `prepareStep` returns rebuilt messages, append `experimental_steeringMessages` for the current step and each earlier step's `step.experimental_steeringMessages`, in order, or they are dropped.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
