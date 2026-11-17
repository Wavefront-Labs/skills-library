---
id: computing-software.cloud-infrastructure-engineering.kubernetes.devcontainers-for-kubernetes-platform-teams
name: devcontainers-for-kubernetes-platform-teams
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [devcontainer, devcontainer-json, codespaces, dev-environment, local-to-cluster, kubeconfig, feature-spec, remote-containers, platform-engineering, reproducible-dev-env, docker-in-docker]
level: advanced
status: docs-checked
description: "Standardizing devcontainer.json across a platform's golden-path repos so every dev environment ships with the right kubeconfig, CLI tools and cluster access baked in."
sources: ["https://containers.dev/implementors/json_reference/", "https://containers.dev/implementors/features/", "https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainerjson-reference.md", "https://github.com/devcontainers/features"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# devcontainers as a platform standard

**Goal:** make "clone the repo, open it, you have kubectl/helm/the right
kubeconfig and cluster access already working" true for every golden-path
repo, instead of a wiki page of manual setup steps that drifts the moment
someone upgrades a CLI tool locally. This is the "developer environment"
leg of a platform, distinct from live local-to-cluster traffic routing
(`computing-software.cloud-infrastructure-engineering.kubernetes.telepresence-and-local-to-cluster-development`).

## 1. devcontainer.json as a platform-owned artifact, not per-repo DIY
Ship one canonical `.devcontainer/devcontainer.json` (or a small family, one
per golden-path archetype) from the Backstage scaffolder skeleton
(`computing-software.cloud-infrastructure-engineering.kubernetes.backstage-scaffolder-golden-path-templates`),
not left for each team to hand-write. Pin `image` to a platform-maintained
base (not `mcr.microsoft.com/devcontainers/base:latest` — unpinned `latest`
means the dev environment silently changes under a team with no changelog)
and use **Features** (`features: {"ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {"version": "<kubectl-version>", "helm": "<helm-version>"}}`;
the Feature installs the latest versions unless you set them) to layer CLI tools reproducibly instead of a hand-maintained Dockerfile every
team copies and forgets to update.

```json
{
  "image": "ghcr.io/org/platform-devcontainer-base:1.4",
  "features": {
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {"version": "<kubectl-version>"},
    "ghcr.io/devcontainers/features/docker-in-docker:4": {}
  },
  "mounts": ["source=${localEnv:HOME}/.kube,target=<CONTAINER_HOME>/.kube,type=bind"],
  "postCreateCommand": "kubectl config use-context dev-cluster"
}
```

## 2. Cluster access inside the container — the actual hard part
Three real patterns, pick deliberately:
- **Bind-mount the host kubeconfig** (shown above) — simplest, works when
  the dev's local kubeconfig already has the right context (e.g. SSO-based
  cloud CLI auth). Breaks if the kubeconfig references an exec credential
  plugin (usually a cloud CLI) not installed inside the container — install the same auth plugin via a Feature or
  `postCreateCommand`, or the mounted kubeconfig is present but unusable.
- **Short-lived token injected at container start** — platform CI/dev-portal
  mints a scoped token (e.g. via an OIDC-federated ServiceAccount) and writes
  it into the container's kubeconfig on create; safer for ephemeral/cloud
  dev environments (Codespaces) where you don't want the user's full local
  cloud credentials mounted at all.
- **In-cluster dev pod** (the container *is* a pod in the dev cluster,
  reached through a remote-development tool) — the
  container already has a ServiceAccount; no kubeconfig distribution
  problem, but now you're managing a dev-pod lifecycle (idle timeout,
  cleanup) as its own platform surface.

## 3. Docker-in-Docker and resource limits
Teams that need to build images inside the devcontainer want
the `docker-in-docker` Feature or `docker-outside-of-docker` (re-uses the host Docker socket,
mounted at `/var/run/docker-host.sock` by default; lighter, but the container can then drive
the host's Docker). DinD runs a second Docker daemon inside the container; on cloud-hosted dev
environments size the machine type for image builds.

## 4. Gotchas
- `postCreateCommand` runs once, when a new container is created and first assigned to a user;
  a step that must run every time (refreshing a short-lived token) belongs in
  `postStartCommand` (each start) or `postAttachCommand` (each attach).
- By default the tool picks the Feature install order, guided by each Feature's
  `installsAfter` (soft) and `dependsOn` (hard) metadata. If your own Features rely on each
  other, declare it there or set `overrideFeatureInstallOrder` in `devcontainer.json`.
- Cloud services may run `onCreateCommand` and `updateContentCommand` while prebuilding, with
  only repository- and org-scoped secrets; steps that need user-scoped secrets belong in
  `postCreateCommand` or later.

## Verify
- A fresh clone + "Reopen in Container" produces a shell where
  `kubectl get nodes` against the intended dev/staging cluster succeeds
  with zero manual steps beyond opening the folder.
- The same `devcontainer.json` works both locally (VS Code Dev Containers)
  and in GitHub Codespaces without environment-specific edits — if it
  doesn't, the divergence (usually secret timing or local kubeconfig
  assumptions) is documented, not silently tolerated.
- Rebuilding the container from a clean image cache reproduces the identical
  tool versions as the previous build (confirms the base image + Features
  are actually pinned, not drifting on `latest`).

## Checked
2026-10-27, against the Dev Container spec (devcontainers/spec main: `devcontainerjson-reference.md`, `devcontainer-features.md`) and the `devcontainer-feature.json` files in devcontainers/features main (kubectl-helm-minikube 1.3.1, docker-in-docker 4.1.3, docker-outside-of-docker 1.10.1). Confirmed: lifecycle command timing (`onCreateCommand`, `updateContentCommand`, `postCreateCommand`, `postStartCommand`, `postAttachCommand`) and prebuild secret scope, `mounts` string syntax and `${localEnv:...}`, Feature `installsAfter`/`dependsOn` and `overrideFeatureInstallOrder`, the kubectl-helm-minikube `version`/`helm` options defaulting to latest, current Feature major versions, and the docker-outside-of-docker socket path.
Method: documentation only; no commands were run.
