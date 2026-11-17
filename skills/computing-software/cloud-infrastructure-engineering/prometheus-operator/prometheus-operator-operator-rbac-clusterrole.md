---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-operator-rbac-clusterrole
name: prometheus-operator-operator-rbac-clusterrole
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [operator-rbac, statefulsets, prometheus-operated, kubelet-endpoints, least-privilege, serviceaccount-automount]
level: advanced
status: docs-checked
description: "Understand why the Prometheus Operator ClusterRole grants what it does, and bind it to the operator ServiceAccount."
sources:
  - https://prometheus-operator.dev/docs/platform/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The operator needs its own ClusterRole, separate from the one used by Prometheus pods. A cluster admin creates the ClusterRole and a ClusterRoleBinding (or RoleBinding) to the ServiceAccount the operator Deployment runs as; the Deployment must reference it in `spec.template.spec.serviceAccount`.

## Why each permission
- Its own CRDs: `get`/`list`/`watch` on alertmanagers, alertmanagerconfigs, prometheuses, prometheusagents, thanosrulers, monitors, rules, probes and scrapeconfigs; `patch` on the four instance resources and `patch`/`update` on their `/finalizers`; write access to the `/status` subresources. The page prose says the operator needs all actions on its CRDs, but the manifest it ships is narrower.
- `statefulsets`: Alertmanager, Prometheus and ThanosRuler objects materialise as StatefulSets, so every change must be applied.
- `configmaps` and `secrets`: the operator generates configuration into them.
- `pods` `list`: to find pods running an old version during version migrations (the prose also mentions deleting them, but the manifest grants only `list`).
- `services` and `services/finalizers` (`get`, `create`, `update`, `delete`): the governing Services `prometheus-operated` and `alertmanager-operated` are reconciled by the operator.
- `nodes` `list`/`watch` and `endpoints` `create`/`update`: the kubelet is not self-hosted, so the operator syncs kubelet IPs into an Endpoints object.
- `namespaces` `get`/`list`/`watch`, `ingresses`, `events.k8s.io` events and `storage.k8s.io` `storageclasses` `get`.

## Service account hardening
The example ServiceAccount sets `automountServiceAccountToken: false`.

## Checked

2026-11-08. Read the RBAC page in full. Corrected the CRD permissions to match the shipped manifest (get/list/watch, patch, finalizers and status writes, not all actions) and the pods list note; removed unsourced advice on --namespaces and token projection.

Method: documentation only; no commands were run.
