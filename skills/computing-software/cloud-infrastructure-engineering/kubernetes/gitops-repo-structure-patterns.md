---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gitops-repo-structure-patterns
name: gitops-repo-structure-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, repo-structure, mono-repo, multi-repo, environment-branches, environment-directories, app-of-apps, applicationset, flux-kustomization, codeowners, blast-radius, argo-cd, fluxcd]
level: practitioner
status: docs-checked
description: "Choose a GitOps repo layout: mono-repo vs multi-repo, per-environment directories vs branches, and how that choice drives app-of-apps/ApplicationSet and Flux Kustomization design."
sources: ["https://github.com/fluxcd/website/blob/main/content/en/flux/guides/repository-structure.md", "https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/best_practices.md", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/applicationset/Generators-Git.md", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/cluster-bootstrapping.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitOps repo structure — the decision that's expensive to reverse later

**Why this matters first, before picking a tool:** Argo CD/Flux render whatever
structure you give them; the structure itself determines blast radius, who can
approve what, and how promotion works. Restructuring a live GitOps repo later means
rewriting every `Application`/`Kustomization` path reference at once.

## 1. Mono-repo vs multi-repo
- **Mono-repo** (one repo, all apps, all envs): simplest to bootstrap, one PR can
  touch two apps' configs together (useful for genuinely coupled changes), one
  CODEOWNERS file per directory gates review per team/app. Downside: no natural
  access boundary — anyone with repo write can touch any app's prod config unless
  you lean hard on directory-scoped CODEOWNERS + branch protection (the Flux guide notes Git itself cannot restrict reading of files
  within a repository; access control comes from the hosting platform).
- **Multi-repo** (config repo per app, or per team, separate from a cluster
  "fleet" repo that references them): natural access boundary (repo-level
  permissions = team boundary), but promotion and cross-app coupled changes now
  span repos, and app-of-apps/ApplicationSet has to enumerate N repos instead of N
  directories.
- **App source vs config repo split** (orthogonal to the above): application code in
  one repo, rendered/pinned manifests in another, is the common middle ground — CI
  in the app repo produces an image + bumps a tag in the config repo, keeping
  "what's deployed" fully declarative and independent of app CI pipeline changes.
  This is *the* pattern that makes GitOps's "git is the source of truth for what's
  live" property actually hold; skipping it (deploying straight from app-repo CI)
  reintroduces push-based deploys with GitOps tooling bolted on top for no benefit.

## 2. Per-environment: directories vs branches vs separate repos
- **Directories per env** (`clusters/dev`, `clusters/staging`, `clusters/prod`, each
  with its own Kustomize overlay or Argo CD `Application`/Flux `Kustomization`
  pointing at `main`): the layout used in the Flux repository-structure guide, which keeps all
  environments on one branch (`main`) and deletes short-lived branches after merge. Diffing
  directories shows exactly what differs per env, and promotion is a PR copying a change from one
  directory's overlay into the next.
- **Branches per env** (`dev` branch auto-deploys, merge to `staging`, merge to
  `prod`): looks like a natural promotion pipeline (merge = promote) but means long-lived
  branches that can diverge, you diff branches rather than directories, and hotfixing prod
  needs a path that does not go through staging. These are trade-offs to weigh, not tool
  limitations; the Flux guide's examples use one branch with per-environment directories.
- **Repo per environment**: strongest isolation (the Flux guide notes a separate production
  repository lets you grant access to a subset of people while everyone can clone staging and open
  pull requests) at the cost of duplication; reserve it for strict compliance boundaries
  (e.g. a regulated prod cluster needing a separately audited change path).

## 3. How the structure maps onto the tooling
- Argo CD **app-of-apps**/**ApplicationSet**: a Git directory generator
  (`generators: - git: directories: - path: clusters/*/apps/*`) creates one generated Application
  per matching directory, with `{{.path.path}}` and `{{.path.basename}}` available to the
  template and an `exclude` option to skip directories — directory structure *is* the fan-out
  mechanism. Argo CD's docs say Git generators need admin-level review of PRs, because a PR can
  create Applications. See `computing-software.devops-ci-cd.argo-cd.app-of-apps-pattern` and
  `applicationset-generators-for-fleets` for the generator mechanics.
- Flux: each cluster state lives in a dedicated directory such as `clusters/production`, and
  `Kustomization` resources tell Flux which directory holds the app manifests and how to patch
  them — mirrors the directory layout almost 1:1; see `flux-cd-fundamentals`.
- Whichever tool, the repo's directory boundaries should match the **RBAC/CODEOWNERS
  boundaries** you actually want — if `clusters/prod/**` isn't under a stricter
  CODEOWNERS rule and branch protection than `clusters/dev/**`, the directory split
  is cosmetic, not a control.

## Gotchas
- A shared `base/` referenced by every env's overlay means a base change ships to
  every environment in the *next* overlay-level PR merge for each — verify your
  promotion process actually re-reviews base changes per environment rather than
  assuming "merged to main" means "reviewed for prod."
- Secrets must never live as plaintext in any of these layouts regardless of
  mono/multi-repo choice — see the sealed-secrets/external-secrets/SOPS skills.
- Renaming a top-level directory (`envs/` → `clusters/`) breaks every
  `Application.spec.source.path`/Flux `Kustomization.spec.path` referencing it
  simultaneously — treat it as a breaking change requiring a coordinated update,
  not a casual rename.
- A single mono-repo with no directory-level CODEOWNERS enforcement gives every
  contributor prod-equivalent reach despite looking segmented — audit this
  explicitly, it's the most common gap between intended and actual blast radius.

## Verify
- [ ] Diffing two environment directories shows only the intended differences
      (replicas, resource limits, image tag/digest) — no accidental drift in shared
      fields that should be identical.
- [ ] CODEOWNERS/branch protection on the prod path actually requires the approvals
      you think it does (test with a throwaway PR).
- [ ] A base change rolls out to every env's overlay through a reviewed PR per
      environment, not silently on merge to main.
- [ ] The chosen layout's fan-out (ApplicationSet generator / Flux root Kustomization)
      produces exactly the expected set of Applications/Kustomizations — no missing
      or duplicated app-env pairs.

## Checked

Checked 2026-10-27. Documentation checked: Flux repository structure guide (fluxcd/website main), Argo CD best-practices page, ApplicationSet Git generator and cluster bootstrapping docs (argoproj/argo-cd master). Confirmed: Flux guide describes monorepo, repo-per-team and repo-per-app layouts with environments on one branch and `clusters/<name>` directories; a separate production repository allows narrower access; Argo CD recommends a config repository separate from application source; the ApplicationSet Git directory generator, `{{.path.path}}`/`{{.path.basename}}` and `exclude` behaviour; the Git generator security note about PR review. Fixed: "dominant modern pattern" and "legacy" labels, which no source supports (reworded as trade-offs).

Method: documentation only; no commands were run.
