---
id: computing-software.ai-ml-engineering.mastra.parallel-and-branch-steps
name: parallel-and-branch-steps
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, then, parallel, branch, workflow, classifier, control-flow]
level: practitioner
status: docs-checked
description: "Compose Mastra workflow steps with then, parallel and branch: schema matching rules, id-keyed outputs, resilient parallel steps, multi-branch semantics, classifier routing."
sources:
  - https://mastra.ai/docs/workflows/control-flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: wire steps sequentially, concurrently and conditionally while keeping schemas consistent.

## Schema rules
- First step `inputSchema` must match the workflow `inputSchema`; final step `outputSchema` must match the workflow `outputSchema`.
- Each step `outputSchema` must match the next step `inputSchema`; if not, use input data mapping.

## `.then()`
Runs steps in order; each can read the previous step's result: `.then(step1).then(step2).commit()`.

## `.parallel([a, b])`
All steps run simultaneously and all must finish before the next step. The output is an object keyed by each step `id`, so the next step's `inputSchema` must have those keys:
```typescript
const step3 = createStep({
  id: 'combine-step',
  inputSchema: z.object({
    'format-step': z.object({ formatted: z.string() }),
    'count-step': z.object({ count: z.number() }),
  }),
  outputSchema: z.object({ result: z.string() }),
  execute: async ({ inputData }) => ({
    result: `${inputData['format-step'].formatted} (${inputData['count-step'].count} characters)`,
  }),
})
// workflow: .parallel([step1, step2]).then(step3).commit()
```
Failure: if any parallel step throws, the whole parallel block fails. For resilience, catch inside the step and return a typed result such as `{ brief: null, failed: true }`; the downstream step filters with `Object.values(inputData).filter(v => !v.failed && v.brief)`.

## `.branch([[condition, step], ...])`
Every condition is evaluated and every one returning `true` runs its step, so more than one branch can run. All branch steps need the same `inputSchema` and `outputSchema`.
```typescript
.then(step1)
.branch([
  [async ({ inputData: { value } }) => value > 10, stepA],
  [async ({ inputData: { value } }) => value <= 10, stepB],
])
```
Output is keyed by each executed step's `id` (like parallel). Write mutually exclusive conditions when exactly one path should run, and do not end with an unconditional `true` fallback unless you want it to run alongside the match. A following step should declare optional fields for each possible branch output, e.g. `'high-value-step': z.object({...}).optional()`.

## Route with a classifier
A configured `Classifier` (from `@mastra/core/classifier`) produces typed answers before `.branch()`:
```typescript
createWorkflow({ id: 'ticket-triage', inputSchema: z.object({ message: z.string() }), outputSchema: z.any() })
  .map({ message: { initData: true, path: 'message' } })
  .classifier(router)
  .branch([
    [async ({ inputData }) => inputData.answers.route.choice === 'billing', billingStep],
    [async ({ inputData }) => inputData.answers.route.choice === 'support', supportStep],
    [async ({ inputData }) => inputData.answers.route.choice === 'other', fallbackStep],
  ])
  .commit()
```
Question types give `choice`, `score` or `probability` (boolean questions expose `P(true)` as `probability`); apply an explicit threshold when routing on those. `choice` is typed as the criteria-key union or `undefined`. If the decision model refuses, the answer is `{ type: 'refusal' }` and those fields are `undefined`, so a refused question matches no condition; add a check on `inputData.answers.route.type === 'refusal'` to handle it.

Not covered here: loops, `.foreach()`, input mapping details and nested workflows, which are on the same source page.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
