---
id: computing-software.devops-ci-cd.argo-cd.ignore-differences-by-managed-fields-managers
name: ignore-differences-by-managed-fields-managers
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, managed-fields-managers, field-manager-ignore, server-side-apply-drift]
level: advanced
status: docs-checked
description: "Ignore drift written by specific controllers in Argo CD using managedFieldsManagers, based on Kubernetes server-side apply field ownership, at app or system level."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ignoreDifferences by managedFieldsManagers

Instead of listing paths, ignore **any field owned by a given field manager** in `metadata.managedFields`.

## 1. Find the manager
```bash
kubectl get deploy api -n app --show-managed-fields -o yaml     # read metadata.managedFields[].manager
```

## 2. App level
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      managedFieldsManagers:
        - kube-controller-manager
        - rollouts-controller
```

## 3. System level (`argocd-cm`)
```yaml
data:
  resource.customizations.ignoreDifferences.apps_Deployment: |
    managedFieldsManagers:
      - kube-controller-manager
```

## 4. How it works / limits
- Differences in fields owned by a listed manager (`metadata.managedFields[].manager`) are ignored.
- The app-level form can match every resource with `group: '*'` and `kind: '*'` to ignore all fields owned by a manager across the application.
- Ignoring a manager that humans use (for example a `kubectl` manager) would hide manual changes: list only controller managers.

## Verify
- [ ] After the controller changes a field it owns, the app remains Synced; a change to a field owned by another manager still shows drift.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `managedFieldsManagers` at application level (including `group: '*'`/`kind: '*'`) and in `resource.customizations.ignoreDifferences.apps_Deployment` against the diffing page. Removed the yq pipeline, example manager names, and unconfirmed ownership and server-side-apply remarks.

Method: documentation only; no commands were run.
