---
id: computing-software.devops-ci-cd.argocd-image-updater.imageupdater-status-and-conditions
name: imageupdater-status-and-conditions
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, status, conditions, recent-updates, kubectl-get-imageupdater, ready, monitoring]
level: practitioner
status: docs-checked
description: "Monitor an ImageUpdater CR through kubectl: printer columns, status fields such as recentUpdates, and the Ready, Reconciling and Error conditions including partial errors."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/examples/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ImageUpdater status and conditions

Quick overview:

```bash
kubectl get imageupdater -n argocd
# NAME                 APPS   IMAGES   LAST CHECKED             READY
# production-updater   7      3        2026-03-02T22:10:00Z     True
```

Full status: `kubectl get imageupdater production-updater -n argocd -o yaml`, or JSONPath such as `-o jsonpath='{.status.recentUpdates}' | jq .`.

Status fields: `observedGeneration`, `lastCheckedAt`, `lastUpdatedAt` (only set when an image was updated), `applicationsMatched`, `imagesManaged`, `recentUpdates`, `conditions`.

`recentUpdates` lists each image updated in the last cycle with `alias`, `image`, `newVersion`, `applicationsUpdated`, `updatedAt` and `message`.

Conditions follow Kubernetes API conventions:

| Condition | True | False |
|---|---|---|
| `Ready` | last reconciliation completed | it failed entirely |
| `Reconciling` | a check is in progress | idle, awaiting next cycle |
| `Error` | errors occurred in last reconciliation | none |

Partial failure: when some applications succeed and others fail, `Ready` is `True` with reason `ReconcileCompletedWithErrors` and `Error` is also `True` with reason `PartialErrors`; read the condition messages.

## Checked

2026-11-04. Confirmed against applications.md (Monitoring status: printer columns, status fields, recentUpdates fields, conditions table, partial-error note), update.md (observing update status) and the examples page (kubectl jsonpath commands). Removed a generic self-check line the pages do not state.

Method: documentation only; no commands were run.
