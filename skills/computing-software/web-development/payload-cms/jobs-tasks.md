---
id: computing-software.web-development.payload-cms.jobs-tasks
name: jobs-tasks
category: computing-software
field: web-development
product: payload-cms
tags: [job-tasks, task-config, inputschema, task-retries]
level: advanced
status: docs-checked
description: "Define tasks in config with slug, handler, inputSchema, outputSchema, retries, onFail, onSuccess, schedule and concurrency."
sources:
  - https://payloadcms.com/docs/jobs-queue/tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Job tasks

Goal: define a unit of background work.

```ts
export default buildConfig({
  jobs: {
    tasks: [
      {
        slug: 'createPost',
        retries: 2,
        inputSchema: [{ name: 'title', type: 'text', required: true }],
        outputSchema: [{ name: 'postID', type: 'text', required: true }],
        handler: async ({ input, job, req }) => {
          const post = await req.payload.create({ collection: 'posts', data: { title: input.title }, req })
          return { output: { postID: String(post.id) } }
        },
      },
    ],
  },
})
```

Options: `slug` (unique across tasks and workflows), `handler` (function or a string path to a file), `inputSchema` and `outputSchema` (field arrays that generate types), `interfaceName`, `label`, `onFail`, `onSuccess`, `retries` (undefined inherits the workflow's value or means none), `concurrency`, `schedule`.

Handlers receive `input`, `job` and `req`; the page example passes `req` to the nested Local API call. A handler fails by throwing an error, and `throw new JobCancelledError('...')` stops the job being retried.

Payload generates types from `inputSchema` and `outputSchema`, which is what types `payload.jobs.queue({ task: 'createPost', input })`.

Verify: queue the task and run it; if it throws, the job document has `hasError` and the message in `error`.

## Checked

2026-11-04. Read jobs-queue/tasks (docs/jobs-queue/tasks.mdx). Confirmed: the option table (slug, handler, inputSchema, outputSchema, interfaceName, label, onFail, onSuccess, retries, concurrency, schedule), the retries inheritance rule, the createPost example, and failure by throwing with JobCancelledError to prevent retries. Removed: the unconfirmed shared-transaction explanation, the generate:types command (not on the page) and the output-on-job-document verify step.
Method: documentation only; no commands were run.
