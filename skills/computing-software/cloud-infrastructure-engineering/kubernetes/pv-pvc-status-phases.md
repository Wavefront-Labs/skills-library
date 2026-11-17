---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pv-pvc-status-phases
name: pv-pvc-status-phases
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, persistentvolume, pv-status-phases, pvc, pvc-pending, released]
level: practitioner
status: docs-checked
description: "Read PV phases (Available, Bound, Released, Failed) and PVC phases (Pending, Bound, Lost), their transitions, and what action each state calls for."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#phase", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storage-object-in-use-protection", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PV and PVC status phases

## PersistentVolume
| Phase | Meaning | Action |
|---|---|---|
| Available | free, not bound | will bind to a matching claim |
| Bound | bound to a PVC (`spec.claimRef`) | normal |
| Released | its claim was deleted but the storage is not yet reclaimed (with `Retain` the data remains) | reclaim manually; reuse requires deleting the PV's `claimRef` |
| Failed | the volume has failed its automated reclamation | check controller events and the backing storage |

## PersistentVolumeClaim
| Phase | Meaning | Action |
|---|---|---|
| Pending | no PV yet | check events: provisioning, WaitForFirstConsumer, no matching static PV |
| Bound | bound | normal |
| Lost | the claim's PV no longer exists (API phase `Lost`) | check what removed the PV; restore from backup if the data is gone |

## Useful views
```bash
kubectl get pv                      # STATUS, CLAIM, RECLAIM POLICY columns
kubectl get pv -o custom-columns=PV:.metadata.name,PHASE:.status.phase,CLAIM:.spec.claimRef.name,SINCE:.status.lastPhaseTransitionTime
kubectl get pvc -A
kubectl describe pvc <name>         # Events at the end
```
`status.lastPhaseTransitionTime` records when the PV last changed phase (feature gate `PersistentVolumeLastPhaseTransitionTime`: beta 1.29, stable 1.31), handy for cleanup policies.

## Transitions to know
- Delete PVC with Retain: Bound -> Released (the data remains, so the PV is not offered to other claims).
- Re-use a Released PV: delete its `claimRef` (`kubectl patch pv <pv> -p '{"spec":{"claimRef":null}}'`) so a new PVC can bind, after confirming what the data is.
- PVC deletion while a pod uses it: removal is postponed, and the PVC shows `Terminating`, until no pod uses it (storage object in use protection).

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed the PV phases (Available, Bound, Released, Failed), Pending for newly created volumes, the PVC phases Pending/Bound/Lost (core/v1 types), storage object in use protection, the claimRef recovery step, and the lastPhaseTransitionTime gate history (beta 1.29, stable 1.31, feature-gate page). Removed `grep`/`sed` filters and the 'Released only with Retain' and 'data likely gone' wording the docs do not state.

Method: documentation only; no commands were run.
