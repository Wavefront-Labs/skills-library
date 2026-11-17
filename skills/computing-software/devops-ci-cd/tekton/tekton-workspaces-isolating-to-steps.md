---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-isolating-to-steps
name: tekton-workspaces-isolating-to-steps
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, isolation, credentials, sidecars]
level: advanced
status: docs-checked
description: "Limit a Tekton workspace to specific steps or sidecars with per-step workspaces declarations and custom mount paths, and share workspaces with sidecars."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Isolated Workspaces is a beta feature (`enable-api-fields` set to `"beta"`). It restricts a workspace to chosen steps or sidecars inside one Task, mainly for credentials. It gives no storage isolation between separate PipelineRuns that bind the same PVC.

```yaml
spec:
  workspaces:
  - name: ssh-credentials
  steps:
  - name: clone-repo
    workspaces:
    - name: ssh-credentials   # only this step receives it
    image: git
  - name: build-source
    image: third-party-source-builder:latest  # no access
```

A per-step or per-sidecar `mountPath` can override the workspace default (for example the Task declares `/workspaces/ws`, one step mounts it at `/foo`, a sidecar at `/files`).

Sidecars: by default a Task's sidecars must set the `volumeMount` themselves, using `$(workspaces.<name>.volume)` and `$(workspaces.<name>.path)`. From Pipelines v0.24.0, with the beta gate, sidecars get workspaces automatically; if a sidecar already has a volumeMount at the expected location, that workspace is not bound to it, preserving the older workaround.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
