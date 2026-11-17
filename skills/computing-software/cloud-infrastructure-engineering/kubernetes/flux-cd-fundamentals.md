---
id: computing-software.cloud-infrastructure-engineering.kubernetes.flux-cd-fundamentals
name: flux-cd-fundamentals
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, flux, fluxcd, flux2, gitops, source-controller, kustomize-controller, helm-controller, gitrepository, ocirepository, kustomization-cr, helmrelease, dependson, reconciliation, argo-cd-comparison, flux-bootstrap]
level: practitioner
status: docs-checked
description: "Run GitOps delivery with Flux CD v2: source-controller, Kustomization/HelmRelease reconciliation, dependsOn ordering, pruning, and the Argo CD differences that matter."
sources: ["https://fluxcd.io/flux/concepts/", "https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md", "https://github.com/fluxcd/helm-controller/blob/main/docs/spec/v2/helmreleases.md", "https://github.com/fluxcd/source-controller/blob/main/docs/spec/v1/README.md", "https://github.com/fluxcd/flux2/blob/main/cmd/flux/bootstrap_github.go", "https://argo-cd.readthedocs.io/en/stable/user-guide/helm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flux CD fundamentals — the controller-native alternative to Argo CD

**Goal:** understand Flux v2's split-controller model well enough to debug why
something isn't reconciling, order dependent apps correctly, and know when Flux is
the better fit than Argo CD (no UI requirement, GitHub-native, pure-CRD pipeline).

## 1. Architecture — separate controllers, not one app
Flux v2 is several independent controllers (install via `flux bootstrap github
--owner=<org> --repository=<repo> --path=clusters/prod --personal`), each owning one
CRD group:
- **source-controller** — `GitRepository`, `OCIRepository`, `HelmRepository`,
  `Bucket`: pulls and verifies the artifact, exposes it as an internal tarball URL
  other controllers consume. Nothing deploys anything at this layer.
- **kustomize-controller** — `Kustomization` (Flux's own CRD, not the `kustomize.config.k8s.io`
  kind): points at a path inside a `GitRepository`/`OCIRepository` source, runs
  `kustomize build` on it, applies the result, prunes removed resources.
- **helm-controller** — `HelmRelease`: points at a `HelmRepository`/`OCIRepository`
  chart source plus inline `values:`, runs the Helm install/upgrade lifecycle
  (so Helm hooks **do** fire here, unlike the Kustomize `helmCharts:` inflator).
- **notification-controller** and the **image-reflector** and **image-automation** controllers
  are further separate controllers (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.flux-image-automation-and-multi-tenancy`).

## 2. Reconciliation loop
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: {name: apps, namespace: flux-system}
spec:
  interval: 1m
  url: https://github.com/org/gitops-repo
  ref: {branch: main}
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: {name: apps, namespace: flux-system}
spec:
  interval: 10m
  sourceRef: {kind: GitRepository, name: apps}
  path: ./clusters/prod/apps
  prune: true
  wait: true
  timeout: 3m
  dependsOn: [{name: infra}]
```
- `interval` on the source and `interval` on the `Kustomization` are independent: the source
  interval sets how often the source is fetched; the `Kustomization` interval (minimum 60
  seconds) sets how often it is rebuilt and applied, correcting drift. A changed `.spec` or a new
  source revision is handled immediately, outside the interval window.
  `flux reconcile kustomization apps --with-source` reconciles the source first and then the
  `Kustomization`: the usual "why hasn't my change applied" debugging move.
- `prune` is a required field: with `true`, objects that were applied earlier but are missing
  from the current source revision are garbage-collected; without it, deleting a manifest from
  git leaves the live resource in place.
- `wait: true` health-checks **all** reconciled resources; when it is set, `healthChecks` is
  ignored. Use `healthChecks` (without `wait`) to check only named resources. A `dependsOn`
  target must have `Ready=True` (its last applied status condition) before the dependent
  `Kustomization` is applied.

## 3. `dependsOn` ordering
`dependsOn` refers to other `Kustomization` (or `HelmRelease`) objects, not to individual
resources. Model dependencies as **separate `Kustomization` objects** (e.g. `infra` before
`apps`), for example CRDs and their controller in one and the custom resources in the next.

## 4. Flux vs Argo CD
- Flux is "many small CRDs reconciling independently" (sources, `Kustomization`, `HelmRelease`);
  Argo CD uses one `Application` object per deployable unit. Choose on your own requirements
  (UI, multi-tenancy, how teams compose delivery), not on a rule of thumb.
- `HelmRelease` is run by helm-controller with its own install, upgrade, test and rollback
  settings. Argo CD's user guide says Helm is only used to inflate charts with `helm template`,
  so the lifecycle differs (see `kustomize-helm-postrender-and-chart-inflator` for the Kustomize
  side).
- Progressive delivery: the Flux project offers a separate controller, Flagger, for it.

## Gotchas
- `GitRepository` with `ref: {branch: main}` polls; a webhook (notification-controller
  receiver) makes reconciliation near-instant instead of waiting for `interval`.
- Pruning removes objects that the `Kustomization` applied earlier and that disappeared from the
  source revision, so scope `path` tightly and avoid two `Kustomization` objects managing the
  same objects.
- `HelmRelease.spec.values` is YAML embedded in the CR — large values blocks make the
  CR itself hard to review; prefer `valuesFrom:` referencing a ConfigMap/Secret kept
  as its own file in git.
- Suspending (`flux suspend kustomization <name>`) stops applying new source revisions and
  pauses drift detection and correction; it does not undo manual changes.

## Verify
- [ ] `flux get kustomizations -A` shows all `Ready=True`, and `flux get sources git`
      shows the expected revision matches the latest commit on the target branch.
- [ ] Deleting a manifest from the git path and reconciling removes the live resource
      (`prune` is actually working, not just configured).
- [ ] `dependsOn` is honored under failure: breaking `infra`'s health check blocks
      `apps` from reconciling, observable via `flux get kustomizations apps`.
- [ ] A webhook-triggered reconcile reflects a new commit within seconds, not the
      full polling `interval`.

## Checked

2026-10-25, against the kustomize-controller Kustomization v1 spec, helm-controller HelmRelease v2 spec, source-controller v1 spec index, Flux concepts page, flux2 `bootstrap_github.go` and `reconcile_kustomization.go`, and the Argo CD Helm user guide. Confirmed: bootstrap flags, Kustomization `sourceRef` kinds, `prune` semantics, `dependsOn` readiness rule, `suspend` behaviour, `valuesFrom`, Flagger. Wrong in the earlier text: `wait: true` makes `healthChecks` ignored (not combined); a new source revision is handled immediately, not only at the Kustomization interval; Argo CD only uses `helm template`. Removed as unconfirmed: Weave GitOps, the 'no UI' and 'no sync-wave equivalent' claims, prune ownership of manual applies.

Method: documentation only; no commands were run.
