---
id: computing-software.devops-ci-cd.argo-cd.multiple-sources-and-ref-sources
name: multiple-sources-and-ref-sources
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, multi-source-application, ref-sources, external-helm-values, sources-field]
level: advanced
status: docs-checked
description: "Combine an external Helm chart with values files from your own Git repo using Argo CD multi-source Applications and ref sources, plus their limits."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple sources and `ref` sources

**Use case:** deploy the upstream `ingress-nginx` chart, but keep values in your Git repo.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: ingress-nginx-prod, namespace: argocd }
spec:
  project: platform
  sources:                                     # plural; replaces `source`
    - repoURL: https://kubernetes.github.io/ingress-nginx
      chart: ingress-nginx
      targetRevision: 4.11.3
      helm:
        valueFiles:
          - $values/platform/ingress-nginx/values-common.yaml
          - $values/platform/ingress-nginx/values-prod.yaml
    - repoURL: https://github.com/acme/platform-config.git
      targetRevision: main
      ref: values                              # referenced as $values
  destination: { name: prod-eu, namespace: ingress-nginx }
```

## Rules
- Argo CD generates manifests for each source separately and combines them; when `sources` is set, `source` is ignored.
- `ref: values` maps to `$values`, which resolves to the root of that source; it can only be used at the beginning of a value file path.
- A `ref` source with no `path` is used only as a source of value files; with `path` set, Argo CD also generates resources from it.
- Sources with `ref` cannot include `chart`; another Helm chart cannot be a source for value files.
- If several sources produce the same resource (group, kind, name, namespace) the last one wins and Argo CD raises a `RepeatedResourceWarning`.
- The docs warn against more than 2-3 entries in `sources`; use ApplicationSets or app-of-apps to group applications.

## Verify
- [ ] The rendered manifests reflect the values from the prod values file.

## Checked
2026-10-28. Confirmed on the Argo CD multiple sources page: `sources` replaces `source`; `ref` and the `$values` variable (start of path only, relative to the referenced source root); ref source without `path` only supplies files; ref sources cannot include `chart`; duplicate resources: last source wins with RepeatedResourceWarning; the 2-3 sources warning.
Fixed: duplicate resources are a warning, not an error (the old text said "error/warning ... in older versions").
Removed (not confirmed): the rollback and UI/CLI limits, `argocd app manifests --source-positions/--source-names`, the umbrella chart and Kustomize `helmCharts` alternatives, the `releaseName` line.

Method: documentation only; no commands were run.
