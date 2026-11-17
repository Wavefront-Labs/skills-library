---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-concurrent-pvc
name: runner-kubernetes-concurrent-pvc
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [kubernetes, pvc, concurrent-id, persistent-volume, build-dir]
level: advanced
status: docs-checked
description: "Use $CI_CONCURRENT_ID to give each concurrent job its own persistent volume claim."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-concurrency PVC

To keep a persistent build directory without sharing it between simultaneous jobs, include `$CI_CONCURRENT_ID` in the claim name:

```
[[runners.kubernetes.volumes.pvc]]
  name = "build-pvc-$CI_CONCURRENT_ID"
  mount_path = "/builds"
```
`CI_CONCURRENT_ID` identifies the job slot within the runner, so with `concurrent = 4` there are four distinct claims.

The security guide warns that `GIT_STRATEGY: fetch`, which reuses the local working copy, fetch on shared environments lets any user with access to the reusable copy add code that runs in other users' pipelines.

## Checked

2026-11-03. Confirmed against the CI_CONCURRENT_ID claim name on the Kubernetes executor page and the fetch warning on the Security page. Removed an unsourced instruction.

Method: documentation only; no commands were run.
