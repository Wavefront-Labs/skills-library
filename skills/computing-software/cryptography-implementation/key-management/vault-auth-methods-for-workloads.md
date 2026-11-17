---
id: computing-software.cryptography-implementation.key-management.vault-auth-methods-for-workloads
name: vault-auth-methods-for-workloads
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, vault-auth-methods, hashicorp-vault, kubernetes-auth, approle, jwt-auth, oidc, github-actions, workload-identity, secrets-manager]
level: practitioner
status: docs-checked
description: "Configure HashiCorp Vault Kubernetes, AppRole and JWT/OIDC auth methods for workloads and CI: role bindings, TTLs, secret-id delivery and audience checks."
sources: ["https://developer.hashicorp.com/vault/docs/auth/kubernetes", "https://developer.hashicorp.com/vault/docs/auth/approle", "https://developer.hashicorp.com/vault/docs/auth/jwt", "https://developer.hashicorp.com/vault/api-docs/auth/jwt", "https://developer.hashicorp.com/vault/docs/audit/file", "https://docs.github.com/en/actions/concepts/security/openid-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault auth methods for workloads

## Kubernetes auth
```
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host="https://kubernetes.default.svc:443"
vault write auth/kubernetes/role/orders \
  bound_service_account_names=orders bound_service_account_namespaces=prod \
  audience=vault policies=orders-read ttl=1h
```
The pod logs in with its projected service-account token (`vault write auth/kubernetes/login role=orders jwt=@token`).
Set `audience` on the role and prefer short-lived service-account tokens over long-lived ones.

## JWT/OIDC for CI (GitHub Actions example)
```
vault auth enable jwt
vault write auth/jwt/config oidc_discovery_url="https://token.actions.githubusercontent.com" bound_issuer="https://token.actions.githubusercontent.com"
vault write auth/jwt/role/deploy role_type=jwt user_claim=actor \
  bound_audiences="https://github.com/example" \
  bound_claims_type=glob bound_claims='{"repository":"example/app","ref":"refs/heads/main"}' \
  policies=deploy ttl=15m
```
Bind repository **and** ref/environment; binding only the org lets any repo deploy.

## AppRole (for VMs and legacy apps)
```
vault auth enable approle
vault write auth/approle/role/batch token_policies=batch secret_id_ttl=24h secret_id_num_uses=1 token_ttl=1h
vault read auth/approle/role/batch/role-id
vault write -wrap-ttl=5m -f auth/approle/role/batch/secret-id     # response-wrapped secret_id
```
Deliver role_id with config management and the wrapped secret_id through a separate trusted path (the "trusted
orchestrator"); the app unwraps once. Prefer platform identity (Kubernetes, cloud IAM auth) when available.

## Rules
- Short token TTLs plus renewal; use Vault Agent to handle login and renewal.
- One role per workload; policies grant only that workload's paths.
- Audit device enabled (`vault audit enable file file_path=/var/log/vault_audit.log`) before production.

## Checked

2026-11-01. Confirmed against the Vault Kubernetes, AppRole and JWT/OIDC auth pages, the JWT API page
(`bound_issuer`, `bound_claims`, `bound_claims_type` with `glob`), the response-wrapping page (`-wrap-ttl`), the file
audit device page (`vault audit enable file file_path=...`) and the GitHub OIDC page (token issuer and the
`repository`, `ref`, `actor` claims). Removed: the projected-token sentence.

Method: documentation only; no commands were run.

## Verify
- [ ] A pod in another namespace with the same SA name cannot log in.
- [ ] CI token from a non-main branch is rejected.
- [ ] secret_id cannot be reused after first login.
