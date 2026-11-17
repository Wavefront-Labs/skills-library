---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-kubernetes-auth
name: vault-kubernetes-auth
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, kubernetes-auth, service-account, tokenreview]
level: practitioner
status: docs-checked
description: "Enable Vault Kubernetes auth with host config, bound service accounts and namespaces, TokenReview RBAC and short-lived token handling."
sources: ["https://developer.hashicorp.com/vault/docs/auth/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pods log in with their service account JWT; Vault verifies it with the Kubernetes TokenReview API.

```sh
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host="https://kubernetes.default.svc"
vault write auth/kubernetes/role/web \
  bound_service_account_names=web \
  bound_service_account_namespaces=shop \
  policies=web ttl=1h
vault write auth/kubernetes/login role=web jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
```

Gotchas: on Vault 1.9.3 and later, running inside the cluster you can omit the reviewer JWT and CA so Vault uses its local token; earlier versions read the token and CA once and stored them, so auth failed when the token expired or was revoked. The service account used for TokenReview needs the `system:auth-delegator` ClusterRole. Since Vault 1.9.0 `disable_iss_validation` and `issuer` are deprecated and new mounts default to `disable_iss_validation=true`; if you upgrade to Kubernetes 1.21+ make sure it is `true` (check with `vault read -field disable_iss_validation auth/kubernetes/config`).

## Checked

2026-11-03. Confirmed on the Kubernetes auth method page: `vault auth enable kubernetes`, `auth/kubernetes/config` with `kubernetes_host`, role fields `bound_service_account_names`, `bound_service_account_namespaces`, `policies`, `ttl`, the login with the pod JWT, the 1.9.3 local-token behaviour, `system:auth-delegator`, and the `disable_iss_validation` history. Removed: the wildcard claim, short-ttl and one-role-per-workload advice, and the invented Verify step.

Method: documentation only; no commands were run.
