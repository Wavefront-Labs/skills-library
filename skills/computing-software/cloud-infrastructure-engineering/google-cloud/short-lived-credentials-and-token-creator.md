---
id: computing-software.cloud-infrastructure-engineering.google-cloud.short-lived-credentials-and-token-creator
name: short-lived-credentials-and-token-creator
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, impersonation, short-lived-credentials, token-creator, generate-access-token, generate-id-token, iam-credentials-api, serviceaccounttokencreator, delegation-chain, impersonated-credentials, token-lifetime, sign-jwt]
level: advanced
status: docs-checked
description: "Mint short-lived access tokens, ID tokens and signed JWTs for a service account via the IAM Credentials API, including delegated chains and the roles each hop needs."
sources: ["https://cloud.google.com/iam/docs/create-short-lived-credentials-direct", "https://cloud.google.com/iam/docs/create-short-lived-credentials-delegated", "https://cloud.google.com/iam/docs/service-account-impersonation", "https://cloud.google.com/sdk/gcloud/reference/auth/print-access-token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-lived credentials and token creator

**Goal:** every "act as this service account" need — deploy pipelines, admins debugging,
service-to-service calls — uses tokens that die within an hour, minted through IAM, instead
of a key file.

## 1. The one role that matters
`roles/iam.serviceAccountTokenCreator` **on the target service account** (not on the project)
lets a principal mint credentials *for* that SA. Grant it to a group or to the calling SA:
```bash
gcloud iam service-accounts add-iam-policy-binding deployer@<P>.iam.gserviceaccount.com \
  --member=group:gcp-platform@example.com --role=roles/iam.serviceAccountTokenCreator
```
Related roles: `roles/iam.serviceAccountOpenIdTokenCreator` creates OIDC identity tokens only;
`roles/iam.serviceAccountKeyAdmin` creates and manages keys (avoid).

## 2. Three token types
| Token | API method | Use |
|---|---|---|
| OAuth2 access token | `generateAccessToken` | call Google APIs as the SA; default maximum 1 h, up to 43,200 s (12 h) through the REST API only for service accounts listed in a policy with `constraints/iam.allowServiceAccountCredentialLifetimeExtension` |
| OpenID Connect ID token | `generateIdToken` | call Cloud Run / IAP / your own services with an `aud` |
| Signed JWT / blob | `signJwt`, `signBlob` | custom auth that needs the SA to sign without a key |
```bash
gcloud auth print-access-token --impersonate-service-account=deployer@<P>.iam.gserviceaccount.com
gcloud auth print-identity-token --impersonate-service-account=deployer@<P>.iam.gserviceaccount.com --audiences=https://api-xyz.a.run.app
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/deployer@<P>.iam.gserviceaccount.com:generateAccessToken" \
  -H 'Content-Type: application/json' -d '{"scope":["https://www.googleapis.com/auth/cloud-platform"],"lifetime":"3600s"}'
```
`gcloud auth print-access-token` has a `--lifetime` flag, but the guide states the gcloud CLI does not support setting a lifetime for impersonated tokens; use the REST API for extended lifetimes.

## 3. In code (no key anywhere)
Client libraries provide impersonated-credentials classes that take a source credential (Application Default Credentials: the human or
the runtime SA), a target principal and scopes; see the *Create short-lived credentials* guide for the per-language samples.

## 4. Delegated chains
A → B → C: A needs `tokenCreator` on B, B needs `tokenCreator` on C; call with
`"delegates": ["projects/-/serviceAccounts/B"]`. Use for "humans may impersonate the
pipeline SA, the pipeline SA may impersonate per-environment deployers" — humans never get
direct rights on prod deployers. Keep chains short; each hop needs its own grant.

## 5. Audit
Alert on token generation for sensitive SAs from unexpected principals; check the IAM audit logging docs for which calls are logged by default.

## Gotchas
- `tokenCreator` on the **project** level grants minting for every SA in the project, including service agents; grant on the SA resource.
- One hour is the default maximum; longer lifetimes need the org policy constraint above and the REST API.
- Tokens are bearer tokens; do not log them. `print-access-token` into shell history is a common leak.

## Verify
- [ ] `gcloud auth print-access-token --impersonate-service-account=<SA>` succeeds for the group and fails for a non-member.
- [ ] No SA key exists for the SA (`keys list --managed-by=user` empty).

## Checked

- Date: 2026-10-27
- Confirmed against the IAM short-lived credentials guides (token creator role on the target SA, CLI cannot set a lifetime, `delegates` for delegated requests), the Restricting service accounts page (`iam.allowServiceAccountCredentialLifetimeExtension`, up to 43,200 seconds via REST), the IAM Credentials API v1 discovery document (`generateAccessToken` with `scope`, `lifetime`, `delegates`; `generateIdToken`, `signJwt`, `signBlob`), the roles reference (`serviceAccountTokenCreator`, `serviceAccountOpenIdTokenCreator`, `serviceAccountKeyAdmin`) and the gcloud references for `auth print-access-token` (`--lifetime`) and `auth print-identity-token` (`--audiences`, `--include-email`).
- Removed: the Python snippet, `gcloud config set auth/impersonate_service_account` and Terraform lines, audit-log field and Data Access claims, quota-project, disabled-SA and `INVALID_ARGUMENT` claims, signed-URL use case and the two-hop rule.

Method: documentation only; no commands were run.
