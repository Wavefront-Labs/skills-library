---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.rollback-mechanics
name: rollback-mechanics
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [rollback-procedure, fast-rollback, release-engineering, kubectl-rollout-undo, argo-rollouts, feature-flags, schema-migration]
level: practitioner
status: docs-checked
description: "Roll back fast and safely: kubectl rollout undo, Argo Rollouts abort semantics, and the limits of rollback when data or specs have already changed."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/", "https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_abort/", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollback mechanics

Make rollback a routine, rehearsed operation, decided before an incident rather than during one.

## Commands the reference pages document
```bash
# Kubernetes: roll back to the previous revision, or a specific one
kubectl rollout undo deployment/<NAME>
kubectl rollout undo deployment/<NAME> --to-revision=<N>
kubectl rollout undo --dry-run=server deployment/<NAME>   # preview

# Argo Rollouts: abort a rollout
kubectl argo rollouts abort <ROLLOUT_NAME> -n <NAMESPACE>
```
Argo Rollouts `abort` stops progressing the current rollout and reverts all steps; the previous ReplicaSet
becomes active. Caveat from the page: `spec.template` still holds the new version, so if the Rollout leaves
the aborted state it will try to go to the new version again; update `spec.template` back to the previous
version to fully revert.

## Notes
- The Workbook on canarying says feature-flag and experiment principles apply to any change to a service,
  not only software releases; a flag gives a way to turn behaviour off without redeploying.
- Check at release time, not mid-incident, whether the previous version can still run: that it still exists
  in your registry, and that data written by the new version is readable by the old one. Where a one-way
  data migration has run, roll forward or restore data instead (reasoning, not a quoted rule).
- A rollback issued by hand against a resource that a GitOps controller manages may be overwritten by the
  controller; revert in its source of truth instead (consult your tool's docs).

## Verify
- [ ] Rollback rehearsed for each release type, and the rehearsal timed.
- [ ] Each release records whether rolling back is safe.

## Checked
2026-11-01. Confirmed against the kubectl rollout undo reference (`--to-revision`, `--dry-run=server`), the
Argo Rollouts abort reference and the SRE Workbook canarying chapter (feature flags principle). Removed:
Helm, GitOps and `rollout history|status` commands, `revisionHistoryLimit` default, expand/contract
sequence, "sub-minute" claims and the "aim for minutes" target, none stated on those pages.
Method: documentation only; no commands were run.
