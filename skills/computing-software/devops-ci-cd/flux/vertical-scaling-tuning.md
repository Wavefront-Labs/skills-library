---
id: computing-software.devops-ci-cd.flux.vertical-scaling-tuning
name: vertical-scaling-tuning
category: computing-software
field: devops-ci-cd
product: flux
tags: [vertical-scaling, concurrent, tmpfs, helm-cache, persistent-storage]
level: advanced
status: docs-checked
description: "Tune Flux controllers for hundreds of apps: worker counts, limits, in-memory builds, Helm index cache and persistent artifact storage."
sources:
  - https://fluxcd.io/flux/installation/configuration/vertical-scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For hundreds of apps deploying often, patch the controllers at bootstrap.

Workers and limits, on kustomize-controller, helm-controller and source-controller:

```yaml
- op: add
  path: /spec/template/spec/containers/0/args/-
  value: --concurrent=10
- op: add
  path: /spec/template/spec/containers/0/args/-
  value: --requeue-dependency=5s
```

and raise the `manager` container limits, for example cpu `2000m`, memory `2Gi`.

In-memory builds: more concurrency on kustomize-controller can hit disk I/O contention, so back `/tmp` with tmpfs (an emptyDir with `medium: Memory`), for example alongside `--concurrent=20`. tmpfs counts against pod memory, so use the GitRepository `ignore` field to exclude non-YAML files.

Helm index cache, for source-controller reading repositories with hundreds of charts:

```
--helm-cache-max-size=10
--helm-cache-ttl=60m
--helm-cache-purge-interval=5m
```

When the max size is reached an error is logged and the index is read from file. Watch `gotk_cache_events_total` to tune it.

Persistent storage: by default source-controller keeps its artifact cache in an `EmptyDir`, so a restart refetches every Git repo, Bucket, chart and OCI artifact. Create a PVC (for example 10Gi, class `standard`), add it to the resources, and patch the source-controller volumes to use it.

Node affinity and tolerations can pin the controllers to dedicated nodes. When vertical scaling is not an option, use sharding.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/vertical-scaling/ (raw source in the fluxcd/website repository).

Method: documentation only; no commands were run.
