---
id: computing-software.devops-ci-cd.gitlab-ci.id-token-claims-and-bound-claims
name: id-token-claims-and-bound-claims
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, id-token-claims, bound-claims, id-tokens-keyword, oidc-claims-reference, decode-id-token]
level: practitioner
status: docs-checked
description: "Know the claims in GitLab ID tokens (sub, project_path, ref_protected, environment, runner_environment...) to write tight trust conditions; decode tokens to debug."
sources: ["https://docs.gitlab.com/ci/secrets/id_token_authentication/", "https://docs.gitlab.com/ci/yaml/#id_tokens", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/secrets/id_token_authentication.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ID token claims and bound claims

## 1. Requesting tokens
```yaml
job:
  id_tokens:
    VAULT_TOKEN_JWT: { aud: https://vault.example.com }
    MULTI_AUD: { aud: [https://gcp.example.com, https://aws.example.com] }
```
Each entry becomes a variable holding a signed JWT (RS256). `aud` accepts a string, an array of strings or a CI/CD variable. `iss` is the domain of the GitLab instance; the public keys are served at `<gitlab>/oauth/discovery/keys`. A job-level `id_tokens` replaces `default:id_tokens` (no merge). The token expires at the job timeout if one is set, otherwise after 5 minutes.

## 2. Claims worth binding
| Claim | Meaning |
|---|---|
| `sub` | default `project_path:{group}/{project}:ref_type:{type}:ref:{branch_name}`; configurable per project |
| `project_id`, `project_path` | project running the job (source project in a merge request pipeline) |
| `namespace_id`, `namespace_path` | namespace of that project |
| `job_project_id`, `job_project_path`, `job_namespace_id`, `job_namespace_path` | scoping claims introduced in GitLab 18.4 |
| `ref`, `ref_type`, `ref_path` | Git ref (source branch in an MR pipeline); `branch` or `tag`; for example `refs/heads/main` |
| `ref_protected` | `true` if the ref is protected |
| `environment`, `environment_protected`, `deployment_tier`, `environment_action` | present only when the job specifies an environment |
| `pipeline_source` | pipeline source, such as `push` |
| `user_id`, `user_login`, `user_email`, `user_access_level` | user executing the job |
| `runner_environment` | `gitlab-hosted` or `self-hosted` |
| `ci_config_ref_uri`, `ci_config_sha` | top-level pipeline definition ref and SHA; `null` unless the definition is in the same project |
| `project_visibility` | `internal`, `private` or `public` |
| `job_id`, `pipeline_id`, `sha` | job, pipeline and commit identifiers |

## 3. Decode to debug
```bash
echo $OIDC_TOKEN | cut -d '.' -f2 | base64 -d | jq .
```
This is the command in the GitLab docs. Do it only in a throwaway job: the token is a credential until it expires.

## 4. Rules of thumb
- Prefer stable identifiers: `project_id` and `namespace_id` alongside `sub`. The docs advise against relying on `user_login` or `user_email` alone because users can change them.
- Bind `ref_protected` and `environment` for production roles.
- Use a specific `aud` per relying party so one service cannot accept a token meant for another.
- GitLab blocks token issuance if the configured `sub` contains a project path previously used by a different project; the fix is `ci_id_token_sub_claim_components` via the projects API with an ID component first.

## Verify
- [ ] Decoded claims match each provider's conditions; a token from an unprotected ref fails the production binding.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/secrets/id_token_authentication.md and doc/ci/yaml/_index.md: `id_tokens` with `aud` as a string, array or CI/CD variable, the claim list and their meanings (including `ref_path`, `ref_protected`, `environment`, `environment_protected`, `deployment_tier`, `pipeline_source`, `runner_environment`, `ci_config_ref_uri`, `ci_config_sha`, `job_id`, `pipeline_id`, `sha`, and `job_project_id` and related claims from GitLab 18.4), claims are emitted as strings in the sample payload, RS256 signing, expiry (job timeout if set, otherwise 5 minutes), the decode command, and the keys endpoint `/oauth/discovery/keys` (AWS page). Removed the `main-fix` glob example, the `tr` base64url padding advice and the Developer-role branch-name example, which no page states.

Method: documentation only; no commands were run.
