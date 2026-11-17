---
id: computing-software.ai-ml-engineering.mastra.live-evals-with-scorers
name: live-evals-with-scorers
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, scorer, evals, live-evaluations, sampling, built-in-scorers, runevals, mastra-evals]
level: practitioner
status: docs-checked
description: "Attach Mastra scorers to agents and workflow steps for live evals: sampling, eligibility filters, score persistence and registration, plus a map of the built-in scorers."
sources:
  - https://mastra.ai/docs/evals/overview
  - https://mastra.ai/docs/evals/built-in-scorers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: score agent and workflow outputs automatically in the background and keep the scores.

## Setup
`npm install @mastra/evals@latest`. Scorers return scores (typically 0 to 1) from model-graded, rule-based or statistical methods.

## Agent scorers
```typescript
import { createAnswerRelevancyScorer, createToxicityScorer } from '@mastra/evals/scorers/prebuilt'
export const evaluatedAgent = new Agent({ id: 'evaluated-agent', /* ... */
  scorers: {
    relevancy: { scorer: createAnswerRelevancyScorer({ model: 'your-model' }), sampling: { type: 'ratio', rate: 0.5 } },
    safety: { scorer: createToxicityScorer({ model: 'your-model' }), sampling: { type: 'ratio', rate: 1 } },
  },
})
```
Workflow steps take the same `scorers` map on `createStep({...})`; each scorer sees that step's own input and output.

## How live scoring behaves
- Runs asynchronously, never blocking responses.
- `sampling.rate` 0-1 (1 = all, 0 = off). The decision is deterministic per trace ID, so scorers at the same rate score the same traces. With no trace it uses the run ID. If trace sampling declined the trace, scorers skip the run.
- `filter` restricts eligibility before sampling, e.g. `{ op: 'eq', left: { path: 'requestContext.plan' }, right: { literal: 'enterprise' } }`. It can reference `requestContext.*`, `entity.*`, `entityType`, `source`, `threadId`, `resourceId`, `projectId`; operators `eq ne lt lte gt gte in notIn exists notExists truthy falsy and or not`. An unknown root fails at agent construction. Filters cannot see run input or output; for that, return `notScorable()` from a scorer step. To limit which messages a scorer sees, use `filterRun()`.

## Persistence
Scores go to the `mastra_scorers` table when `storage` is configured and the scorer is registered. Agent/step scorers register themselves; scorers passed straight to `runEvals()` (including Quick Checks) need `new Mastra({ storage, scorers: { ... } })`. Registration matches by scorer ID only (every `checks.calledTool()` has ID `check-called-tool`), but the registered instance supplies the stored `description`, so register with a representative argument. Without registration scoring still works but each save warns `Scorer with id <id> not found` and nothing is stored.

## Trace scoring and Studio
Historical traces can be scored once observability is configured and scorers are registered on `Mastra`; in Studio use Observability, the scorers list, score results (save a result as a dataset item) and the agent Evaluate tab.

## Built-in scorers (ids)
- Accuracy/reliability: answer-relevancy, answer-similarity, faithfulness, hallucination (lower is better), completeness, content-similarity, textual-difference, tool-call-accuracy, trajectory-accuracy, prompt-alignment, multi-turn-judge.
- Context quality: context-precision (ranking, Mean Average Precision) and context-relevance (relevance plus usage and gaps); both accept static or dynamically extracted context.
- Output quality: tone-consistency, toxicity (lower better), bias (lower better), keyword-coverage.
- Zero-LLM `checks.*` for deterministic assertions.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
