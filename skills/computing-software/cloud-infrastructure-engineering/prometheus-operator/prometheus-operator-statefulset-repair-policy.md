---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-statefulset-repair-policy
name: prometheus-operator-statefulset-repair-policy
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [repair-policy-for-statefulsets, stuck-rollout, pod-eviction, poddisruptionbudget, statefulset-recovery]
level: advanced
status: docs-checked
description: "Recover a StatefulSet rollout stuck after a bad Prometheus or Alertmanager update using the operator repair-policy-for-statefulsets argument."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A StatefulSet update that produces a broken pod (bad image, invalid config) can leave the rollout stuck, because the StatefulSet controller does not roll back by itself (Kubernetes forced rollback behaviour).

## Operator repair
Start the operator with `--repair-policy-for-statefulsets`:
- `none` (default): no automatic action; you must delete or evict the stuck pod.
- `evict`: evicts the stuck pod through the Eviction API, respecting PodDisruptionBudgets. The safer option.
- `delete`: deletes it directly, bypassing PDBs; use when eviction is blocked by an unsatisfiable PDB.

It repairs at most one pod per reconciliation loop, walking pods in reverse ordinal order. Only pods whose revision matches neither the current nor the desired update revision are considered, and pods already being deleted are skipped.

Example argument: `--repair-policy-for-statefulsets=evict`.

## Manual repair
Identify the stuck pod and run `kubectl delete pod -n <namespace> <pod-name>`. The StatefulSet controller recreates it at the current revision; once the underlying problem is fixed the rollout proceeds.

## Checked

2026-11-08. Read the troubleshooting page in full. Policies, default and repair behaviour match; no changes needed.

Method: documentation only; no commands were run.
