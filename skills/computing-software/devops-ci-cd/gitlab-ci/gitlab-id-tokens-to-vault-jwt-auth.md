---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-id-tokens-to-vault-jwt-auth
name: gitlab-id-tokens-to-vault-jwt-auth
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, vault-jwt-gitlab, vault-jwt-role, bound-claims-vault, vault-login-ci]
level: advanced
status: docs-checked
description: "Configure HashiCorp Vault JWT auth for GitLab ID tokens: auth method config, roles with bound_claims and audiences, short TTLs, and reading secrets with the secrets:vault keyword."
sources: ["https://docs.gitlab.com/ci/secrets/hashicorp_vault/", "https://docs.gitlab.com/ci/secrets/hashicorp_vault_tutorial/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/secrets/hashicorp_vault.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab ID tokens to Vault (JWT auth)

Using Vault secrets in GitLab CI/CD is documented for the Premium and Ultimate tiers. ID tokens themselves are available in all tiers.

## 1. Vault config (from the docs)
```bash
vault auth enable jwt
vault write auth/jwt/config \
  oidc_discovery_url="https://gitlab.example.com" \
  bound_issuer="https://gitlab.example.com"
vault policy write myproject-production - <<EOF
path "ops/data/production/*" {
  capabilities = [ "read" ]
}
EOF
vault write auth/jwt/role/myproject-production - <<EOF
{
  "role_type": "jwt",
  "policies": ["myproject-production"],
  "token_explicit_max_ttl": 60,
  "user_claim": "user_email",
  "bound_audiences": "https://vault.example.com",
  "bound_claims_type": "glob",
  "bound_claims": {
    "project_id": "42",
    "ref_protected": "true",
    "ref_type": "tag",
    "ref": "auto-deploy-*"
  }
}
EOF
```
The `bound_issuer` for ID tokens includes `https://` (the old `CI_JOB_JWT` issuer did not). All `bound_claims` must match for login to succeed.
**Always restrict a role to a project or namespace** with a claim such as `project_id` or `namespace_id`; otherwise any JWT from this GitLab instance may be allowed to use the role.
From Vault 1.17, a role must have `bound_audiences` when the JWT contains an `aud` claim.
Other role attributes (time-to-live, IP ranges, number of uses) are in Vault's JWT auth documentation.

## 2. Job
CI/CD variables on the project: `VAULT_SERVER_URL`; optional `VAULT_AUTH_ROLE`, `VAULT_AUTH_PATH` (default `jwt`), `VAULT_NAMESPACE`.
```yaml
job_using_vault:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DATABASE_PASSWORD:
      vault: production/db/password@ops
      token: $VAULT_ID_TOKEN
```
`production/db/password@ops` means path `production/db`, field `password`, secrets engine mounted at `ops` (read from `ops/data/production/db` for KV v2, the default engine). The value is written to a temporary file and the variable holds the file path; set `file: false` to put the value in the variable itself.

## 3. Hardening
- Bind on `project_id` or `namespace_id` rather than paths where possible; claims are strings (`"true"`).
- Combine `ref_protected` with `ref_type`/`ref` for production roles, as in the example.
- Use short `token_explicit_max_ttl` values.

## Errors
- A login failure from a mismatched audience means `bound_audiences` differs from the job's `aud`.
- A failure naming a `bound_claims` claim means the job's claim (for example `ref_protected` on an unprotected ref) does not match the role.

## Verify
- [ ] A job on a protected tag reads the secret; a job on an unprotected ref is denied.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/secrets/hashicorp_vault.md, hashicorp_vault_tutorial.md and convert-to-id-tokens.md: enabling the `jwt` auth method with `oidc_discovery_url` and an `https://`-prefixed `bound_issuer`, role fields (`role_type`, `policies`, `token_explicit_max_ttl`, `user_claim`, `bound_audiences`, `bound_claims_type: glob`, `bound_claims`), the warning to restrict roles with `project_id` or `namespace_id`, the `secrets:vault` job and path format `path/field@engine-mount` (tier Premium or Ultimate), the `VAULT_*` variables, and the Vault 1.17 note that roles need `bound_audiences` when the JWT has `aud`. Removed the manual `vault write auth/.../login` flow and the Free-tier claim (GitLab documents Vault secrets as Premium and Ultimate), the image tag, `token_policies`, and the audit-log claim, none of which the GitLab docs state.

Method: documentation only; no commands were run.
