---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-volume-sources
name: tekton-workspaces-volume-sources
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, volumeclaimtemplate, pvc, volumesource]
level: practitioner
status: docs-checked
description: "Choose a Tekton workspace volume source: volumeClaimTemplate for isolated per-run storage versus an existing persistentVolumeClaim, plus emptyDir, configMap and secret."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only one volume source type is allowed per workspace entry.

`volumeClaimTemplate` creates a PVC for each PipelineRun or TaskRun and deletes it when that run is deleted. Use it for writeable workspaces that must be isolated per run, especially when runs are triggered by inputs at different trust levels.

```yaml
workspaces:
  - name: myworkspace
    volumeClaimTemplate:
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
```

`persistentVolumeClaim` references an existing PVC, optionally exposing only a `subPath`:

```yaml
workspaces:
  - name: myworkspace
    persistentVolumeClaim:
      claimName: mypvc
    subPath: my-subdir
```

Caution from the docs: binding an existing PVC can share data across PipelineRuns, so do not use the same PVC for pipelines at different trust levels unless sharing is intentional and safe for every workload that can mount the claim. Other sources documented are `emptyDir`, `configMap`, `secret`, `projected` and `csi`.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
