---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-profiles-namespaces
name: kubeflow-profiles-namespaces
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [profiles, profile-controller, cd-registration-flow, resourcequota, namespace-isolation]
level: practitioner
status: docs-checked
description: "Kubeflow Profiles: the CRD that wraps a namespace, the RBAC and Istio resources created per profile, automatic profile creation, and creating or deleting a Profile."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/central-dash/profiles.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Profiles namespaces

A Profile is a Kubernetes CRD wrapping a Namespace of the same name. It has one owner and any number of contributors with view or modify access. The Profile Controller reconciles profiles and namespaces. Users see only profiles where they are owner, contributor (read and write) or viewer (read); the active profile is chosen in the top bar dropdown.

Automatic creation: set `CD_REGISTRATION_FLOW=true` on the central-dashboard Deployment so first-time users are prompted to create a profile. It is disabled by default. Those users become owners and can manage contributors, so admins often disable it and create profiles manually, granting users only view or modify access.

Created per profile:
- Namespace.
- RoleBinding `namespaceAdmin` to `ClusterRole/kubeflow-admin` for the owner; per contributor `user-{EMAIL}-clusterrole-{ROLE}` to `kubeflow-edit` or `kubeflow-view`.
- RoleBindings `default-editor` (to ClusterRole/kubeflow-edit) for ServiceAccount default-editor and `default-viewer` (to ClusterRole/kubeflow-view) for ServiceAccount default-viewer.
- Istio AuthorizationPolicies: `ns-owner-access-istio` for the owner and `user-{EMAIL}-clusterrole-{ROLE}` per contributor.

Create a profile with `kubectl apply` on:

```yaml
apiVersion: kubeflow.org/v1
kind: Profile
metadata:
  name: my-profile   # becomes the namespace; avoid existing namespaces
spec:
  owner:
    kind: User
    name: admin@example.com
  plugins: []
  resourceQuotaSpec: {}
```

Use `kubectl get profiles`, `kubectl describe profile NAME`, `kubectl delete profile NAME`. Deleting a profile deletes its namespace and every resource in it. The page notes unexpected behaviour may occur if the namespace already exists, and that `plugins` and `resourceQuotaSpec` are optional (a ResourceQuota is created from `resourceQuotaSpec`).

## Checked

2026-11-08. Confirmed against the Profiles and Namespaces page: what a Profile is, visibility rules, CD_REGISTRATION_FLOW behaviour and its warning, the per-profile resources and names, the example Profile and the kubectl commands. Contributors are managed with KFAM per the page.
Method: docs-only read of cited pages, 2026-11-08
