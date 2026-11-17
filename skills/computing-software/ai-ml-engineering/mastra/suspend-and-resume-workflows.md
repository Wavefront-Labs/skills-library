---
id: computing-software.ai-ml-engineering.mastra.suspend-and-resume-workflows
name: suspend-and-resume-workflows
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, suspend, resume, workflow, snapshot, suspenddata, sleep]
level: practitioner
status: docs-checked
description: "Pause a Mastra workflow step with suspend(), resume it with resumeData, read suspendData, find suspended steps, recover runs from storage, and use sleep."
sources:
  - https://mastra.ai/docs/workflows/suspend-and-resume
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop a workflow mid-run to wait for input, a callback or time, then continue from saved state.

Suspension saves a snapshot to your configured storage provider; snapshots persist across deployments and restarts.

## Suspend
Declare `resumeSchema` (and optionally `suspendSchema`) on the step and call `suspend()` unless the resume data satisfies the condition:
```typescript
const step1 = createStep({
  id: 'step-1',
  inputSchema: z.object({ userEmail: z.string() }),
  outputSchema: z.object({ output: z.string() }),
  resumeSchema: z.object({ approved: z.boolean() }),
  execute: async ({ inputData, resumeData, suspend }) => {
    const { approved } = resumeData ?? {}
    if (!approved) return await suspend({})
    return { output: `Email sent to ${inputData.userEmail}` }
  },
})
```

## Resume
```typescript
const run = await workflow.createRun()
await run.start({ inputData: { userEmail: 'alex@example.com' } })
await run.resume({ step: step1, resumeData: { approved: true } })
```
- `step` can be the step object (type-safe `resumeData`) or a step id string (useful when it comes from user input or a database).
- With only one suspended step you can omit `step`; the last suspended step resumes.
- To resume with only a `runId`, create a run instance first: `workflow.createRun({ runId: '123' })` then `run.resume({ resumeData })`.
- Call `resume()` from anywhere (HTTP endpoint, event handler, timer).

## suspendData
Pass context to `suspend({ reason, requestDetails })` (with a matching `suspendSchema`). On resume the step receives the same object as `suspendData` in `execute`.

## Find suspended steps
```typescript
const result = await run.start({ inputData })
if (result.status === 'suspended') {
  await run.resume({ step: result.suspended[0], resumeData: { approved: true } })
}
```
`result.suspended` lists ids of suspended workflows and steps, e.g. `['nested-workflow', 'step-1']`, usable as `step`.

## Recover from storage
```typescript
import { createWorkflowStateReader } from '@mastra/core/workflows'
const state = await workflow.getWorkflowRunById('run-123')
if (state?.status === 'suspended') {
  const reader = createWorkflowStateReader(state)
  const suspendedStep = reader.getSuspendedStep()
  const approvalLabel = reader.getResumeLabel('approve')
  const run = await workflow.createRun({ runId: state.runId })
  await run.resume({
    step: approvalLabel?.stepId ?? suspendedStep?.path,
    resumeData: { approved: true },
    forEachIndex: approvalLabel?.foreachIndex,
  })
}
```
For nested workflows `suspendedStep.path` is the resume path; for `foreach` suspensions, matching labels include `foreachIndex` when they point at one iteration.

## Sleep
`.sleep()` (milliseconds) and `.sleepUntil()` (a date) pause at workflow level and set status `waiting`; `suspend()` pauses inside a step and sets `suspended`.

## Checked
Method: 2026-11-08 read the cited Mastra suspend-and-resume page in full (served as markdown) and compared every claim. All claims matched; one wording change (resuming with only a runId, not "from another process"). No other changes.
