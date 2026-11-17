---
id: computing-software.cloud-infrastructure-engineering.kubernetes.applicationset-generators-for-fleets
name: applicationset-generators-for-fleets
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argo-cd, argocd, applicationset, list-generator, cluster-generator, git-generator, matrix-generator, scm-provider-generator, pull-request-generator, multi-cluster, multi-tenant, fleet-management, gitops, templating]
level: practitioner
status: docs-checked
description: "Fan an Argo CD ApplicationSet across clusters, tenants, or PRs: list/cluster/git/matrix/SCM generators, template field precedence, and the ApplicationSet controller's own blast radius."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/GoTemplate/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Template/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Controlling-Resource-Modification/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Application-Deletion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ApplicationSet generators — one object producing many Applications

**Goal:** stop hand-writing one `Application` manifest per cluster/tenant/service.
An `ApplicationSet` takes a generator (the source of "what to fan out over") and a
`template` (the `Application` shape to stamp per generated item), and the controller
reconciles the resulting set of `Application` objects — adding/removing them as the
generator's output changes.

## 1. The generators, by what they enumerate
- **List**: a literal inline list of `{cluster, url, ...}` key-value sets — the
  simplest, good for a small fixed fleet or bootstrapping before anything dynamic
  exists.
- **Cluster**: enumerates every cluster registered with Argo CD (via Secrets labeled
  `argocd.argoproj.io/secret-type: cluster`) — the standard way to fan an app out to
  "every cluster we manage," filterable by label selector so you can target a subset
  (`selector: {matchLabels: {env: prod}}`).
- **Git (directories)**: one `Application` per matching directory
  (`directories: [{path: "clusters/*/apps/*"}]`) — this is what makes the directory
  layout in `gitops-repo-structure-patterns` *become* a set of Applications
  automatically; add a directory, get an app, no manifest to hand-write.
- **Git (files)**: one `Application` per matching JSON/YAML file — used when
  per-app config (not just directory presence) should drive templating, e.g. a
  `config.yaml` per app declaring which clusters it targets.
- **SCM Provider / Pull Request**: enumerates repos (SCM Provider) or open PRs (Pull
  Request generator) across a GitHub/GitLab org — used for preview-environment
  patterns (one ephemeral Application per open PR, torn down on merge/close) or for
  "deploy this same chart into every repo matching a topic" fleet patterns.
- **Matrix / Merge**: combines two generators — the common real-world need is
  `Matrix: [Cluster generator, Git directory generator]` to produce the cross
  product "every app directory × every cluster it should run in," usually narrowed
  with each generator's own selector so the cross product isn't literally every app
  on every cluster.

## 2. Templating and field precedence
```yaml
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - matrix:
        generators:
          - clusters: {selector: {matchLabels: {env: prod}}}
          - git: {repoURL: https://example.com/acme/fleet.git, directories: [{path: "apps/*"}]}
  template:
    metadata: {name: "{{.name}}-{{.path.basename}}"}
    spec:
      destination: {server: "{{.server}}"}
      source: {repoURL: https://example.com/acme/fleet.git, path: "{{.path.path}}"}
  templatePatch: |
    spec:
      source:
        helm:
          valueFiles: ['{{ if eq .metadata.labels.env "prod" }}values-prod.yaml{{ else }}values-dev.yaml{{ end }}']
```
- Generator output fields (`.name`, `.server`, `.path.path`, `.path.basename`, the
  cluster Secret's `.metadata.labels.<key>` and `.metadata.annotations`, plus
  anything from the generator's `values` map) are the variables available in
  `{{ }}`. The example above uses Go templates (`goTemplate: true`); the default
  engine is fasttemplate, whose syntax differs (`{{name}}`, no leading dot).
  The docs recommend `goTemplateOptions: ["missingkey=error"]` so an undefined
  key fails instead of rendering as an empty or placeholder value.
- `templatePatch` only works when `goTemplate: true`. It applies a templated patch
  over the base `template` (Sprig functions are available, except `env`,
  `expandenv` and `getHostByName`). The docs warn it can apply arbitrary changes,
  so use it only with trusted parameters.
- The Cluster generator's `values:` field (a map of string key-values) is exposed
  as `{{.values.<key>}}`, which is how "every cluster gets the same app but with a
  cluster-specific parameter" works without one directory per cluster. The cluster
  Secret's labels and annotations are available as `.metadata.labels.<key>` and
  `.metadata.annotations`.

## 3. ApplicationSet's own blast radius
- The `ApplicationSet` controller's default policy is `sync` (create, update and
  delete are all allowed), so a bug or typo in a generator (e.g. a directory glob
  that's too broad) can delete Applications, not just fail to create them. Restrict
  it with the controller `--policy` flag (`create-only`, `create-update`,
  `create-delete`) or per ApplicationSet with `spec.syncPolicy.applicationsSync`
  (the flag takes precedence unless the per-ApplicationSet override is enabled with
  `ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_POLICY_OVERRIDE`).
- `spec.syncPolicy.preserveResourcesOnDeletion: true` on the ApplicationSet stops
  the `resources-finalizer.argocd.argoproj.io` finalizer being added to generated
  Applications, so deleting an Application does not delete its Kubernetes
  resources. It is separate from the Application-level `automated.prune` sync
  option (off by default); conflating the two leaks orphaned resources or deletes
  more than intended.
- A broad `git` directory generator combined with `selfHeal` fleet-wide means a bad
  commit to the fleet repo can simultaneously misconfigure every cluster it
  enumerates — treat the generator source repo/path with at least the review rigor
  of the prod environment it can reach.

## Gotchas
- `list` generator entries are static — they don't notice a cluster going away;
  prefer `cluster` generator with label selectors for anything that should track
  cluster inventory automatically.
- Matrix generators compose multiplicatively (two generators each returning 20
  items produce 400 Applications); narrow with selectors before combining, not
  after. Matrix and Merge generators can be nested only once.
- `goTemplate: true` is opt-in and changes the templating syntax (for example
  `{{.path.basename}}` instead of `{{path.basename}}`) from the default fasttemplate
  engine; `{{ if }}` and `templatePatch` only work with Go templates. Confirm which
  mode is set.

## Verify
- [ ] `kubectl get applicationset <name> -o yaml` status shows the expected
      generated-Application count — no missing or duplicated cluster/app pairs.
- [ ] A new directory/cluster/PR appears as a new Application within one
      reconcile interval, without manual intervention.
- [ ] Removing a directory/cluster from the generator's source prunes the
      corresponding Application (and verify whether the underlying resources were
      also deleted, per `preserveResourcesOnDeletion`).
- [ ] A deliberately malformed generator entry fails visibly (logged/status
      condition) when `missingkey=error` is set, rather than rendering a broken value
      into a live Application.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/operator-manual/applicationset, latest release v3.5.6, repo commit 2026-10-25).
Confirmed: Go template mode needs `goTemplate: true` and `missingkey=error` is the recommended option; `templatePatch` requires Go templates and carries a trusted-input warning; cluster generator `values` map becomes `.values.<key>` and Secret labels/annotations are exposed under `.metadata`; `--policy` values (`sync` default, `create-only`, `create-update`, `create-delete`) and `applicationsSync`; `preserveResourcesOnDeletion` lives under the ApplicationSet `syncPolicy` and controls the resources finalizer; matrix/merge nest once; git directory generator `path.basename`.
Removed or corrected: the claim that values come from Secret `values.<key>` annotations, the unquoted `{{.repoURL}}` variable that no generator provides, YAML with unescaped inner quotes, and the fasttemplate silent-typo claim.

Method: documentation only; no commands were run.
