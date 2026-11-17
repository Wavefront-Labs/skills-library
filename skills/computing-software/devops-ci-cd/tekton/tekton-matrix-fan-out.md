---
id: computing-software.devops-ci-cd.tekton.tekton-matrix-fan-out
name: tekton-matrix-fan-out
category: computing-software
field: devops-ci-cd
product: tekton
tags: [matrix, fan-out, include, pipelinetask]
level: practitioner
status: docs-checked
description: "Fan out a Tekton PipelineTask with matrix params to generate combinations and matrix include for explicit combinations."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/matrix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`matrix` fans a PipelineTask out into several TaskRuns (or Runs for custom tasks). The doc marks it as a beta feature, available when `enable-api-fields` is `"beta"`.

`matrix.params` generates the cross product of its value lists:

```yaml
matrix:
  params:
    - name: platform
      value: [linux, mac]
    - name: browser
      value: [safari, chrome]
```

This yields four combinations: linux/safari, linux/chrome, mac/safari, mac/chrome.

`matrix.include` adds explicit combinations, each optionally named, with its own params (for example a combination `linux-url` with `platform: linux` and `url: some-url`). The `name` in an include entry also becomes the display name of the resulting TaskRun; precedence for the displayed name is `matrix.include[].name` over `tasks[].displayName`.

A PipelineTask may specify both `params` and `matrix`. Matrix works in `tasks`, `finally` tasks and custom tasks.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): matrix.md. Removed: nothing.

Method: documentation only; no commands were run.
