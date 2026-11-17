---
id: computing-software.devops-ci-cd.tekton.tekton-pipelinerun-timeouts
name: tekton-pipelinerun-timeouts
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipelinerun, timeouts, finally, taskrunspecs]
level: practitioner
status: docs-checked
description: "Set PipelineRun timeouts for pipeline, tasks and finally, with the precedence order and the sum constraint."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelineruns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.timeouts` has three optional sub-fields (Go durations like `1h30m`, `60s`):
- `pipeline`: whole run; default is the global default (60 minutes unless `default-timeout-minutes` in `config-defaults` changes it). On expiry running child TaskRuns, including finally, are cancelled and the run fails.
- `tasks`: cumulative time of non-finally tasks. On expiry running tasks are cancelled, finally tasks run if `timeouts.finally` is set, and the run fails.
- `finally`: cumulative time of finally tasks (they run in parallel).

Constraint: `timeouts.pipeline >= timeouts.tasks + timeouts.finally`. Setting any to `"0"` means no timeout; to set `tasks` or `finally` to 0 you must also set `pipeline` to 0.

```yaml
timeouts:
  pipeline: "0h0m60s"
  tasks: "0h0m40s"
  finally: "0h0m20s"
```

Individual TaskRun timeout precedence, highest first: `taskRunSpecs[].timeout`, `pipeline.spec.tasks[].timeout`, `timeouts.tasks` or `timeouts.pipeline`, then the global default. A `taskRunSpecs` timeout cannot exceed pipeline-level constraints or validation fails. The singular `timeout` field is deprecated; use `timeouts`.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelineruns.md. Removed: nothing.

Method: documentation only; no commands were run.
