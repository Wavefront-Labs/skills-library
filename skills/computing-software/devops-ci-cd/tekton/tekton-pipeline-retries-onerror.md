---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-retries-onerror
name: tekton-pipeline-retries-onerror
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, retries, onerror, failure-handling]
level: practitioner
status: docs-checked
description: "Set retries on a PipelineTask and use onError continue to ignore a task failure, including how results behave and the limits of combining them."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`retries` per PipelineTask: the number of times Tekton re-runs a failed task. Default is no retry. Retries run even when other tasks have failed, unless the `PipelineRun` was cancelled or gracefully cancelled. Use it for flaky network or dependency steps.

```yaml
tasks:
  - name: build-the-image
    retries: 1
    taskRef:
      name: build-push
```

`onError` takes `stopAndFail` (default) or `continue`. With `continue`, a failed task does not fail the PipelineRun and the rest keep executing:

```yaml
- name: task1
  onError: continue
```

The PipelineRun message then reads like `Tasks Completed: 1 (Failed: 1 (Ignored: 1), Cancelled 0), Skipped: 0`, while the TaskRun itself stays failed with reason `FailureIgnored`.

If the failed task initialised a result before failing, consumers can read `$(tasks.task1.results.result1)`. If it did not, a consumer with `stopAndFail` fails the run with `InvalidTaskResultReference`, whereas a consumer with `continue` is skipped with reason `Results were missing`.

Setting `retries` and `onError: continue` on the same PipelineTask is not allowed.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
