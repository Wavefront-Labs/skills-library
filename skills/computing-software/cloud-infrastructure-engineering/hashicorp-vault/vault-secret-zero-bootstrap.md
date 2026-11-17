---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-secret-zero-bootstrap
name: vault-secret-zero-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, secret-zero, trusted-orchestrator, platform-identity]
level: practitioner
status: docs-checked
description: "Choose a trusted-platform identity (Kubernetes login or AppRole with response wrapping) so workloads authenticate without a pre-shared Vault secret."
sources: ["https://developer.hashicorp.com/vault/docs/auth/approle", "https://developer.hashicorp.com/vault/docs/auth/kubernetes", "https://developer.hashicorp.com/vault/docs/concepts/response-wrapping"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options for the first credential a workload presents to Vault.

Kubernetes: the pod logs in with its service account JWT against a role.

```sh
vault write auth/kubernetes/login role=demo jwt=<service account JWT>
```

AppRole: a workload needs a RoleID and a SecretID. The AppRole page describes a trusted orchestrator (a scheduler or CI system) that holds permission to fetch SecretIDs and hands the application a short-lived, response-wrapped token; the app unwraps it and logs in. Wrapped tokens are single-use, so a token already used by someone else shows interception.

```sh
vault write -f auth/approle/role/<role>/secret-id
```

- Request response wrapping with a short TTL on the SecretID call so the delivered token expires quickly.
- Limit SecretID exposure with the role fields `secret_id_num_uses` and `secret_id_ttl`.
- The RoleID can be provisioned separately from the SecretID, so neither alone is enough to log in.

## Checked
2026-11-03. Confirmed on the Kubernetes auth page (`vault write auth/kubernetes/login role=demo jwt=...`), the AppRole page (RoleID/SecretID, `secret-id` issuance, trusted orchestrator with wrapped token, `secret_id_num_uses`, `secret_id_ttl`) and the response wrapping page (single-use wrapped tokens). Removed: the `-wrap-ttl` flag example (not confirmed by these pages), the service-account file path, CIDR binding advice, the cloud-IAM comment and the Verify step.
Method: documentation only; no commands were run.
