---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-finally-task-status
name: tekton-pipeline-finally-task-status
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, finally, status, tasks-status]
level: advanced
status: docs-checked
description: "Check individual task status with tasks.NAME.status and the aggregate tasks.status in Tekton finally tasks, including possible values and guarding with when."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Finally tasks can inspect how the main tasks ended.

`$(tasks.<name>.status)` for a single PipelineTask is one of: `Succeeded` (the TaskRun completed successfully), `Failed` (it failed or was cancelled by the user), `None` (the task was skipped or has no execution information).

`$(tasks.status)` is the aggregate over all `tasks`: `Succeeded` (all succeeded), `Failed` (one or more failed), `Completed` (all completed successfully including skipped ones), `None` (none of the above, for example some tasks pending, running, cancelled or timed out).

```yaml
finally:
  - name: finaltask
    params:
      - name: aggregateTasksStatus
        value: "$(tasks.status)"
    taskSpec:
      params:
        - name: aggregateTasksStatus
      steps:
        - image: ubuntu
          name: check-task-status
          script: |
            if [ $(params.aggregateTasksStatus) == "Failed" ]
            then
              echo "one or more tasks failed"
            fi
```

Unlike normal tasks, `when` in a finally task can also operate on these execution statuses, in addition to params and results, so a notify task can run only when something failed.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
