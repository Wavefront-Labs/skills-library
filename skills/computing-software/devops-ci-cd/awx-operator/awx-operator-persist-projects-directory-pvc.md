---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-persist-projects-directory-pvc
name: awx-operator-persist-projects-directory-pvc
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, projects-persistence, pvc, storage-class, readwritemany, existing-claim]
level: practitioner
status: docs-checked
description: "Persist /var/lib/projects with an operator-created or existing PersistentVolumeClaim."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/persisting-projects-directory.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator persist projects directory pvc

To persist the `/var/lib/projects` directory, these awx-operator variables are customizable (defaults in brackets):
- `projects_persistence` (false): whether the directory is persistent.
- `projects_storage_class` (empty): the PersistentVolume storage class.
- `projects_storage_size` (8Gi): the PersistentVolume size.
- `projects_storage_access_mode` (ReadWriteMany): the PersistentVolume access mode.
- `projects_existing_claim` (empty): an existing PersistentVolumeClaim to use; cannot be combined with `projects_storage_*`.

Operator-managed volume:

```yaml
spec:
  projects_persistence: true
  projects_storage_class: rook-ceph
  projects_storage_size: 20Gi
```

To use an existing claim, set `projects_existing_claim` to the PVC name instead of the `projects_storage_*` settings.

## Checked

2026-11-04. Confirmed against the AWX Operator "Persisting Projects Directory" page: all five variables, their defaults, the exclusion rule and the example (rook-ceph, 20Gi). Removed the claim that the directory is non-persistent by default beyond `projects_persistence: false`, the advice on RWX storage classes across nodes, the duplicated recap paragraph, and the explicit `projects_persistence: true` requirement with an existing claim (not stated).
Method: documentation only; no commands were run.
