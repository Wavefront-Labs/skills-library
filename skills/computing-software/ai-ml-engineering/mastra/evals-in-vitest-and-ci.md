---
id: computing-software.ai-ml-engineering.mastra.evals-in-vitest-and-ci
name: evals-in-vitest-and-ci
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, vitest, expectevals, evals, ci, runevals, scorer, matchers]
level: practitioner
status: docs-checked
description: "Run Mastra runEvals as Vitest tests with expectEvals, expectEval, custom matchers and MastraEvalsReporter, and wire scorer experiments into CI."
sources:
  - https://mastra.ai/docs/evals/vitest-integration
  - https://mastra.ai/docs/evals/running-in-ci
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make evals fail the build like regular tests.

## Setup
`npm install @mastra/evals vitest` (Vitest 3, 4 or 5). In `vitest.config.ts`:
```typescript
import { MastraEvalsReporter } from '@mastra/evals/vitest'
export default defineConfig({ test: {
  reporters: ['default', new MastraEvalsReporter()],
  setupFiles: ['@mastra/evals/vitest/setup'], // or call registerEvalMatchers()
} })
```

## expectEvals (dataset, minimum pass rate)
```typescript
test('weather agent', { timeout: 60_000 }, async () => {
  await expectEvals({
    target: mastra.getAgent('weatherAgent'),
    data: [{ input: "What's the weather in London?" }],
    gates: [checks.calledTool('weatherTool'), checks.noToolErrors(), checks.includes('London')],
    scorers: [{ scorer: mastra.getScorer('answerRelevancyScorer'), threshold: 0.7 }],
  }).toPass(0.8)
})
```
`toPass(0.8)` needs 80% of items to pass every gate; scorer thresholds still compare the average regardless. `toPass()` with no argument requires all items to pass. Always await it: it resolves with the full `RunEvalsResult` and attaches scores for the reporter. Pass a per-test `timeout` (or `testTimeout`), since LLM evals exceed Vitest's 5-second default.

## expectEval (one item per test)
`test.for([...])('weather agent: $input', { timeout: 60_000 }, async item => { await expectEval({ target, data: item, gates: [...] }).toPass() })` gives one reporter entry per item, so one regression is one failing test.

## Matchers on a raw result
After `const result = await runEvals({...})`: `toHaveVerdict('passed')`, `toPassGates()` (fails if no gates), `toPassThresholds()` (fails if none), `toHaveScoreAbove(name, min)`, `toHaveScoreBelow(name, max)`. Workflow targets use a `WorkflowScorerConfig` for `scorers` (e.g. `{ trajectory: [scorer] }`, with `expectedTrajectory` on data items) and dot-path names such as `trajectory.code-trajectory-accuracy-scorer`.

## Any framework in CI
Jest, Mocha or Vitest all work if they support ESM. Resolve the target with `mastra.getAgent()` / `mastra.getWorkflow()` rather than importing it: a directly imported agent has no Mastra instance, so registry lookups in tools fail, scores are not persisted and trace-based trajectory scoring is unavailable. `runEvals` returns `scores` (averages per scorer) and `summary.totalItems`:
```typescript
const result = await runEvals({ data: [{ input: 'weather in Berlin', groundTruth: { expectedLocation: 'Berlin' } }],
  target: mastra.getAgent('weatherAgent'), scorers: [locationScorer] })
expect(result.scores['location-accuracy']).toBe(1)
```

## Rate limits
Vitest runs files in parallel and `runEvals` has its own `concurrency`, so traffic multiplies. If you hit provider limits, lower `concurrency` or set `fileParallelism: false`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
