---
id: computing-software.devops-ci-cd.concourse-ci.vault-authentication-backends
name: vault-authentication-backends
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [vault, authentication, approle, userpass, cert, periodic-token, token-renewal, credential-manager]
level: advanced
status: docs-checked
description: "Authenticate the Concourse web node to Vault: periodic token, userpass, approle and cert backends, token TTL and period behaviour, and why token_num_uses should not be set."
sources:
  - https://concourse-ci.org/docs/operation/creds/vault/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The web node can authenticate with a token or any auth backend plus params. Once it has a token it renews continuously, at half the token's lease duration.

**Periodic token** is simplest: `vault token create --policy concourse --period 1h`, then `CONCOURSE_VAULT_CLIENT_TOKEN=...`. The timer starts at creation, so choose a period that covers planned web downtime. Its flaw: if the web node is down longer than the period, the token expires and must be recreated. Use approle to avoid this.

**userpass**: create a user with `vault write auth/userpass/users/concourse policies=concourse period=1h password=...`, then set `CONCOURSE_VAULT_AUTH_BACKEND="userpass"` and `CONCOURSE_VAULT_AUTH_PARAM="username:concourse,password:..."`.

**approle**: `vault write auth/approle/role/concourse policies=concourse period=1h`, read the `role-id`, generate a `secret-id`, then `CONCOURSE_VAULT_AUTH_BACKEND="approle"` and `CONCOURSE_VAULT_AUTH_PARAM="role_id:...,secret_id:..."`. Only set `secret_id_ttl` or `secret_id_num_uses` if something periodically regenerates secret IDs and reconfigures web nodes.

**cert**: Vault must use TLS. `vault write auth/cert/certs/concourse policies=concourse certificate=@out/vault-ca.crt ttl=1h`, then `CONCOURSE_VAULT_AUTH_BACKEND="cert"`, `CONCOURSE_VAULT_CLIENT_CERT` and `CONCOURSE_VAULT_CLIENT_KEY`. No auth params are needed; Vault checks the cert against all roles.

For all: `policies` must include one with access to the secrets path. If you set a `token_max_ttl` (`max_ttl` for cert), set the same value as `CONCOURSE_VAULT_AUTH_BACKEND_MAX_TTL` so the web node re-authenticates in time. `period` makes tokens periodic and renewable forever, so setting both period and max TTL is pointless. Setting `token_num_uses` is not recommended: the web node does not re-acquire a token when the limit is reached.

## Checked

2026-11-04. All four methods, parameters and cautions confirmed on the Vault credential manager page, Configuring Authentication.

Method: documentation only; no commands were run.
