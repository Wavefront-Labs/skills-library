---
id: computing-software.devops-ci-cd.tekton.tekton-stepactions-reference-and-params
name: tekton-stepactions-reference-and-params
category: computing-software
field: devops-ci-cd
product: tekton
tags: [stepaction, steps, reuse, params]
level: practitioner
status: docs-checked
description: "Define a Tekton StepAction as a reusable step, reference it with ref from a Task, pass params and know which fields are forbidden alongside ref."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/stepactions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `StepAction` is the reusable unit of work a `Step` performs (stable feature). It cannot run standalone; steps in a Task either define work inline or `ref` a StepAction. Required: `image`, which must follow the container contract. Optional: `command` or `script` (not both), `args`, `env`, `params`, `results`, `workingDir`, `securityContext`, `volumeMounts`, `description`.

```yaml
steps:
  - name: action-runner
    ref:
      name: step-action
    params:
      - name: step-action-param
        value: $(params.param-for-step-action)
```

A step that references a StepAction may not set `image`, `command`, `args`, `script`, `env` or `volumeMounts`; doing so is a validation error because the StepAction supplies them. Declaring `params` on an inline step is also a validation error, since inline steps take their params from the TaskRun. The Task must ensure the StepAction has all its required params.

Substitution precedence: TaskRun param values in step params, then step-provided values, then defaults that reference other params, then simple defaults, then step result references (resolved last).

## Checked

Checked 2026-11-08 against docs/stepactions.md in tektoncd/pipeline (main), read in full. Confirmed stable status, field list, command versus script exclusivity, params passing, the forbidden fields alongside ref, the inline-step params error and the substitution precedence order. No changes needed to claims.

Method: documentation only; no commands were run.
