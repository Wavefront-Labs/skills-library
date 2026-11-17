---
id: computing-software.cybersecurity-defensive.pomerium.k8s-rbac-bind-pomerium-users
name: k8s-rbac-bind-pomerium-users
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [rolebinding, kubectl-auth, forbidden-error, rbac-subjects, whoami]
level: practitioner
status: docs-checked
description: "Grant Kubernetes RBAC to users who authenticate through Pomerium, and diagnose Forbidden errors with kubectl auth whoami and can-i."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/kubernetes-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without bindings, requests fail with `Forbidden` for the user, e.g. `User "foo@example.com" cannot list resource "pods"`.

Diagnose:
- `kubectl auth whoami` shows the username and groups (e.g. `system:authenticated`).
- `kubectl auth can-i list pods` returns `no` until access is granted.

Fix: create a Role and a RoleBinding whose subject is the Pomerium user. The docs' example:
- Role `example-role` granting `get`, `list`, `watch` on `pods`.
- RoleBinding `example-role-binding` with subject kind `User` and name `foo@example.com`.

After that `can-i` returns `yes`.

`kubectl auth whoami` shows the user and group names as set by Pomerium; bind that username. See k8s-pomerium-jwt-method and k8s-impersonation-method.

## Checked

2026-11-04. Confirmed against the Kubernetes Access page: Forbidden example, whoami, can-i, Role and RoleBinding. Replaced an inferred identity-mapping paragraph.

Method: documentation only; no commands were run.
