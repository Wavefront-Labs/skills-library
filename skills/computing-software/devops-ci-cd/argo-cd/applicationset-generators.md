---
id: computing-software.devops-ci-cd.argo-cd.applicationset-generators
name: applicationset-generators
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, applicationset, generators, list-generator, git-generator, git-directory-generator, git-file-generator, cluster-generator, matrix-generator, merge-generator, pull-request-generator, scm-provider-generator, cluster-decision-resource, plugin-generator, go-template, template-patch, applicationset-policy, preserve-resources-on-deletion, progressive-syncs, rolling-sync, applicationset-controller, gitops, kubernetes]
level: advanced
status: docs-checked
description: "Generate Argo CD Applications at scale with ApplicationSet: list/git/cluster/matrix/merge/pull-request/SCM generators, Go templates and templatePatch, deletion policies and progressive syncs."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Progressive-Syncs/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Controlling-Resource-Modification/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Template/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Matrix/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ApplicationSet generators

**Goal:** one CRD that stamps out an Application per (service × cluster × environment)
from Git structure or cluster inventory, so adding a cluster or a directory needs no YAML
copy-paste.

## 1. Shape
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: { name: services, namespace: argocd }
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]      # fail loudly on a missing parameter
  generators: [ … ]
  template:
    metadata:
      name: '{{.path.basename}}-{{.name}}'      # must be unique and DNS-safe
      labels: { team: '{{index .path.segments 1}}' }
    spec:
      project: default
      source: { repoURL: https://git.example.com/k8s/apps.git, targetRevision: main, path: '{{.path.path}}' }
      destination: { server: '{{.server}}', namespace: '{{.path.basename}}' }
      syncPolicy: { automated: { prune: true, selfHeal: true }, syncOptions: [CreateNamespace=true] }
  templatePatch: |                               # optional: per-element patch rendered as YAML (needs goTemplate; spec.project is not supported here)
    {{- if .autoSync }}
    spec: { syncPolicy: { automated: { prune: true } } }
    {{- end }}
  syncPolicy:
    preserveResourcesOnDeletion: true            # deleting the AppSet keeps the deployed resources
    applicationsSync: create-update              # create-only | create-update | create-delete | sync (default)
```
Prefer `goTemplate: true`: fasttemplate is the default but is documented as to be deprecated in favour of Go templates.

## 2. Generators
| generator | yields | typical use |
|---|---|---|
| `list` | static elements (`- {cluster: eu, url: https://…}`) | few hand-maintained targets |
| `git.directories` | one element per matching directory (`path: apps/*`, `exclude: true` entries) with `path.path`, `path.basename`, `path.segments` | app-per-folder monorepo |
| `git.files` | one element per matching file (`path: clusters/**/config.json`), file contents flattened as params | per-cluster/per-env config files |
| `clusters` | every cluster registered in Argo CD (`name`, `server`, `metadata.labels.*`), filtered by `selector` on cluster-secret labels | fan-out to all prod clusters |
| `pullRequest` | one per open PR (`number`, `branch`, `branch_slug`, `head_sha`, `labels`) from GitHub/GitLab/Gitea/Bitbucket/Azure | preview environments |
| `scmProvider` | one per repository in an org (`repository`, `url`, `branch`, `sha`), filters on name/path existence/labels | app-per-repo |
| `matrix` | cartesian product of two generators (a matrix or merge can only be nested once) | services × clusters |
| `merge` | join of generators on `mergeKeys` (base + overrides) | defaults per cluster with per-app exceptions |
| `clusterDecisionResource` | from a placement CRD (OCM `Placement`) | multi-cluster schedulers |
| `plugin` | HTTP plugin returning JSON params | anything else (CMDB, Backstage) |

Git generators poll (`requeueAfterSeconds`, default 180 s, i.e. 3 minutes) and can also react to the ApplicationSet
webhook server (`/api/webhook` endpoint of the ApplicationSet instance; the shared secret is optional) so new
directories appear sooner. `pullRequest`/`scmProvider` take a token
(`tokenRef: {secretName, key}`); without one requests are anonymous. The `pullRequest` generator polls every `requeueAfterSeconds` (default 1800).

Matrix example — every app directory to every cluster labelled `env=prod`:
```yaml
generators:
  - matrix:
      generators:
        - git: { repoURL: …, revision: main, directories: [{ path: apps/* }] }
        - clusters: { selector: { matchLabels: { env: prod } } }
```
Element keys from the second generator can reference the first (`{{.path.basename}}` in
a nested `git.files` path) — the "parameterised child generator" pattern.

## 3. Preview environments with pullRequest
```yaml
generators:
  - pullRequest:
      github: { owner: example, repo: web, tokenRef: { secretName: github-token, key: token }, labels: [preview] }
      requeueAfterSeconds: 60
template:
  metadata: { name: 'web-pr-{{.number}}' }
  spec:
    source: { repoURL: https://github.com/example/web.git, targetRevision: '{{.head_sha}}', path: deploy
              helm: { parameters: [{ name: image.tag, value: 'pr-{{.number}}-{{.head_short_sha}}' }] } }
    destination: { server: https://kubernetes.default.svc, namespace: 'preview-{{.branch_slug}}' }
    syncPolicy: { automated: { prune: true }, syncOptions: [CreateNamespace=true] }
```
Closing the PR removes the element → Application deleted → resources pruned (requires the
Application finalizer, which the AppSet adds by default, and `applicationsSync` not
`create-only`). CI must push the image tag before the sync, or add `PreSync` waits.

## 4. Deletion and protection
- Deleting an ApplicationSet cascades to its Applications and their resources unless
  `preserveResourcesOnDeletion: true`. Set it on production AppSets; cleanup is then manual.
- `applicationsSync: create-update` keeps Apps when generator elements disappear (safer
  during generator mistakes — a broken `git.files` glob returning nothing would otherwise
  delete every app). `create-only` ignores template changes after creation.
- Controller-wide: `--policy` flag / `applicationsetcontroller.policy` in
  `argocd-cmd-params-cm`; when set it takes precedence over `applicationsSync`, unless `applicationsetcontroller.enable.policy.override` (`--enable-policy-override`, default false) is enabled.
- `ignoreApplicationDifferences` lets you list Application fields that the AppSet should not revert
  (e.g. `spec.source.targetRevision`); it has limitations for fields inside lists.

## 5. Progressive syncs (rolling out across clusters)
Beta feature since v3.3.0, off by default (`applicationsetcontroller.enable.progressive.syncs: "true"` in `argocd-cmd-params-cm`, or `--enable-progressive-syncs`):
```yaml
strategy:
  type: RollingSync
  rollingSync:
    steps:
      - matchExpressions: [{ key: env, operator: In, values: [dev] }]
      - matchExpressions: [{ key: env, operator: In, values: [staging] }]
      - matchExpressions: [{ key: env, operator: In, values: [prod] }]
        maxUpdate: 25%
```
Applications must carry the labels in `template.metadata.labels`. RollingSync forces autosync off on the
generated Apps; `maxUpdate` (default 100%) caps simultaneous updates per step, and Applications matched by no step are not synced automatically.

## 6. Debugging
`kubectl -n argocd get appset services -o yaml` → `status.conditions`; logs:
`kubectl -n argocd logs deploy/argocd-applicationset-controller`. Dry-run rendering:
`argocd appset generate appset.yaml` prints the Applications it would create — run
it in CI on every change to the AppSet.

## Verify
- [ ] `argocd appset generate` output in CI shows the expected Application names and no missing keys.
- [ ] Adding a directory/cluster produces an Application within the requeue/webhook interval.
- [ ] Removing an element behaves per `applicationsSync` (deleted vs kept) as intended.
- [ ] Production AppSets have `preserveResourcesOnDeletion: true`.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: generator parameter names (`path.basename`, `path.segments`, PR `number`/`branch_slug`/`head_sha`/`head_short_sha`, cluster `metadata.labels.<key>`), `requeueAfterSeconds` defaults (180 s Git, 1800 s pull request), webhook endpoint, matrix/merge nesting limit, `templatePatch` constraints, `applicationsSync` values, `--policy` and policy-override setting (default false), progressive sync status (Beta since v3.3.0), flag and key, `maxUpdate` default, `ignoreApplicationDifferences`, `argocd appset generate`. Removed unconfirmed claims (version gates 2.8+/2.9+, status condition names, rate-limit advice). The skill called progressive syncs alpha, which was stale.

Method: documentation only; no commands were run.
