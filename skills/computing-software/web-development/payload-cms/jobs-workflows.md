---
id: computing-software.web-development.payload-cms.jobs-workflows
name: jobs-workflows
category: computing-software
field: web-development
product: payload-cms
tags: [job-workflows, workflow-tasks, durable-execution, concurrency-key]
level: advanced
status: docs-checked
description: "Chain tasks in a workflow so completed steps are cached on retry, and prevent duplicate runs with a concurrency key."
sources:
  - https://payloadcms.com/docs/jobs-queue/workflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Job workflows

Goal: run several tasks in order with resumable failures.

```ts
jobs: {
  tasks: [/* createProfile, sendEmail, addToList */],
  workflows: [
    {
      slug: 'onboardUser',
      inputSchema: [{ name: 'userId', type: 'text', required: true }],
      handler: async ({ job, tasks }) => {
        await tasks.createProfile('step1', { input: { userId: job.input.userId } })
        await tasks.sendEmail('step2', { input: { userId: job.input.userId } })
        await tasks.addToList('step3', { input: { userId: job.input.userId } })
      },
    },
  ],
}
```

Each call takes a unique step ID (`'step1'`) and the task input. Workflow options: `slug`, `handler`, `inputSchema`, `interfaceName`, `label`, `queue` (default `default`), `retries`, `concurrency`.

Recovery: if step 2 fails, the whole handler re-runs but completed steps return cached output without re-executing, so step 1 does not duplicate its work. Task-level `retries` applies per step.

Concurrency control:

```ts
concurrency: ({ input }) => `sync:${input.documentId}`
```

Jobs sharing a key run one at a time.

Verify: make step 2 fail once and confirm step 1 runs only once.

## Checked

2026-11-04. Read jobs-queue/workflows (docs/jobs-queue/workflows.mdx). Confirmed: the workflow option table (slug, handler, inputSchema, interfaceName, label, queue defaulting to "default", retries, concurrency), the tasks.name('stepId', { input }) call form, completed tasks returning cached output on re-run without duplicating work, and the concurrency key function with jobs sharing a key running one at a time.
Method: documentation only; no commands were run.
