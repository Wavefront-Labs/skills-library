---
id: computing-software.devops-ci-cd.github-actions.arc-container-modes-dind-vs-kubernetes
name: arc-container-modes-dind-vs-kubernetes
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, arc-container-mode, kubernetes-mode-dind, runner-container-hooks, kubernetes-mode-work-volume, arc-docker-builds]
level: advanced
status: docs-checked
description: "Choose ARC containerMode: dind (privileged Docker sidecar) vs kubernetes (container hooks, job pods, RWO work volume), and what breaks in each for container jobs and docker build."
sources: ["https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller#using-docker-in-docker-or-kubernetes-mode-for-containers", "https://github.com/actions/runner-container-hooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC container modes: dind vs kubernetes

## 1. dind
```yaml
containerMode:
  type: "dind"
```
Adds a Docker-in-Docker container using the `docker:dind` image by default (it runs the Docker daemon as root; the docs mention `docker:dind-rootless` as a replacement). The Docker-in-Docker container requires privileged mode, so isolate these runners (dedicated node pools or taints).

## 2. kubernetes mode
```yaml
containerMode:
  type: "kubernetes"
  kubernetesModeWorkVolumeClaim:
    accessModes: ["ReadWriteOnce"]
    storageClassName: "<STORAGE_CLASS>"
    resources: { requests: { storage: 1Gi } }
```
Runner uses **runner-container-hooks** (actions/runner-container-hooks): container steps run in separate pods that share the work volume.
- `ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER` defaults to `true`: jobs **must** declare `container:`.
  Set the env var to `"false"` on the runner container to allow plain jobs.
- Kubernetes mode has no Docker daemon, so `docker build` steps need a daemonless builder or dind mode.
- Needs a StorageClass that provisions volumes for the work volume claim.
- Customise the job pod (for example node selectors or tolerations) with a pod template file referenced by `ACTIONS_RUNNER_CONTAINER_HOOK_TEMPLATE` set on the runner container.

## 3. Choosing
| Need | Mode |
|---|---|
| Existing workflows with services and docker build, trusted repos | dind on isolated nodes |
| Avoid privileged pods | kubernetes mode plus a daemonless builder |

## Verify
- [ ] A job with `services: postgres` passes (dind) or a `container:` job passes (kubernetes).

## Checked
2026-10-28. Confirmed on the deploy-runner-scale-sets page: containerMode types dind and kubernetes; dind uses `docker:dind` by default and requires privileged mode; `kubernetesModeWorkVolumeClaim` with `ReadWriteOnce` access mode; `ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER` set to false on the runner container allows jobs without a job container; `ACTIONS_RUNNER_CONTAINER_HOOK_TEMPLATE` points at a mounted pod template. Confirmed repo: actions/runner-container-hooks.
Removed (not confirmed): "docker: not found" wording for the default mode, layer re-pull and pod density costs, the "defaults to true" statement for the job container variable, rootless builder names, PVC timing, RBAC details, the Pod Security row and the gp3 / 5Gi sample values.

Method: documentation only; no commands were run.
