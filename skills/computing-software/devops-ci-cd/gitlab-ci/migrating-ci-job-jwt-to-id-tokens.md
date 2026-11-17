---
id: computing-software.devops-ci-cd.gitlab-ci.migrating-ci-job-jwt-to-id-tokens
name: migrating-ci-job-jwt-to-id-tokens
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-job-jwt-migration, id-tokens, vault-jwt-gitlab]
level: practitioner
status: docs-checked
description: "Replace removed CI_JOB_JWT / CI_JOB_JWT_V2 with id_tokens in GitLab CI: per-relying-party aud, Vault role bound_audiences, AWS/GCP trust updates and rollout order."
sources: ["https://docs.gitlab.com/ci/secrets/convert-to-id-tokens/", "https://docs.gitlab.com/ci/secrets/id_token_authentication/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/secrets/convert-to-id-tokens.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from CI_JOB_JWT to id_tokens

`CI_JOB_JWT_V2` was removed in GitLab 17.0 and the `CI_JOB_JWT` variables are deprecated; use ID tokens (`id_tokens:`) instead. The Vault migration tutorial in the GitLab docs applies to Premium and Ultimate.

## Changes per consumer
| Consumer | Change |
|---|---|
| Vault | declare `id_tokens: VAULT_ID_TOKEN: { aud: https://vault.example.com }` and set `bound_audiences` on the role; update `bound_issuer` to include `https://` |
| `secrets:` keyword (Vault) | when a job has at least one ID token, `secrets` uses it automatically; or name it with `token: $VAULT_ID_TOKEN` |
| AWS | use an ID token with an `aud` that matches the IAM OIDC provider audience (the docs suggest `sts.amazonaws.com` or the GitLab URL) |
| GCP, Azure | the job's `aud` must match the provider's allowed audiences or the federated credential's audience |

## Vault: two documented approaches
1. **New auth path.** Update `bound_issuer` to `https://gitlab.example.com` on the existing path (jobs using `CI_JOB_JWT` then start to fail), or leave it and create a parallel method for ID tokens:
```bash
vault auth enable -path jwt_v2 jwt
vault write auth/jwt_v2/config \
  oidc_discovery_url="https://gitlab.example.com" \
  bound_issuer="https://gitlab.example.com"
```
Roles are bound to an auth path, so recreate each role under `auth/jwt_v2/role/<name>` with `bound_audiences` set (it is mandatory when the JWT has an `aud` claim); do not change `role_type`. Then switch jobs to `VAULT_AUTH_PATH=jwt_v2`.
2. **Role-level issuer.** Keep one auth path and add an `iss` list to each role's `bound_claims`, accepting both the `https://` form and the old bare hostname, then remove `bound_issuer` from the auth method:
```json
"bound_claims": { "iss": ["https://gitlab.example.com", "gitlab.example.com"], "project_id": "22", "ref": "master", "ref_type": "branch" }
```
From Vault 1.17, JWT login requires `bound_audiences` on the role when the JWT contains `aud` (single string or list).

## Rollout
1. Add `bound_audiences` and the issuer changes to roles.
2. Update pipelines to `id_tokens` project by project.
3. Retire the old roles or auth path when no job uses `CI_JOB_JWT`.

## Verify
- [ ] A job with `id_tokens` authenticates; a token with a different `aud` is rejected by the role.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/secrets/convert-to-id-tokens.md and the AWS, Azure and Google Cloud pages: `CI_JOB_JWT_V2` was removed in GitLab 17.0 and the `CI_JOB_JWT` variables are deprecated, `bound_issuer` must include `https://` for ID tokens, two migration paths (a second auth path such as `jwt_v2` with recreated roles, or a role-level `bound_claims` `iss` list holding both issuer forms), role fields in the new-path example, and `bound_audiences` being mandatory when the JWT has `aud` (Vault 1.17 and later). Removed the claim that jobs now see an empty variable and the quoted error strings, the table of AWS and GCP audiences beyond what those pages say, and the grep step.

Method: documentation only; no commands were run.
