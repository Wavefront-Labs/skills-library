---
id: computing-software.ai-ml-engineering.mastra.workflow-human-approval
name: workflow-human-approval
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workflow, human-in-the-loop, suspend, resume, bail, approval]
level: practitioner
status: docs-checked
description: "Add human approval to a Mastra workflow: suspend with a reason, read suspendPayload, resume with feedback, bail on rejection, and chain multi-step approvals."
sources:
  - https://mastra.ai/docs/workflows/human-in-the-loop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pause a workflow for a person, show them why, then continue or stop cleanly.

## Pause with context
Give the step a `resumeSchema` and a `suspendSchema` carrying a reason:
```typescript
const step1 = createStep({
  id: 'step-1',
  inputSchema: z.object({ userEmail: z.string() }),
  outputSchema: z.object({ output: z.string() }),
  resumeSchema: z.object({ approved: z.boolean() }),
  suspendSchema: z.object({ reason: z.string() }),
  execute: async ({ inputData, resumeData, suspend }) => {
    const { approved } = resumeData ?? {}
    if (!approved) return await suspend({ reason: 'Human approval required.' })
    return { output: `Email sent to ${inputData.userEmail}` }
  },
})
```

## Show the user why
```typescript
const result = await run.start({ inputData: { userEmail: 'alex@example.com' } })
if (result.status === 'suspended') {
  const suspendStep = result.suspended[0]
  const payload = result.steps[suspendStep[0]].suspendPayload // { reason: ... }
}
```

## Resume with the answer
`await run.resume({ step: 'step-1', resumeData: { approved: true } })`.

## Reject with `bail()`
`bail()` stops the workflow at the step without an error: the workflow completes with a `success` status and later logic in the step is skipped. Check for an explicit rejection before the suspend check:
```typescript
execute: async ({ inputData, resumeData, suspend, bail }) => {
  const { approved } = resumeData ?? {}
  if (approved === false) return bail({ reason: 'User rejected the request.' })
  if (!approved) return await suspend({ reason: 'Human approval required.' })
  return { message: `Email sent to ${inputData.userEmail}` }
}
```

## Multi-turn
Chain steps (`.then(step1).then(step2)`), each with its own `resumeSchema` and `suspendSchema`. Resume each suspended step in sequence with a separate `resume()` call (`step: 'step-1'`, then `step: 'step-2'`), which keeps UI feedback and input handling clear per stage.

## Checked
Method: 2026-11-08 read the cited Mastra human-in-the-loop workflows page in full (served as markdown) and compared each claim. All claims matched the page; no content changes.
