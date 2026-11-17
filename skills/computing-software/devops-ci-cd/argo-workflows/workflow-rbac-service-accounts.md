---
id: computing-software.devops-ci-cd.argo-workflows.workflow-rbac-service-accounts
name: workflow-rbac-service-accounts
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-rbac, service-account, workflowtaskresults, executor-role, default-service-account]
level: intro
status: docs-checked
description: "Pick the service account for workflow pods and grant the minimum executor permissions on workflowtaskresults plus what the workflow needs."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-rbac/", "https://argo-workflows.readthedocs.io/en/latest/service-accounts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow RBAC and service accounts
All pods in a Workflow run as `spec.serviceAccountName`, or the namespace `default` service account if omitted. Argo needs the Kubernetes API for artifacts, outputs and secrets, authenticating through that account. The default account almost always has insufficient privileges. Choose one at submit time with `argo submit --serviceaccount <name>`.

Do not use `default` in production: it is shared, so it may accumulate permissions you do not want. Make a dedicated service account for the workflow and bind a Role to it with a RoleBinding.

Minimum for the executor to function:

```yaml
rules:
  - apiGroups: [argoproj.io]
    resources: [workflowtaskresults]
    verbs: [create, patch]
```

Beyond that, access depends on what the workflow does; if it deploys a resource, its account needs `create` on that resource.

For a demo only, you can give the default account admin in the current namespace:

```bash
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default -n argo
```

That grants admin only in the namespace where the binding was made, so Workflows work only there.

## Checked
2026-11-08. Confirmed against the Argo Workflows Workflow RBAC and Service Accounts pages: the service account used by workflow pods and the default fallback, `argo submit --serviceaccount`, the not-for-production warning on `default`, the minimum executor role on `workflowtaskresults`, and the demo admin rolebinding. Removed the Argo Agent role sentence, which is not on the cited pages.
Method: documentation only; no commands were run.
