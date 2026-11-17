---
id: computing-software.devops-ci-cd.helm.rbac-and-security
name: rbac-and-security
category: computing-software
field: devops-ci-cd
product: helm
tags: [rbac, service-account, permissions, namespace, secrets, least-privilege, role-binding]
level: advanced
status: docs-checked
description: "Kubernetes RBAC for Helm users: default ClusterRoles, the secret-reader pattern for helm list, and chart rbac.create conventions."
sources:
  - "https://helm.sh/docs/topics/rbac/"
  - "https://helm.sh/docs/chart_best_practices/rbac/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Kubernetes RBAC is on by default (from Kubernetes 1.6). Normal users are managed outside the cluster; service accounts are managed by the Kubernetes API, bound to a namespace. Roles and RoleBindings are namespaced; ClusterRoles and ClusterRoleBindings are cluster-wide. A ClusterRole can be bound to one namespace through a RoleBinding.

Default user-facing ClusterRoles:

- `cluster-admin`: super-user on every resource. In a RoleBinding it gives full control of that namespace, including the namespace itself.
- `admin`: read/write on most resources in a namespace, including creating roles and rolebindings; not write access to resource quota or the namespace. Use it if your charts create Roles and RoleBindings.
- `edit`: read/write on most objects in a namespace, no viewing or modifying roles or rolebindings.
- `view`: read-only on most objects, not roles, rolebindings or secrets.

What Helm users need:

- Helm stores release metadata as Secrets by default, and `view` does not grant reading Secrets. To run `helm list` a user needs a custom ClusterRole such as `secret-reader` (verbs `get`, `watch`, `list` on `secrets`) bound alongside `view`.
- `helm list --all-namespaces` needs cluster-scope read access, so bind `view` and `secret-reader` with ClusterRoleBindings.
- Installing a chart that creates cluster-scope resources (namespaces, roles, CRDs) needs cluster-scope write access: `admin` or `cluster-admin`. The guide recommends considering `admin` or a custom ClusterRole tailored to the user instead of `cluster-admin`, which includes node access such as `kubectl drain`.

Chart authoring guidance (RBAC best practices): keep RBAC and ServiceAccount configuration under separate values keys, `rbac.create` (boolean, default `true`) and `serviceAccount.create` / `serviceAccount.name`. If the name is unset and create is true, generate it from the `fullname` template; if create is false and no name is set, the `default` ServiceAccount is used. The guide supplies a `mychart.serviceAccountName` helper template for this.

## Checked

2026-11-08. Read the Role-based Access Control topic and RBAC best-practices pages in full. Rewrote the body: the previous minimum-rights list, hook and lookup rights and secrets hygiene advice were not in the sources and were removed; added the documented default ClusterRoles, secret-reader pattern and rbac.create/serviceAccount conventions.

Method: documentation only; no commands were run.
