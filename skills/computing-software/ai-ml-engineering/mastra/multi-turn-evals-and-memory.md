---
id: computing-software.ai-ml-engineering.mastra.multi-turn-evals-and-memory
name: multi-turn-evals-and-memory
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, dataset, experiment, runevals, multi-turn, memory, threads, evals]
level: advanced
status: docs-checked
description: "Evaluate Mastra agents across conversations with runEvals turns, pick scorers that read all turns, and run evals on memory-enabled agents with shared or per-item threads"
sources:
  - https://mastra.ai/docs/evals/multi-turn
  - https://mastra.ai/docs/evals/evals-with-memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: test behaviour that emerges across turns, including recall from memory.

## `inputs`: one accumulated score
```typescript
await runEvals({
  data: [{ inputs: ['What is the weather in Brooklyn?', 'What about tomorrow?', 'Compare the two forecasts.'] }],
  target: weatherAgent,
  scorers: [checks.calledTool('get_weather', { times: 2 }), checks.includes('Brooklyn')],
})
```
Each input runs `agent.generate()` sequentially on one fresh thread; scorers get the accumulated output. `run.input` is only the first turn's input. An empty `inputs` throws a `MastraError`. Single-turn (`input`) and multi-turn items can be mixed in one call.

- Cross-turn recall needs the agent to have memory configured; without it turns still run but in isolation, and `runEvals` warns. `runEvals` generates the `threadId` and a `resourceId`; pin the resource with `targetOptions: { memory: { resource: 'user-42' } }`.
- Scorer reach: Quick Checks and custom scorers reading `run.output` see the whole conversation; `createMultiTurnJudgeScorer({ model, criterion })` grades every assistant turn against one plain-English criterion (1 or 0); prebuilt LLM judges (answer relevancy, faithfulness, etc.) grade only the last assistant message and the first input. Trajectory scorers use the last turn's span when traces exist.
- Custom whole-conversation judge: `extractAgentResponseMessages(run.output)` from `@mastra/evals/scorers/utils` returns each assistant message's text.

## `turns`: per-turn gates and scorers
```typescript
data: [{ turns: [
  { input: 'What is the weather in Brooklyn?', gates: [checks.calledTool('get_weather')] },
  { input: 'What about tomorrow?', gates: [checks.calledTool('get_weather')],
    scorers: [{ scorer: checks.similarity('tomorrow forecast'), threshold: 0.5 }] },
] }]
```
Per-turn gates/scorers see only that turn's input and output, fold into the verdict (failing turn gate = `failed`, missed threshold = `scored`), and report in `result.turnResults[i]` (averaged by turn index across conversations). Top-level `scorers`/`gates` still run over the accumulated output. `turns` cannot be combined with `input`/`inputs`. With storage, per-turn scores are persisted with `metadata.turnIndex` and the shared `threadId`.

## Memory-enabled agents (thread scope, observational memory)
Without a thread you get `ObservationalMemory (scope: 'thread') requires a threadId...`. Options:
- Shared thread: create it first (`await (await agent.getMemory())!.createThread({ threadId, resourceId })`), then `runEvals({ target, scorers, data, targetOptions: { memory: { thread: threadId, resource: resourceId } } })`. `targetOptions` is global per call; there is no per-item override.
- Per-item threads: call `runEvals` once per item with a unique thread (create it before), then average `result.scores[scorer.id]` yourself.
- Stored dataset with explicit threads: put `{ threadId, resourceId }` in each item's `metadata` and use `dataset.startExperiment({ scorers, task: async ({ input, metadata }) => agent.generate(input, { memory: { thread, resource } }) })`. A registered memory-enabled agent target instead gets a fresh thread per item by default.
- Pre-seeding `RequestContext` with `MastraMemory` is not a supported way to drive memory.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
