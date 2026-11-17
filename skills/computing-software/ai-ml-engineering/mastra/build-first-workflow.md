---
id: computing-software.ai-ml-engineering.mastra.build-first-workflow
name: build-first-workflow
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workflow, createstep, createworkflow, commit, getworkflow, workflow-result]
level: intro
status: docs-checked
description: "Build a Mastra workflow: createStep with schemas, createWorkflow().then().commit(), register on Mastra, run with start or stream, and read the status-based result."
sources:
  - https://mastra.ai/docs/workflows/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define typed steps, compose them into a workflow, register it, run it and read the result.

## Step
`createStep()` takes `id`, `inputSchema`, `outputSchema` (any Standard JSON Schema library: Zod, Valibot via `toStandardJsonSchema(...)` from `@valibot/to-json-schema`, ArkType) and an `execute` that can call code, APIs, agents or tools.
```typescript
import { createStep } from '@mastra/core/workflows'
import { z } from 'zod'

const step1 = createStep({
  id: 'step-1',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
  execute: async ({ inputData }) => ({ formatted: inputData.message.toUpperCase() }),
})
```

## Workflow
Give `createWorkflow()` an `id`, `inputSchema` and `outputSchema`, add steps with `.then()`, and finish with `.commit()`.
```typescript
export const testWorkflow = createWorkflow({
  id: 'test-workflow',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ output: z.string() }),
})
  .then(step1)
  .commit()
```
A workflow can be used as a step (`.then(childWorkflow)`); `cloneWorkflow(parent, { id: 'cloned-workflow' })` reuses logic under a new tracked id. Optional shared values across steps use `stateSchema` with `state` / `setState` in `execute`.

## Register and reference
```typescript
export const mastra = new Mastra({ workflows: { testWorkflow } })
const testWorkflow = mastra.getWorkflow('testWorkflow')
```
Prefer `mastra.getWorkflow()` over a direct import: it gives access to the instance config (logger, telemetry, storage, agents, vector stores) and full type inference. Use the registration key; `getWorkflowById()` looks up by `id` but without the same type inference.

## Run
Start waits for all steps; stream emits events.
```typescript
const run = await testWorkflow.createRun()
const result = await run.start({ inputData: { message: 'Hello world' } })
if (result.status === 'success') console.log(result.result)
```
For streaming: `const stream = run.stream({ inputData })`, iterate `stream.fullStream`, then `await stream.result` (same type as `run.start()`).

## Result type
`run.start()` and `stream.result` return a union on `status`: `success`, `failed`, `suspended`, `tripwire`, `paused`. Always available: `status`, `input`, `steps`, optionally `state`.
| Status | Extra properties |
| - | - |
| success | `result` |
| failed | `error` |
| tripwire | `tripwire` (`reason`, `retry?`, `metadata?`, `processorId?`) |
| suspended | `suspendPayload`, `suspended` |
| paused | none |

Check `status` first before reading status-specific fields. A successful result also lists each step's `status`, `payload` and `output` under `steps`.

## Also on the page
Studio shows a graph view, an input form generated from `inputSchema`, and live status. Active runs can be restarted with `run.restart()` or `workflow.restartAllActiveWorkflowRuns()`; the page also covers `RequestContext` access inside steps via `requestContext.get(...)`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
