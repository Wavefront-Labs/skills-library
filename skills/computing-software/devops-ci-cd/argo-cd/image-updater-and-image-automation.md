---
id: computing-software.devops-ci-cd.argo-cd.image-updater-and-image-automation
name: image-updater-and-image-automation
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argocd-image-updater, image-updater, image-automation, flux-image-automation, imagerepository, imagepolicy, imageupdateautomation, image-list, update-strategy, semver-strategy, newest-build, digest-strategy, alphabetical, write-back-git, write-back-argocd, helm-image-tag, kustomize-image, registries-conf, registry-credentials, ecr-credentials, image-pull-secret, ci-pushes-tag, deploy-on-push, gitops-promotion, kubernetes]
level: advanced
status: gated
description: "Deploy new images without a CI commit: Argo CD Image Updater (semver, newest-build, digest; git write-back), Flux image automation CRDs, and when CI-written tags win."
sources: ["https://argocd-image-updater.readthedocs.io/en/stable/", "https://argocd-image-updater.readthedocs.io/en/stable/basics/update-strategies/", "https://argocd-image-updater.readthedocs.io/en/stable/basics/update-methods/", "https://fluxcd.io/flux/guides/image-update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image Updater and image automation

**Goal:** a new image tag in the registry becomes a Git commit (and a sync) with no
pipeline step that holds Git write credentials — or you decide, knowingly, to keep tag
bumps in CI.

## 1. Decide first: CI writes the tag, or a watcher does?
| approach | pros | cons |
|---|---|---|
| **CI commits the tag** (`yq -i '.image.tag = env(TAG)' values.yaml && git push`, or `kustomize edit set image`) | explicit, auditable, works with any registry, promotion is a PR | CI needs Git write creds; race on busy repos (retry on push reject) |
| **Argo CD Image Updater** | no CI→Git creds, deploys on push, per-app annotations | another controller to run; semver/regex rules must be right; git write-back commits by a bot |
| **Flux image automation** | same, native CRDs with `ImagePolicy` | Flux-only |
Regulated environments usually want the PR trail of the first; dev/staging love the
second. Both can coexist: updater on `dev`, PR promotion to `prod`.

## 2. Argo CD Image Updater — install and registries
**Version note:** the current Image Updater documentation (v1.x) is CRD-based: you create `ImageUpdater` custom resources, and v1.4.0 CRDs changed inheritance of `commonUpdateSettings` and removed `spec.namespace`. The annotation-based setup in sections 2 and 3 is the legacy v0.x configuration; follow the stable docs for v1.x and treat the annotations below as unconfirmed for v1.x (gated: unconfirmed, source is paywalled or blocked).
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml
```
Config `argocd-image-updater-config` ConfigMap:
```yaml
data:
  registries.conf: |
    registries:
      - name: GHCR
        prefix: ghcr.io
        api_url: https://ghcr.io
        credentials: pullsecret:argocd/ghcr-pull     # or secret:argocd/ghcr#token, env:VAR, ext:/script
        default: false
      - name: ECR
        prefix: 123456789012.dkr.ecr.eu-west-1.amazonaws.com
        api_url: https://123456789012.dkr.ecr.eu-west-1.amazonaws.com
        credentials: ext:/scripts/ecr-login.sh         # prints user:password; IRSA on the updater SA
        credsexpire: 10h
  log.level: info
  interval: 2m
  git.user: argocd-image-updater
  git.email: bot@example.com
```
It reads the Argo CD API (`argocd-image-updater-secret` with an API token of a user that
has `applications, update`) or Kubernetes directly (`--applications-api kubernetes`,
recommended in-cluster).

## 3. Annotate the Application
```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: web=ghcr.io/example/web, worker=ghcr.io/example/worker:~1.4
    argocd-image-updater.argoproj.io/web.update-strategy: semver            # semver | newest-build (was latest) | digest | alphabetical
    argocd-image-updater.argoproj.io/web.allow-tags: regexp:^v[0-9]+\.[0-9]+\.[0-9]+$
    argocd-image-updater.argoproj.io/web.ignore-tags: "*-rc*"
    argocd-image-updater.argoproj.io/web.helm.image-name: image.repository   # Helm value paths
    argocd-image-updater.argoproj.io/web.helm.image-tag: image.tag
    argocd-image-updater.argoproj.io/worker.kustomize.image-name: example/worker   # Kustomize: original image name
    argocd-image-updater.argoproj.io/write-back-method: git:secret:argocd/git-creds   # or argocd (edits the Application spec)
    argocd-image-updater.argoproj.io/write-back-target: helmvalues:/values-image.yaml   # or kustomization:/overlays/dev
    argocd-image-updater.argoproj.io/git-branch: main                                   # or base:image-updater-{{.AppName}} for PR flow (branch created, no PR)
```
- `semver` with a constraint in `image-list` (`:~1.4`, `:^2`) is the safe default;
  `newest-build` sorts by registry **creation time** (needs manifest pulls; slow on big
  repos — pair with `allow-tags`); `digest` tracks a mutable tag (`:latest`) by digest —
  for dev only; `alphabetical` for date-stamped tags.
- `platforms` annotation (`linux/amd64`) when multi-arch manifests confuse `newest-build`.
- Write-back `git` commits to the app's source repo (`.argocd-source-<app>.yaml` by
  default — a parameter override file Argo CD reads; `helmvalues:`/`kustomization:`
  targets edit real files instead, which is what humans expect). `argocd` write-back only
  patches the live Application (lost if the App is re-applied from Git — avoid with AppSets
  unless `ignoreApplicationDifferences` covers `spec.source.helm.parameters`).
- Pull secrets: the updater needs **read** access to the registry (`pullsecret:` can
  reuse the namespace's imagePullSecret).

Check: `kubectl -n argocd logs deploy/argocd-image-updater` shows
`Setting new image … to tag v1.4.7` / `Committed changes`; dry-run with
`argocd-image-updater run --once --dry-run` in CI to test annotations. Limits: one
updater per Argo CD instance; large fleets → raise `interval`, enable registry caching.

## 4. Flux image automation
```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata: { name: web, namespace: flux-system }
spec: { image: ghcr.io/example/web, interval: 5m, secretRef: { name: ghcr-pull } }
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata: { name: web, namespace: flux-system }
spec:
  imageRepositoryRef: { name: web }
  filterTags: { pattern: '^main-[a-f0-9]+-(?P<ts>[0-9]+)', extract: '$ts' }   # or policy.semver.range: '>=1.0.0 <2.0.0'
  policy: { numerical: { order: asc } }
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
metadata: { name: apps, namespace: flux-system }
spec:
  interval: 5m
  sourceRef: { kind: GitRepository, name: apps }
  git:
    checkout: { ref: { branch: main } }
    commit: { author: { name: fluxbot, email: flux@example.com }, messageTemplate: "chore: update {{range .Changed.Changes}}{{.OldValue}} -> {{.NewValue}} {{end}}" }
    push: { branch: main }     # or a feature branch + PR via CI
  update: { path: ./clusters/dev, strategy: Setters }
```
Manifests carry setter markers: `image: ghcr.io/example/web:v1.4.6 # {"$imagepolicy": "flux-system:web"}`
(or `:tag` / `:name` variants). Install with `flux bootstrap … --components-extra=image-reflector-controller,image-automation-controller`.
`flux get images all` and `flux reconcile image repository web` for ops.

## 5. Gotchas
The gotchas below (rate limits, bot commit loops, version support such as v1.4.7 or 0.13+) were not checked against the docs (gated: unconfirmed, source is paywalled or blocked).
- Mutable tags + `semver` = nothing updates (same tag, new digest): use `digest` strategy
  or immutable tags. Conversely, a CI that re-tags `v1.4.7` breaks the audit trail.
- Registry rate limits (Docker Hub 100/6h anonymous): authenticate and raise `interval`.
- The updater's commit triggers a sync *and* a webhook-driven CI run if your CI builds on
  push to the config repo — filter the bot author (`[skip ci]` in `git.commit-message-template`).
- Write-back to the same branch that humans edit races with their pushes; the updater
  retries, humans sometimes don't — use a separate `values-image.yaml` file per app.
- Image Updater only works with Helm and Kustomize sources (not plugins/plain dirs);
  multi-source apps supported from 0.13+.

## Verify
- [ ] Pushing `v1.4.8` produces a bot commit in ≤ interval and the app syncs to it; `v1.5.0-rc1` is ignored.
- [ ] `--dry-run --once` in CI validates annotations on every Application change.
- [ ] Bot commits don't trigger a CI build loop.
- [ ] Prod remains on the PR-promotion path (or has an explicit constraint range).

## Checked

2026-11-02. Confirmed against the Image Updater stable docs, the update methods and strategies pages and the Flux image automation guide: v1.0.0 moved from annotations to CRDs, newest-build is the renamed latest strategy and alphabetical the renamed name strategy, git.user and git.email and commit-message-template live in argocd-image-updater-config, Flux ImagePolicy and the image-reflector/automation controllers installed via --components-extra. Added a version note. Gated: the v0.x annotation details in sections 2 and 3 and the gotchas.

Method: documentation only; no commands were run.
