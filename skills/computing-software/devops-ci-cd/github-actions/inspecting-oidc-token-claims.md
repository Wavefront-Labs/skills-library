---
id: computing-software.devops-ci-cd.github-actions.inspecting-oidc-token-claims
name: inspecting-oidc-token-claims
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, oidc-claims-debug, jwt-decode-oidc, actions-id-token-request-url, id-token-audience, sub-claim, repository-claim, environment-claim, ref-claim, job-workflow-ref, trust-policy-mismatch, not-authorized-to-perform-sts-assumerolewithwebidentity, oidc-debugging, oidc, openid-connect]
level: practitioner
status: docs-checked
description: "Request and decode the raw OIDC token, then map sub/ref/environment/job_workflow_ref claims to the cloud trust policy to fix AssumeRoleWithWebIdentity denials fast."
sources: ["https://docs.github.com/en/actions/reference/security/oidc", "https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting OIDC token claims

**Goal:** see exactly what the cloud provider sees, so the trust condition matches the
token instead of guessing.

## 1. Fetch the token in a step
```yaml
permissions: { id-token: write, contents: read }
steps:
  - name: Request OIDC token
    run: |
      curl -sS -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
        "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=api://AzureADTokenExchange"
```
`ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN` are the documented request variables, and the job
needs `id-token: write` to request a token (without it the JWT cannot be requested). The `audience` query
parameter sets `aud`; by default `aud` is the URL of the repository owner. Use the value your provider expects
(`sts.amazonaws.com` for the official AWS action, `api://AzureADTokenExchange` recommended for Azure). The response
is a JWT: decode its payload with a trusted JWT decoder and do not leave a debugging step in production workflows.

## 2. Claims that trust policies key on
| claim | description (from the OIDC reference) |
|---|---|
| `sub` | the subject validated by the cloud; the default shape is `repo:ORG/REPO:ref:refs/heads/BRANCH`, `repo:ORG/REPO:environment:NAME` or `repo:ORG/REPO:pull_request` (the `pull_request` form only when the job has no environment); repositories using immutable subject claims have `OWNER@OWNER-ID/REPO@REPO-ID` in the repo segment |
| `repository`, `repository_owner`, `repository_id`, `repository_owner_id`, `repository_visibility` | where the workflow runs (visibility: internal, private or public) |
| `ref`, `ref_type`, `base_ref`, `head_ref` | the git ref and pull request branches |
| `environment` | the job's environment (required if the claim is included via include_claim_keys) |
| `job_workflow_ref`, `job_workflow_sha` | the called reusable workflow path and commit |
| `workflow`, `workflow_ref`, `workflow_sha` | the workflow name, file ref and SHA |
| `actor`, `actor_id` | who initiated the run |
| `event_name` | the triggering event |
| `run_id`, `run_number`, `run_attempt` | run identifiers |
| `runner_environment` | `github-hosted` or `self-hosted` |
| `aud` | audience (default: the repository owner URL) |
| `iss` | `https://token.actions.githubusercontent.com` (GHES: `https://HOSTNAME/_services/token`) |

## 3. Match it to the provider
- **AWS**: conditions on `token.actions.githubusercontent.com:aud` (`sts.amazonaws.com` with the official action) and
  on `:sub`, using `StringEquals` or `StringLike` with `*` wildcards.
- **Azure**: audience `api://AzureADTokenExchange` is recommended.
- **Vault**: `bound_claims` on any claim, optionally `bound_subject` and `bound_audiences`.
- The OIDC discovery document is at `https://token.actions.githubusercontent.com/.well-known/openid-configuration`.

## 4. Customising sub
A repository or organisation template (REST API, `include_claim_keys`, `use_default`) changes the `sub` format, for
example to include `job_workflow_ref`. Every trust policy then needs updating; inspect the token again after any change.
For repositories created after July 15, 2026 (or opted in), the default `sub` includes owner and repository IDs.

## 5. Gotchas
- A `sub` for a job that uses an environment carries the environment name instead of the ref.
- A policy pinned to `ref:refs/heads/main` will not match a `pull_request` subject.

## Verify
- [ ] Decoded `sub`/`aud`/`iss` printed and match the provider condition string-for-string.
- [ ] After fixing the policy, the real auth step succeeds and the dump step is removed.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23.
- Request variables ACTIONS_ID_TOKEN_REQUEST_URL and ACTIONS_ID_TOKEN_REQUEST_TOKEN, the audience query parameter, id-token write requirement, default aud: confirmed in the OIDC reference.
- Claim names and descriptions, issuer values (including GHES), the pull_request and environment sub forms, immutable subject claims after July 15, 2026: confirmed in the OIDC reference.
- AWS aud and wildcard conditions, Azure audience, Vault bound_claims: confirmed in the per-provider pages.
- Removed the jq and base64 decoding pipeline, GCP mapping, Azure issuer and subject mapping detail, the fork id-token claim and the token lifetime remark, which no fetched page documents.

Method: documentation only; no commands were run.
