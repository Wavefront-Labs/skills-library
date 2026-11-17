---
id: computing-software.devops-ci-cd.tekton.tekton-stepactions-results-and-remote
name: tekton-stepactions-results-and-remote
category: computing-software
field: devops-ci-cd
product: tekton
tags: [stepaction, results, remote-resolution, steps]
level: advanced
status: docs-checked
description: "Emit results from a Tekton StepAction, pass results between steps and resolve StepActions remotely."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/stepactions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A StepAction declares the `results` it emits, and the step that references it can read them. The docs cover three things: emitting results from the StepAction, fetching emitted results from the Task that references it, and passing results between steps. Related fields a StepAction may declare are `workingDir`, `securityContext` and `volumeMounts`.

Step results are written to `$(step.results.<name>.path)` (not `$(results.<name>.path)`). They are not TaskRun results automatically: the Task must fetch them explicitly with a Task result whose `value` is `$(steps.<stepName>.results.<resultName>)`, and later steps can read them with the same variable. Step results can only be referenced in a step's or StepAction's `env`, `command` and `args`. Array and object step results need `enable-api-fields` set to alpha or beta; whole-array `[*]` references cannot be used in `script` and `env`.

A StepAction can also be fetched through a resolver instead of from the cluster, by giving `ref` a `resolver` and `params` (for example the git resolver with `url`, `revision` and `pathInRepo`). Which remote types work depends on the resolvers the cluster operator installed. The default resolver type can be set with `default-resolver-type` in the `config-defaults` ConfigMap (alpha).

When the TaskRun finishes, the step status shows `container`, `imageID`, `name` and `terminated` details, and the resolved `taskSpec` shows the image that the StepAction supplied.

## Checked

Checked 2026-11-08 against docs/stepactions.md in tektoncd/pipeline (main), read in full. Confirmed result emission, the step.results path, explicit fetching into Task results, the type table and reference limits, remote resolution and default-resolver-type. Removed the unsourced claim about hub, bundles and cluster resolvers and the unsourced advice paragraph.

Method: documentation only; no commands were run.
