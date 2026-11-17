---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeclaim-spec-and-inheritance
name: karpenter-nodeclaim-spec-and-inheritance
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeclaim, spec, requirements, immutable, expireafter, terminationgraceperiod, finalizer, ownerreferences]
level: advanced
status: docs-checked
description: "NodeClaim spec fields and what they inherit from the NodePool: nodeClassRef, taints, expireAfter, terminationGracePeriod, requirements, resource requests, labels, finalizer."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclaims.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodeClaim spec and inheritance

NodeClaims cannot be modified; changes come via NodePool edits and drift. You can also create a NodeClaim manually to request capacity outside normal provisioning.

Inherited from the NodePool template:
- `spec.nodeClassRef` (`group`, `kind`, `name`), `spec.taints`, `spec.startupTaints`.
- `spec.expireAfter` (default `720h`, `Never` disables). Changing it on the NodePool drifts existing claims.
- `spec.terminationGracePeriod`: after it, pods are force-deleted regardless of PDBs or do-not-disrupt. Undefined means wait indefinitely. Pods are deleted early to respect their own `terminationGracePeriodSeconds`. Changing it drifts claims.
- Labels and annotations from `spec.template.metadata`; they sync to the Node. Labels become requirements, so requirements plus labels are capped at 100.

Resolved at scheduling:
- `spec.requirements`: NodePool requirements combined with pod constraints (nodeSelector, nodeAffinity); operators In, NotIn, Exists, DoesNotExist, Gt, Lt, Gte, Lte. Includes the instance-type candidate list, zone, arch and capacity-type.
- `spec.resources.requests`: aggregate pod requests used to right-size the instance.

Metadata set by Karpenter:
- name generated with the NodePool name as prefix.
- `ownerReferences` to the NodePool with `blockOwnerDeletion: true`, so deleting the NodePool cascades.
- finalizer `karpenter.sh/termination`: cordon, drain, terminate instance, delete Node before the claim goes.
- hash annotations such as `karpenter.sh/nodepool-hash` and `karpenter.k8s.aws/ec2nodeclass-hash` used for drift.

## Checked

2026-11-04. Confirmed against the NodeClaims concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
