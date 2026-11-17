---
id: computing-software.devops-ci-cd.concourse-ci.vault-credential-manager
name: vault-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [vault, credential-manager, kv, secrets-engine, lookup-templates, shared-path, namespace, policy]
level: practitioner
status: docs-checked
description: "Configure Vault as the credential manager: URL and CA, kv or kv_v2 engine at /concourse, read policy, KV mount cache, lookup order, shared path, templates, prefix, namespace."
sources:
  - https://concourse-ci.org/docs/operation/creds/vault/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `CONCOURSE_VAULT_URL=https://vault.example.com:8200` on the web node, plus `CONCOURSE_VAULT_CA_CERT` for a local CA. Concourse supports a single path and so one secrets engine, `kv` or `kv_v2`; v2 adds versioned secrets, and Concourse always reads the latest version, so a deleted secret looks nonexistent.

```shell
vault secrets enable -version=1 -path=concourse kv
vault policy write concourse ./concourse-policy.hcl
```

with a policy `path "concourse/*" { capabilities = ["read"] }` that matches your path prefix. `CONCOURSE_VAULT_ENABLE_KV_MOUNT_CACHE=true` caches the KV mount version (v1 or v2) per lookup instead of querying Vault every time.

**Lookup.** `((foo))` is searched at `/concourse/TEAM_NAME/PIPELINE_NAME/foo`, then `/concourse/TEAM_NAME/foo`. Secrets are key-value; the default field is `value`, and `((foo.bar))` picks another. Deeper paths use `/` as in `((foo/bar/baz.qux))`. A one-off task has no pipeline, so only the team path is searched.

**Customising.**
- `CONCOURSE_VAULT_SHARED_PATH=some-shared-path` for credentials common to all teams (under the prefix; use with care).
- `CONCOURSE_VAULT_LOOKUP_TEMPLATES` with `{{.Team}}`, `{{.Pipeline}}`, `{{.Secret}}`. With prefix `/secrets` and templates `/{{.Team}}/concourse/{{.Pipeline}}/{{.Secret}},/{{.Team}}/concourse/{{.Secret}},/common/{{.Secret}}`, `((password))` for `myteam`/`mypipeline` resolves `/secrets/myteam/concourse/mypipeline/password`, then `/secrets/myteam/concourse/password`, then `/secrets/common/password`.
- `CONCOURSE_VAULT_PATH_PREFIX` replaces `/concourse`.
- `CONCOURSE_VAULT_NAMESPACE` for Vault Enterprise; applies to all teams.

## Checked

2026-11-04. Configuration, policy, lookup rules and examples confirmed on the Vault credential manager page.

Method: documentation only; no commands were run.
