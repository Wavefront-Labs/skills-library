---
id: computing-software.devops-ci-cd.argo-workflows.managed-namespace
name: managed-namespace
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [managed-namespace, namespaced-install, cluster-scoped, roles, executor-image]
level: practitioner
status: docs-checked
description: "Install Argo Workflows namespace scoped with --namespaced and optionally run Workflows in another namespace with --managed-namespace."
sources: ["https://argo-workflows.readthedocs.io/en/latest/managed-namespace/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespaced and managed namespace installs
Argo can be cluster scoped (ClusterRoles) or namespace scoped (Roles).

Namespace scoped: start both the Workflow Controller and the Argo Server with `--namespaced`. To run Workflows in a different namespace add `--managed-namespace`. Cluster scoped installs omit both flags.

```yaml
args:
  - --configmap
  - workflow-controller-configmap
  - --executor-image
  - quay.io/argoproj/argoexec:v4.1.5
  - --namespaced
  - --managed-namespace
  - default
```

Either way an admin must install it, since the CRDs are cluster-scoped objects.

Use case: a managed namespace lets some users or services run Workflows without privileges in the namespace where Argo is installed. If the same team maintains Argo and all the CI/CD Workflows, a plain namespace install may do. If a separate data science team runs the Workflows, give them a namespace such as `data-science-workflows` and install Argo elsewhere with that as the managed namespace. The security page adds that the managed namespace should not be the controller's own namespace, because users who can create Workflows there might modify the controller.

## Checked
2026-11-03. Confirmed against the Argo Workflows Managed Namespace page (scoping, flags, example args, admin install requirement, use case) and the Security page (managed namespace warning). Nothing removed.
Method: documentation only; no commands were run.
