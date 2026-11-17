---
id: computing-software.database-administration.patroni.patroni-kubernetes-role-labels
name: patroni-kubernetes-role-labels
category: computing-software
field: database-administration
product: patroni
tags: [patroni, kubernetes, labels, role-label, service-selector]
level: practitioner
status: docs-checked
description: "Customise the pod role labels and migrate Services with tmp_role_label to reduce downtime."
sources:
  - https://patroni.readthedocs.io/en/latest/kubernetes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change role label names or values without breaking traffic routing.

By default Patroni sets labels on the pod it runs in based on the node's role, such as `role=primary`. The key and values can be customised with `kubernetes.role_label`, `kubernetes.leader_label_value`, `kubernetes.follower_label_value` and `kubernetes.standby_leader_label_value`.

To migrate from default to custom labels with less downtime:
1. Set `kubernetes.tmp_role_label` (for example `tmp_role`). After pods restart they carry `role: primary` and `tmp_role: primary`.
2. When all pods are updated, change the Service selector to use `cluster-name: foo` and `tmp_role: primary`.
3. Set your custom values (for example `kubernetes.leader_label_value=primary`), restart pods again so they get the new labels.
4. Change the Service selector to the new role label and value.
5. Remove the temporary label from configuration and update all pods.

In ConfigMaps mode, point the Postgres Service at the leader using a label selector on the `role_label`. Spilo, its Helm chart, and the postgres-operator are referenced as ways to run Patroni at scale; the repository's example manifest cannot use PersistentVolumes because of permission issues.

## Checked

2026-11-08. Confirmed against the Patroni Kubernetes page (customize role label, ConfigMaps and examples sections, read in full). Removed the per-option default values, the `bootstrap_labels` option (added in 4.1.0) and the `tmp_role_label` default-value remark, which that page does not state.

Method: documentation only; no commands were run.
