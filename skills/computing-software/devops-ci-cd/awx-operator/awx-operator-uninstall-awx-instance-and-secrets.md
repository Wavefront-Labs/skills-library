---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-uninstall-awx-instance-and-secrets
name: awx-operator-uninstall-awx-instance-and-secrets
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, uninstall, delete, garbage-collect, secrets, pvc, recovery]
level: practitioner
status: docs-checked
description: "Remove an AWX instance by deleting its AWX resource, and understand what persists afterwards."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/uninstall/uninstall.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator uninstall awx instance and secrets

To uninstall an AWX deployment, delete the AWX custom resource for it:

```sh
kubectl delete awx awx-demo
awx.awx.ansible.com "awx-demo" deleted
```

Deleting the AWX instance removes all related deployments and statefulsets, but persistent volumes and secrets remain. To enforce secrets also being removed, use `garbage_collect_secrets: true`.

If you ever intend to recover an AWX from an existing database, keep a copy of the secrets: a successful recovery needs them.

## Checked

2026-11-04. Confirmed against the AWX Operator "Uninstall" page: the delete command, what is removed and what remains, `garbage_collect_secrets: true`, and the secrets note. Removed the closing paragraph (AWXBackup/AWXRestore, namespace deletion advice) and the explanation of why secrets are needed, which the page does not give.
Method: documentation only; no commands were run.
