---
id: computing-software.cloud-infrastructure-engineering.kubernetes.flux-image-automation-and-multi-tenancy
name: flux-image-automation-and-multi-tenancy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, flux, fluxcd, image-automation, image-reflector-controller, image-automation-controller, imagerepository, imagepolicy, imageupdateautomation, git-push-back, multi-tenancy, tenant-rbac, flux-tenants, gitops]
level: practitioner
status: docs-checked
description: "Automate image tag bumps in a Flux GitOps repo with image-reflector/automation controllers, and isolate multi-tenant Flux fleets with per-tenant RBAC and source restrictions."
sources: ["https://fluxcd.io/flux/guides/image-update/", "https://fluxcd.io/flux/installation/configuration/multitenancy/", "https://github.com/fluxcd/image-reflector-controller/blob/main/docs/spec/v1/imagepolicies.md", "https://github.com/fluxcd/image-reflector-controller/blob/main/docs/spec/v1/imagerepositories.md", "https://github.com/fluxcd/image-automation-controller/blob/main/docs/spec/v1/imageupdateautomations.md", "https://github.com/fluxcd/flux2/blob/main/cmd/flux/bootstrap_github.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flux image automation and multi-tenancy — CI-less deploys and tenant isolation

Two separate, commonly paired capabilities: automatically updating image tags in git
without a CI pipeline writing to it, and running many teams' workloads through one
Flux fleet without them reconciling each other's resources.

## 1. Image automation — three CRDs, one write-back loop
```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImageRepository
metadata: {name: app}
spec: {image: ghcr.io/org/app, interval: 5m}
---
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImagePolicy
metadata: {name: app}
spec:
  imageRepositoryRef: {name: app}
  policy: {semver: {range: ">=1.0.0 <2.0.0"}}
---
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImageUpdateAutomation
metadata: {name: app}
spec:
  interval: 5m
  sourceRef: {kind: GitRepository, name: apps}
  git:
    checkout: {ref: {branch: main}}
    commit: {author: {email: flux@example.com, name: fluxcdbot}}
    push: {branch: main}
  update: {path: ./apps/app, strategy: Setters}
```
- `image-reflector-controller` scans the registry (`ImageRepository`) and evaluates
  `ImagePolicy` (a `semver`, `alphabetical` or `numerical` policy, optionally narrowed first with
  `spec.filterTags.pattern`, a regular expression) to pick the latest matching tag — this is
  read-only, nothing changes yet.
- `image-automation-controller` is the write-back half: it finds YAML lines marked
  with a **setter marker comment**:
  ```yaml
  image: ghcr.io/org/app:1.2.3 # {"$imagepolicy": "flux-system:app"}
  ```
  rewrites the value to match the policy, commits, and pushes to the branch in
  `spec.git.push.branch`. Pushing to the branch the source tracks is a direct git push, not a
  gated promotion; see the Gotchas below before wiring this to prod. `Setters` is the only
  supported (and default) `update.strategy`.
- The marker comment is required per field — a `deployment.yaml` or `HelmRelease`
  values block with no `$imagepolicy` marker is never touched, so this is opt-in
  per image reference, not global.

## 2. PR-gated automation instead of direct push
Direct push to `main` is fine for a dev/sandbox env with low blast radius; for
staging/prod most teams redirect `push:` to a dedicated branch
(`push: {branch: flux-image-updates}`) and front it with a bot-opened PR (GitHub
Action watching for pushes to that branch), turning the automation into a proposal a
human merges — the right default once this feeds a protected environment. This is
exactly the seam where "automated" and "promoted" diverge; see
`environment-promotion-in-gitops` for how that merge decision should be gated.

## 3. Multi-tenancy
Flux ships a reference layout (`flux-system` namespace owns the fleet-level
`GitRepository`/root `Kustomization`; each tenant gets its own namespace, its own
`ServiceAccount`, and its own `Kustomization` that `impersonates` that
ServiceAccount):
```yaml
spec:
  serviceAccountName: team-a-reconciler   # Kustomization/HelmRelease runs AS this SA
```
- `spec.serviceAccountName` on a `Kustomization`/`HelmRelease` makes the controller
  apply resources impersonating that tenant's ServiceAccount, so a tenant's RBAC
  (scoped to their namespace via RoleBindings, not ClusterRoleBindings) is what
  actually limits blast radius — the controller's own cluster-wide permissions are
  irrelevant to what a tenant-scoped reconciliation can touch.
- Keep tenants' write access to their own app repositories or paths, never to the fleet
  repository that defines other tenants' RBAC.
- The Flux multi-tenancy lockdown docs add controller flags: `--no-cross-namespace-refs=true`
  (on kustomize-controller, helm-controller, notification-controller and the image controllers)
  and `--default-service-account=<name>` (kustomize-controller and helm-controller), so that
  objects without `spec.serviceAccountName` use that account from their own namespace.
  `flux create tenant` scaffolds a tenant's namespace, service account and RBAC.

## Gotchas
- Direct git push from `ImageUpdateAutomation` means CI status checks and required
  reviews are bypassed unless routed through a PR branch as above — don't let image
  automation become an un-reviewed path into a protected environment.
- A loose `semver` range or an `alphabetical`/`numerical` policy on unfiltered tags can select
  a tag you did not intend — scope ranges and `filterTags` to the tagging scheme your CI
  actually produces.
- Without `spec.serviceAccountName` (or a `--default-service-account` lockdown), a
  `Kustomization` reconciles with the controller's own, broad permissions — a tenant's
  manifest can touch cluster-scoped resources even if that was never intended.
- Private registries need credentials on the `ImageRepository` (`spec.secretRef`, or the image
  pull secrets of `spec.serviceAccountName` for the generic provider); check the object's
  status with `flux get image repository`.

## Verify
- [ ] A new tag matching the `ImagePolicy` range appears via
      `flux get image policy app` before checking whether the commit landed.
- [ ] The automation commit only touches lines with the setter marker — no
      unrelated manifest drift.
- [ ] A tenant's `Kustomization` using `serviceAccountName` cannot apply a resource
      outside its own namespace (test with a deliberately out-of-scope manifest).
- [ ] Prod-bound image updates go through a PR/review step, not a direct push to the
      branch the prod `Kustomization` tracks.

## Checked

2026-10-25, against the image-reflector-controller ImageRepository and ImagePolicy v1 specs, image-automation-controller ImageUpdateAutomation v1 spec, Flux multi-tenancy lockdown docs, and flux2 `bootstrap_github.go` and command list. Confirmed: all three image CRDs are `image.toolkit.fluxcd.io/v1` (the earlier v1beta1/v1beta2 apiVersions were stale), `semver`/`alphabetical`/`numerical` policies and `filterTags`, `Setters` as the only strategy, `sourceRef` and `git.push.branch`, `spec.secretRef`, `serviceAccountName` impersonation, `--no-cross-namespace-refs`, `--default-service-account`, `flux create tenant`, `flux get image` commands. Wrong earlier: `--read-write-key` only makes the bootstrap deploy key read/write, it does not scope tenants. Removed as unconfirmed: the silent-failure claim for missing registry secrets and the 'flux-tenants' remark.

Method: documentation only; no commands were run.
