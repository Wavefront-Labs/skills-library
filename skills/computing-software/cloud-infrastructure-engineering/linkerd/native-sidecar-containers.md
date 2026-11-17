---
id: computing-software.cloud-infrastructure-engineering.linkerd.native-sidecar-containers
name: native-sidecar-containers
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, native-sidecars, jobs, kubernetes]
level: practitioner
status: docs-checked
description: "Run the proxy as a Kubernetes native sidecar to let meshed Jobs finish and avoid init container startup races."
sources:
  - https://linkerd.io/2.19/features/native-sidecars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd supports Kubernetes native sidecar containers, which fix two long-standing problems with regular sidecars:

1. Meshed Jobs and CronJobs cannot terminate without modification, because the sidecar proxy keeps running after the job container exits.
2. There are startup race conditions in meshed pods when init containers also need network access.

Enable it with the annotation:

```yaml
metadata:
  annotations:
    config.beta.linkerd.io/proxy-enable-native-sidecar: "true"
```

Set it at the level of an individual namespace or workload, or globally at install time.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/features/native-sidecars/. Both problems fixed by native sidecars, the annotation name and the namespace, workload or install-time scopes.

Removed or reworded: Claims about injection-time reads, cluster prerequisites and the rollout advice (not on the cited page).

Method: documentation only; no commands were run.
