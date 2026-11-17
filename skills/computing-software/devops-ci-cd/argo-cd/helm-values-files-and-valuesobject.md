---
id: computing-software.devops-ci-cd.argo-cd.helm-values-files-and-valuesobject
name: helm-values-files-and-valuesobject
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, helm-values-files, valuesobject, ignore-missing-value-files, helm-values-precedence]
level: practitioner
status: docs-checked
description: "Feed Helm values to Argo CD apps with valueFiles, values and valuesObject: precedence, paths outside the chart, ignoreMissingValueFiles and per-environment layering."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/helm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm values files and valuesObject

```yaml
spec:
  source:
    repoURL: https://github.com/acme/deploy.git
    targetRevision: main
    path: charts/api
    helm:
      valueFiles:
        - values.yaml
        - ../../envs/common/api.yaml          # outside the chart dir, inside the repo
        - ../../envs/prod/api.yaml
        - ../../envs/prod/api-overrides.yaml
      ignoreMissingValueFiles: true           # skip files that do not exist (optional layers)
      valuesObject:                           # inline map; takes precedence over values and valueFiles
        replicaCount: 6
        podAnnotations: { team: payments }
```

## Precedence (low → high)
chart's default `values.yaml` → `valueFiles` (the last file listed wins) → `values` → `valuesObject` → `parameters`
(documented order: `parameters > valuesObject > values > valueFiles > helm repository values.yaml`; `valuesObject` wins over `values`).

## Rules
- Value file paths are relative to `path` and must stay inside the repository (a path starting with `/` is relative to the repository root; symlinks pointing outside the repo are rejected). Since v2.6, files from a separate repository can be used with multiple sources (`ref`). Remote URLs are passed to Helm as-is and are not glob-expanded.
- `values` is a YAML **string** (block scalar); prefer `valuesObject` (real YAML, diffable, ApplicationSet-templatable).
- A missing file makes Helm error out unless `ignoreMissingValueFiles: true` (CLI `--ignore-missing-value-files`).

## Patterns
- Env layering via ApplicationSet: `- ../../envs/{{.env}}/api.yaml` per generated app.
- `valueFiles` entries may contain glob patterns, expanded in lexical order, so file names can control precedence; build environment variables such as `$ARGOCD_APP_NAME` can be used in paths.

## Verify
- [ ] `argocd app manifests <app>` reflects the highest-precedence value.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: documented precedence (`parameters > valuesObject > values > valueFiles > chart values.yaml`), `ignoreMissingValueFiles`, path boundary rules, glob expansion in `valueFiles`, remote URLs, multi-source value files since v2.6. The old skill ranked `fileParameters` above `parameters` and said valuesObject was the highest source, both unconfirmed or wrong. Removed the remote-value-files server setting claim and the secrets remark.

Method: documentation only; no commands were run.
