---
id: computing-software.devops-ci-cd.argo-cd.applicationset-post-selectors-and-requeue
name: applicationset-post-selectors-and-requeue
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, post-selector, generator-selector, generator-requeue-after, applicationset-selector]
level: advanced
status: docs-checked
description: "Filter ApplicationSet generator output with post-selectors on generated params, and tune polling with requeueAfterSeconds for SCM and pull request generators."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Post-Selector/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Pull-Request/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Controlling-Resource-Modification/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generator post-selectors and requeue

## 1. Post-selector
Any generator can have a `selector` that filters the **generated parameter sets** after generation:
```yaml
spec:
  goTemplate: true
  generators:
    - list:
        elements:
          - { cluster: dev-eu,  env: dev,  tier: "2" }
          - { cluster: prod-eu, env: prod, tier: "1" }
          - { cluster: prod-us, env: prod, tier: "1" }
      selector:
        matchLabels: { env: prod }
        matchExpressions:
          - { key: cluster, operator: In, values: [prod-eu] }    # staged rollout: only prod-eu for now
```
The selector uses the Kubernetes label-selector format (`matchLabels`, `matchExpressions` with operators `In`, `NotIn`, `Exists`, `DoesNotExist`; `values` must be non-empty for `In`/`NotIn`) on the generated values.
The cluster generator also has its own label `selector` that narrows which clusters are targeted.

## 2. Requeue / polling
- The pull request generator polls the SCM API every `requeueAfterSeconds` (default 1800, i.e. 30 minutes).
```yaml
    - pullRequest:
        github: { owner: acme, repo: web, tokenRef: { secretName: gh-token, key: token }, labels: [preview] }
        requeueAfterSeconds: 120
```
  To remove the polling delay, configure the ApplicationSet webhook server (payload URL uses the `/api/webhook` endpoint of the ApplicationSet instance).
- The Git generator polls every `requeueAfterSeconds` (default 3 minutes); the same webhook server can trigger it sooner.

## Gotchas
- Applications that are no longer generated (for example after tightening a selector) are removed under the default `sync` policy; `applicationsSync: create-only` stops the controller modifying or deleting Applications (it does not protect against deletion of the ApplicationSet itself; `preserveResourcesOnDeletion` is a separate setting). Preview changes with `argocd appset create --dry-run ./appset.yaml -o json`, which fills `.status.resources` with the Applications that would be managed.

## Verify
- [ ] `argocd appset create --dry-run ./appset.yaml -o json` lists only the selected clusters' Applications.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: post-selector format and operators, `requeueAfterSeconds` default 1800 for pull request and 3 minutes for Git generators, `/api/webhook` endpoint, `applicationsSync: create-only` and `preserveResourcesOnDeletion` semantics, `argocd appset create --dry-run`. Removed unconfirmed claims (flattened Git-file keys, matrix/merge placement, string comparison, SCM-provider requeue default, cluster-secret immediacy, rate-limit remark, label-selector verify command).

Method: documentation only; no commands were run.
