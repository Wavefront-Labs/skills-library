---
id: computing-software.devops-ci-cd.concourse-ci.job-visibility-triggers-and-tags
name: job-visibility-triggers-and-tags
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [job, public, disable-manual-trigger, disable-reruns, tags, old-name, hooks]
level: practitioner
status: docs-checked
description: "Configure job-level options: rename with old_name, public logs, disabling manual triggers and reruns, job tags to pick workers (v8.3.0+), and job-level hooks."
sources:
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Smaller `job` fields from the Jobs page:

- `old_name` renames a job without losing history. Set `name` to the new name and `old_name` to the current one; once the pipeline is set and builds have transferred, remove `old_name`.
- `public: true` (default `false`) lets unauthenticated users view the job's build log. They can always see inputs, outputs and build status history. While it is set, `get` and `put` steps show their resource version metadata even if the resource itself is not `public`.
- `disable_manual_trigger: true` disables manual triggering from the web UI or `fly trigger-job`.
- `disable_reruns: true` disables rerunning builds from the web UI or `fly rerun-build`.
- `tags` (v8.3.0 or higher): worker tags for every step and `on_*` hook in the job. Child steps can override with their own tags but cannot clear them; to leave a step untagged, split the plan more finely.
- `on_success`, `on_failure`, `on_error`, `on_abort` and `ensure` at job level are equivalent to the step hooks of the same names.

```yaml
jobs:
  - name: new-name
    old_name: current-name
    plan:
      - get: 10m
```

Use `disable_manual_trigger` for jobs that must only run from upstream results, such as a production deploy gated by `passed` constraints. Use `public` only after checking build logs hold nothing sensitive.

## Checked

2026-11-04. Each field and default confirmed on the Jobs page (job schema and Job Hooks).

Method: documentation only; no commands were run.
