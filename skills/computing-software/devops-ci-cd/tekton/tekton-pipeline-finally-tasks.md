---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-finally-tasks
name: tekton-pipeline-finally-tasks
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, finally, cleanup, pipelinerun-status]
level: practitioner
status: docs-checked
description: "Run Tekton finally tasks after all pipeline tasks complete, and read how they change the final PipelineRun status and reason."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`finally` tasks use the same syntax as `tasks` (a valid name plus `taskRef` or `taskSpec`) and are guaranteed to run, in parallel, after all `tasks` have completed, whether they succeeded or failed.

```yaml
spec:
  tasks:
    - name: tests
      taskRef:
        name: integration-test
  finally:
    - name: cleanup-test
      taskRef:
        name: cleanup
```

Status calculation includes finally tasks:
- All tasks and finally tasks succeed: `true`, reason `Succeeded`.
- Some tasks skipped by `when`, the rest successful, finally successful: `true`, reason `Completed`.
- Any finally task fails (even if all tasks succeeded): `false`, `Failed`.
- A failed main task: `false`, `failed`, regardless of finally outcome.

Transitions are `Started` to `Running` to `Succeeded`, `Completed` or `Failed`. Finally tasks accept params, workspaces, matrix and `displayName` like normal tasks, and can consume task results and pipeline results.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
