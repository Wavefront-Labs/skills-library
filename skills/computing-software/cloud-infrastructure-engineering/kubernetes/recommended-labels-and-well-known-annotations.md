---
id: computing-software.cloud-infrastructure-engineering.kubernetes.recommended-labels-and-well-known-annotations
name: recommended-labels-and-well-known-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, labels, recommended-labels, app-kubernetes-io, well-known-annotations, last-applied-configuration, metadata-conventions]
level: practitioner
status: docs-checked
description: "Apply the app.kubernetes.io recommended labels and know the well-known labels and annotations tools read (last-applied-configuration, change-cause)."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/", "https://kubernetes.io/docs/reference/labels-annotations-taints/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recommended labels and well-known annotations

## Recommended labels (shared prefix `app.kubernetes.io/`)
| Label | Example | Meaning |
|---|---|---|
| `name` | `mysql` | name of the application |
| `instance` | `mysql-abcxyz` | unique name identifying the instance of an application |
| `version` | `5.7.21` | current version of the application (SemVer, revision hash, etc.) |
| `component` | `database` | component within the architecture |
| `part-of` | `wordpress` | name of a higher level application this one is part of |
| `managed-by` | `Helm` | tool being used to manage the operation of an application |
```yaml
metadata:
  labels:
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: mysql-abcxyz
    app.kubernetes.io/version: "5.7.21"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: Helm
```
These are recommended, not required by any core tooling; the docs advise applying them on
every resource object. Record application name and instance separately, and every instance
must have a unique name. Use `name` and `instance` in selectors, and keep `version` out of a
Deployment selector (the selector is immutable). Enforce them with an admission policy if you
want consistency.

## Well-known labels you read, not set
`kubernetes.io/hostname`, `kubernetes.io/os`, `kubernetes.io/arch`,
`topology.kubernetes.io/zone` and `topology.kubernetes.io/region`,
`node.kubernetes.io/instance-type`, `kubernetes.io/metadata.name` (set on every namespace,
usable in NetworkPolicy namespaceSelectors), `pod-template-hash` (added by the Deployment
controller), `batch.kubernetes.io/job-name`, `statefulset.kubernetes.io/pod-name` (select a
single StatefulSet pod). The full list is on the "Well-Known Labels, Annotations and Taints"
page.

## Well-known annotations
| Annotation | Set by / used for |
|---|---|
| `kubectl.kubernetes.io/last-applied-configuration` | legacy kubectl change tracking, superseded by server-side apply |
| `kubernetes.io/change-cause` | shown as CHANGE-CAUSE in `kubectl rollout history`; set with `kubectl annotate deployment/<name> kubernetes.io/change-cause="..."` (the `--record` flag is deprecated) |
| `kubectl.kubernetes.io/restartedAt` | written into the pod template metadata by `kubectl rollout restart` |
| `kubectl.kubernetes.io/default-container` | container used by kubectl commands without `-c` |
| `deployment.kubernetes.io/revision` | Deployment/ReplicaSet revision |
| `storageclass.kubernetes.io/is-default-class` | default StorageClass |
| `cluster-autoscaler.kubernetes.io/safe-to-evict` | cluster autoscaler eviction control |
| `kubernetes.io/description` | free-text description |
| `kubernetes.io/egress-bandwidth` | Pod egress rate limit in bits per second (for example `10M`) |

## Gotchas
- Label values are at most 63 characters and start and end alphanumeric; the total of all
  annotations on an object must not exceed 256 KiB.

## Verify
- [ ] `kubectl get deploy -A -L app.kubernetes.io/name,app.kubernetes.io/part-of` has no empty columns for app workloads.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Recommended Labels", "Well-Known Labels,
Annotations and Taints" and "Labels and Selectors" (latest release v1.37.1). Confirmed: the six
labels and meanings, each label and annotation listed above including `change-cause` behaviour
and the `--record` deprecation in the Deployment page, the last-applied "legacy" note, the
256 KiB limit. Removed unconfirmed claims (tools that key off the labels, the Helm chart label
remark, the `controller-revision-hash` and `pod-security` entries, "delete only when switching to SSA").
Method: documentation only; no commands were run.
