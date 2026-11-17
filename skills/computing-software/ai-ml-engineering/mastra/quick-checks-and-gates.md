---
id: computing-software.ai-ml-engineering.mastra.quick-checks-and-gates
name: quick-checks-and-gates
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, scorer, runevals, quick-checks, gates, verdicts, thresholds, ci, evals]
level: practitioner
status: docs-checked
description: "Use Mastra Quick Checks as zero-LLM assertions and combine gates and score thresholds in runEvals to get a passed, scored or failed verdict for CI."
sources:
  - https://mastra.ai/docs/evals/quick-checks
  - https://mastra.ai/docs/evals/gates-and-verdicts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: assert on text and tool use without an LLM, and turn eval results into one verdict.

## Quick Checks
```typescript
import { checks } from '@mastra/evals/checks'
import { runEvals } from '@mastra/core/evals'
const result = await runEvals({
  data: [{ input: 'What is the weather in Brooklyn?' }],
  target: weatherAgent,
  scorers: [checks.includes('Brooklyn'), checks.calledTool('get_weather'), checks.noToolErrors()],
})
// result.scores: { 'check-includes': 1, 'check-called-tool': 1, 'check-no-tool-errors': 1 }
```
- Text: `includes`, `excludes`, `equals` (case-insensitive unless `{ ignoreCase: false }`), `matches(regex)`, `similarity` (Dice, 0-1 or binary with `threshold`).
- Tools: `calledTool(name)` (at least N times), `didNotCall`, `toolOrder([...])`, `maxToolCalls(n)`, `usedNoTools()`, `noToolErrors()`.
- They mix with LLM scorers in the same `scorers` array and can be attached to agents with `sampling` for live scoring. Each is a `createScorer()` with only preprocess and generateScore steps. Use LLM scorers for subjective or semantic judging.

## Gates and thresholds
```typescript
const result = await runEvals({
  data: [{ input: 'What is the weather in Brooklyn?' }],
  target: weatherAgent,
  gates: [checks.calledTool('get_weather'), checks.noToolErrors()],
  scorers: [
    { scorer: faithfulnessScorer, threshold: 0.7 },
    { scorer: hallucinationScorer, threshold: { max: 0.3 } },
    checks.includes('Brooklyn'), // tracked only
  ],
})
```
- Gates must average 1.0 across the items they could score. `notScorable()` items are excluded; a gate that throws counts as 0. Gates run before regular scorers.
- A numeric `threshold` is a minimum; use `{ max }` where high is bad, `{ min, max }` for a band. Compared against the average, with `notScorable()` results left out.
- `scorers` is optional if at least one gate exists; a run with neither throws.
- Verdict: `failed` (a gate averaged below 1.0), `scored` (gates passed, a threshold missed), `passed` (all met). It is omitted when there are no gates/thresholds or every one returned `notScorable()`.
- Details: `result.gateResults`, `result.thresholdResults` (with `averageScore`).

## CI pattern
```typescript
if (result.verdict === 'failed') { console.error(result.gateResults?.filter(g => !g.passed)); process.exit(1) }
if (result.verdict === 'scored') console.warn(result.thresholdResults?.filter(t => !t.passed))
```

## Checked
Method: 2026-11-08 read the Mastra Quick checks and Gates and verdicts docs pages in full (served as markdown). The check names, scoring, gate/threshold semantics, verdict rules and CI pattern all match the pages; no claims removed. Live-scoring sampling is shown on the page; the page's example model IDs were not copied.
