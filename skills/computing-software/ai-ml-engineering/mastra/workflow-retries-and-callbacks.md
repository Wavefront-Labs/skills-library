---
id: computing-software.ai-ml-engineering.mastra.workflow-retries-and-callbacks
name: workflow-retries-and-callbacks
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workflow, retries, retryconfig, onfinish, onerror, error-handling, bail]
level: practitioner
status: docs-checked
description: "Handle Mastra workflow failures: check result status and failed steps, onFinish and onError callbacks, workflow retryConfig, step retries, fallback branches, bail and throw."
sources:
  - https://mastra.ai/docs/workflows/error-handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: detect, retry and report workflow failures.

## Inspect the result
`result.status` is `success`, `failed`, `suspended`, `paused` or `tripwire`; `result` holds output on success, `error` on failure, and `steps` has per-step status and output. Find the failing step:
```typescript
if (result.status === 'failed') {
  for (const [stepId, stepResult] of Object.entries(result.steps)) {
    if (stepResult.status === 'failed') console.error(`Step ${stepId} failed:`, stepResult.error)
  }
}
```

## Lifecycle callbacks
Set in the workflow's `options`:
```typescript
createWorkflow({
  id: 'data-pipeline',
  inputSchema: ..., outputSchema: ...,
  options: {
    onFinish: async result => { /* any status */ },
    onError: async errorInfo => { /* failed or tripwire */ },
  },
})
```
- `onFinish` runs for success, failed, suspended or tripwire; `onError` only for `failed` or `tripwire`.
- Both receive `status`, `steps`, `runId`, `workflowId`, `resourceId?`, `getInitData()`, `mastra`, `requestContext`, `logger`, `state`; `onFinish` adds `result` (success) and `error`; `onError` gets `error` and `tripwire`.
- They are awaited but not durable or retried: use workflow steps for work that must complete reliably.
- Errors thrown inside callbacks are caught and logged; they do not change the workflow result.

## Retries
Workflow-wide, applying to all steps: `createWorkflow({ retryConfig: { attempts: 5, delay: 2000 } })`. Per step, overriding the workflow setting: `createStep({ ..., retries: 3 })`. Retries are meant for transient errors such as unavailable external services; a step triggers them by throwing.

## Fallback path
Catch in a step and return a status, then `.branch([[cond ok, step2], [cond error, fallback]])`.

## Other tools
- `getStepResultAsync(step1)` in a later step returns a previous step's result, or `null` if it has not completed successfully.
- `bail({ ... })` exits early with a successful result (the payload becomes the step output and execution ends).
- `throw new Error('error')` exits with an error.

## Checked
Method: 2026-11-08 read the cited Mastra workflow error-handling page in full (served as markdown) and compared each claim. All claims matched; no content changes.
