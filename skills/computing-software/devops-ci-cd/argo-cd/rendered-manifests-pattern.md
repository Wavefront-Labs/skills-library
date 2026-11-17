---
id: computing-software.devops-ci-cd.argo-cd.rendered-manifests-pattern
name: rendered-manifests-pattern
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, rendered-manifests, manifest-hydration, gitops-repo-structure]
level: advanced
status: docs-checked
description: "Apply the rendered manifests (hydration) pattern: CI renders Helm/Kustomize into plain YAML in an env branch or repo, Argo syncs the output, reviewers see real diffs."
sources: ["https://akuity.io/blog/the-rendered-manifests-pattern", "https://argo-cd.readthedocs.io/en/latest/user-guide/source-hydrator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendered manifests pattern (hydration)

Problem: a one-line change to a Helm value or Kustomize base can change dozens of objects across
environments, and the PR diff shows none of it. Rendering at sync time also makes Argo depend on
chart repos and plugins.

## Pattern
1. **Dry source** (what humans edit): `apps/payments/base`, `overlays/prod`, Helm values.
2. CI (or Argo's Source Hydrator) renders each environment:
   Render with your Helm or Kustomize tooling into one directory per app, for example `rendered/prod/payments/`.
3. Commit rendered output to an environment branch (`env/prod`) or a separate repo, one directory per app.
4. Argo Applications point to the rendered path as plain directory sources.

## Argo CD Source Hydrator (beta since v3.5.0 per the latest docs)
```yaml
spec:
  sourceHydrator:
    drySource: { repoURL: https://github.com/org/deploy, targetRevision: main, path: apps/payments/prod }
    syncSource: { targetBranch: env/prod, path: apps/payments/prod }
```
Argo renders and pushes the hydrated manifests itself. It needs the commit server component enabled, `hydrator.enabled: "true"` in the `argocd-cmd-params-cm` ConfigMap, and push credentials. `syncSource.path` must be a non-root directory.

## Benefits and costs
| + | - |
|---|---|
| PRs on env branches show exact object diffs | extra commits/branches to manage |
| Argo syncs plain manifests | CI must have push rights to the env branch |
| Promotion = merge rendered diff | secrets must stay out (use ESO/SOPS refs, not values) |

## Gotchas
- Render deterministically (pin chart and kustomize versions).
- Protect env branches; only the renderer may push.

## Verify
- [ ] A values change PR produces a rendered diff PR listing every changed object.

## Checked

2026-10-28. Confirmed against the Argo CD Source Hydrator page (latest docs): drySource, syncSource.targetBranch, hydrator.enabled in argocd-cmd-params-cm, commit server, non-root syncSource.path, push credentials; and the Akuity rendered manifests article (push credentials managed in CI). Corrected: hydrator maturity (beta since v3.5.0, not alpha 3.1+). Removed: render commands with flags, the helm.sh/chart timestamp note and the faster-syncs claim (not in the sources).

Method: documentation only; no commands were run.
