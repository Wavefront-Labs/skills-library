---
id: computing-software.devops-ci-cd.tekton.tekton-pipelinerun-taskrunspecs
name: tekton-pipelinerun-taskrunspecs
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipelinerun, taskrunspecs, podtemplate, serviceaccount]
level: advanced
status: docs-checked
description: "Override service account, pod template, timeout and metadata for individual PipelineTasks with taskRunSpecs in a Tekton PipelineRun."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelineruns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`taskRunSpecs` entries target a PipelineTask by `pipelineTaskName` and override pipeline-wide settings:

```yaml
spec:
  podTemplate:
    securityContext:
      runAsUser: 1000
      runAsGroup: 2000
      fsGroup: 3000
  taskRunSpecs:
    - pipelineTaskName: build-task
      serviceAccountName: sa-for-build
      podTemplate:
        nodeSelector:
          disktype: ssd
      timeout: "1h30m"
```

Here `build-task` gets the `nodeSelector` of its own template combined with the `securityContext` from the PipelineRun-level template, and a 1h30m timeout. In v1beta1 the field names are `taskServiceAccountName` and `taskPodTemplate`.

`metadata.annotations` and `metadata.labels` can be added per task, for example Vault agent injection annotations. Precedence when a key appears at several levels: `PipelineRun.spec.taskRunSpec.metadata` over `PipelineRun.metadata` over the Pipeline task metadata.

`podTemplate` fields support parameter substitution, including matrix params, such as `kubernetes.io/arch: $(params.arch)` in a `nodeSelector` or tolerations with `$(params.env)`. Entries may also carry `stepSpecs` and `sidecarSpecs`.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelineruns.md. Removed: nothing.

Method: documentation only; no commands were run.
