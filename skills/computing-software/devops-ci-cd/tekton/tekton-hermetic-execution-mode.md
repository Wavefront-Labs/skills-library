---
id: computing-software.devops-ci-cd.tekton.tekton-hermetic-execution-mode
name: tekton-hermetic-execution-mode
category: computing-software
field: devops-ci-cd
product: tekton
tags: [hermetic, network-isolation, annotations, alpha]
level: advanced
status: docs-checked
description: "Run Tekton TaskRun steps without network access using the hermetic execution mode annotation."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/hermetic.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hermetic builds are self-contained: no network access and no fetching dependencies at runtime. In hermetic execution mode every step of the TaskRun runs without network access. It is alpha and experimental, and does not apply to sidecar containers.

Enable it by setting `enable-api-fields` to `"alpha"` in the `feature-flags` ConfigMap, then annotate each TaskRun that should be hermetic:

```yaml
metadata:
  annotations:
    experimental.tekton.dev/execution-mode: hermetic
```

The docs' sample is a step that runs `apt-get update` and `apt-get install -y curl`; it should fail when hermetic mode works.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): hermetic.md. Removed: the reproducible-build advice and the TEP number (not on the page).

Method: documentation only; no commands were run.
