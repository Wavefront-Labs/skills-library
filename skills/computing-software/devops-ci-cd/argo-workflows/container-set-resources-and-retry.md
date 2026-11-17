---
id: computing-software.devops-ci-cd.argo-workflows.container-set-resources-and-retry
name: container-set-resources-and-retry
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [container-set-retry, resource-requests, retry-strategy, emissary-executor, containerset-retries]
level: advanced
status: docs-checked
description: "Size ContainerSet resource requests so the total equals peak concurrent need and use containerSet.retryStrategy, which differs from template retries."
sources: ["https://argo-workflows.readthedocs.io/en/latest/container-set-template/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ContainerSet resource sizing and retry
Every container in a ContainerSet starts immediately; the emissary executor only starts the main process once its dependencies finish, but idle containers still hold and bill their requests. If requests are small this is irrelevant. If large, set per-container requests so the sum equals the most you need simultaneously.

- Sequence a -> b -> c needing 1Gi, 2Gi, 1Gi: request 512Mi, 1Gi, 512Mi (total 2Gi, enough for b).
- Diamond a -> b,c -> d needing 1000, 2000, 1000, 1000 CPU: b and c overlap, so request 500, 1000, 1000, 500 (total 3000).
- Lopsided a -> b where a is a 10 hour job with tiny requests and b is a 5 minute job needing GPUs and 100Gi: the sum means paying for the GPU for 10 hours, so a ContainerSet is a poor fit.

Retries are set inside the set:

```yaml
containerSet:
  retryStrategy:
    retries: "10"
    duration: 30s
```
`retries` is the maximum count and `duration` the time limit. Unlike template-level `retryStrategy` (which creates new Pods or nodes), the executor re-runs your `command` inside the same container. UI nodes stay the same and retry output is appended to the original container's logs. If the executor cannot locate the container's `command`, it does not retry, because that would fail every time.

## Checked
2026-11-08. Confirmed against the Argo Workflows ContainerSet Template page: resource request examples A, B and C, the `containerSet.retryStrategy` fields `retries` and `duration`, in-container re-run with appended logs, and no retry when `command` cannot be located. Nothing removed.
Method: documentation only; no commands were run.
