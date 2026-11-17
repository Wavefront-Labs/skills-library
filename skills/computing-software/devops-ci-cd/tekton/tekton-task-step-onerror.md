---
id: computing-software.devops-ci-cd.tekton.tekton-task-step-onerror
name: tekton-task-step-onerror
category: computing-software
field: devops-ci-cd
product: tekton
tags: [task, steps, onerror, exit-code]
level: practitioner
status: docs-checked
description: "Use step onError continue and continueAndFail in a Tekton Task, read earlier step exit codes, and understand result behaviour after a failed step."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a failing step skips the remaining steps and fails the TaskRun. `onError` on a step takes `continue`, `stopAndFail` or `continueAndFail`; the default behaviour described above is stop-and-fail.

- `continue`: the step does not fail the TaskRun and later steps run. The original script exit code is recorded in the container terminated state (visible with `kubectl get tr NAME -o json | jq .status`).
- `continueAndFail`: later steps still run but the TaskRun fails once they finish. If several steps fail, the first failing `continueAndFail` step is reported. An OOM-killed step or sidecar always takes precedence over a `continueAndFail` exit code.

```yaml
steps:
  - image: docker.io/library/golang:latest
    name: run-unit-tests
    onError: continueAndFail
    script: |
      go test ./...
  - image: registry.access.redhat.com/ubi9/ubi-minimal
    name: publish-test-report
    script: |
      ./publish-report
```

A later step can read an earlier exit code with `cat $(steps.step-<step-name>.exitCode.path)` (or `steps.step-unnamed-<index>.exitCode.path` for an unnamed step).

If an ignored-failure step wrote a result file before failing, a consuming task in a pipeline can use it; if the step failed before writing it, any consumer of that result makes the pipeline fail with `InvalidTaskResultReference`.

## Checked

Checked 2026-11-08 against docs/tasks.md in tektoncd/pipeline (main), reading the onError, exitCode, result-with-onError and breakpoint subsections in full (partial read of a long file; other sections not read). All claims confirmed; the "(default)" label was reworded because the docs describe the default behaviour but do not name the value.

Method: documentation only; no commands were run.
