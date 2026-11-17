---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-isolation-trust-boundaries
name: tekton-workspaces-isolation-trust-boundaries
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, security, trust-boundaries, rwx]
level: advanced
status: docs-checked
description: "Avoid cross-run data leakage in Tekton by not sharing persistent workspaces across PipelineRuns at different trust levels."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tekton does not enforce filesystem isolation between PipelineRuns that deliberately bind the same persistent workspace. When two runs mount the same PVC, their pods can access the same files subject to the PVC access mode, Kubernetes volume permissions and container security context.

Guidance from the docs:
- Use `volumeClaimTemplate` when a PipelineRun needs a writeable persistent workspace isolated from other runs.
- Do not bind the same existing PVC to pipelines at different trust levels, for example untrusted pull-request validation and trusted release automation.
- `ReadWriteMany` PVCs are shared Kubernetes filesystems that many pods can mount at once; Tekton adds no boundary on top.
- Isolated workspaces limit which steps in one Task see data but do not protect between runs.

See the Tekton Security Best Practices page for the full guidance.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
