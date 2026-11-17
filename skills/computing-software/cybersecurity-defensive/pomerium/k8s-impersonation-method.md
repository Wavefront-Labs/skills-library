---
id: computing-software.cybersecurity-defensive.pomerium.k8s-impersonation-method
name: k8s-impersonation-method
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [kubernetes-api, user-impersonation, clusterrole, kubernetes-service-account-token, rbac]
level: advanced
status: docs-checked
description: "Proxy the Kubernetes API server through Pomerium using a service account with impersonate permissions so IdP users and groups drive RBAC."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/kubernetes-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium can front the Kubernetes API server for centralised IdP authentication, group support, dynamic policy and an audit trail without a VPN. This is one of two methods; the other is the Pomerium JWT (Kubernetes 1.30+, see k8s-pomerium-jwt-method).

1. Give Pomerium a service account with `impersonate` permissions. The docs' ClusterRole `pomerium-impersonation` grants `impersonate` on `users` and on `groups`, with `resourceNames` limited to `group1`, `group2`, `group3`.
2. Create a route policy for the API server using the service account token (the `kubernetes-service-account-token` route reference).
3. Write RoleBindings against IdP `User` and `Group` subjects.
4. Users connect with `pomerium-cli` as an auth provider in `~/.kube/config` (see k8s-kubeconfig-exec-plugin).
5. Pomerium authorizes each request and passes the user identity to the API server for RBAC.

The docs note that the supported groups can be explicitly listed in the RBAC definition.

## Checked

2026-11-04. Confirmed against the Kubernetes Access page: ClusterRole, route policy, RoleBindings, pomerium-cli, flow. Replaced an unstated managed-cluster claim and an unstated restriction advice.

Method: documentation only; no commands were run.
