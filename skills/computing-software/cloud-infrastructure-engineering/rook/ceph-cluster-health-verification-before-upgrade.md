---
id: computing-software.cloud-infrastructure-engineering.rook.ceph-cluster-health-verification-before-upgrade
name: ceph-cluster-health-verification-before-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [health-verification, ceph-status, health-ok, active-clean, rook-version-label, toolbox]
level: practitioner
status: docs-checked
description: "The health checklist to confirm before a Rook or Ceph upgrade: pod states, ceph status expectations and how to read container versions."
sources:
  - https://rook.io/docs/rook/latest-release/Upgrade/health-verification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrades should begin with Ceph fully healthy so they can stay seamless.

Pods: in a healthy cluster every pod in the Rook namespace is `Running` or `Completed` with few, if any, restarts: `kubectl -n $ROOK_CLUSTER_NAMESPACE get pods`.

Ceph status from the toolbox:
```
TOOLS_POD=$(kubectl -n $ROOK_CLUSTER_NAMESPACE get pod -l "app=rook-ceph-tools" -o jsonpath='{.items[*].metadata.name}')
kubectl -n $ROOK_CLUSTER_NAMESPACE exec -it $TOOLS_POD -- ceph status
```
Signs of good health listed:
- Overall `HEALTH_OK` with no warnings or errors.
- All monitors in the quorum list.
- The manager is active.
- All OSDs up and in.
- All PGs `active+clean`.
- If applicable, all MDSes active for each filesystem, and all RGW daemons active.

When output deviates, look further with commands like `ceph osd status` and consult the Ceph troubleshooting docs. Rook will not upgrade Ceph daemons in `HEALTH_ERR`; `skipUpgradeChecks: true` or `continueUpgradeAfterChecksEvenIfNotHealthy: true` force it, potentially unsafely.

Versions: read a pod image with `kubectl ... get pod ${POD_NAME} -o jsonpath='{.spec.containers[0].image}'`, for example for `rook-ceph-mon-b`, or list status and images for every Rook pod with a `range .items[*]` jsonpath over the operator and cluster namespaces. Rook also sets a `rook-version` label on Ceph resources.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (health-verification) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 1 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
