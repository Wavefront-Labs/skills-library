---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-oidc-to-gcp-workload-identity
name: gitlab-oidc-to-gcp-workload-identity
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-gcp-workload-identity, workload-identity-federation-gitlab, gcloud-cred-config]
level: advanced
status: docs-checked
description: "Authenticate GitLab CI to Google Cloud via Workload Identity Federation: pool, provider attribute mapping and conditions, id_tokens audience, STS token exchange."
sources: ["https://docs.gitlab.com/ci/cloud_services/google_cloud/", "https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/cloud_services/google_cloud/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab ID tokens to GCP Workload Identity

## 1. Google Cloud setup
You need at least the workload identity pool Admin permission on the project.
- **Pool**: one pool per GitLab installation per Google Cloud project; different repositories can use different providers in the same pool. Keep the pool enabled.
- **Provider**: type OpenID Connect. **Issuer (URL)**: your GitLab address with `https://` and a **trailing slash**, for example `https://gitlab.com/`. **Audiences**: set manually to your GitLab address with `https://` and **no** trailing slash, for example `https://gitlab.com`.
- **Attribute mapping**: `google.subject` = `assertion.sub`, and `attribute.X` = `assertion.X` for every claim you want to use in permissions (for example `attribute.user_login` = `assertion.user_login`). CEL expressions can build complex attributes.
- For projects on GitLab.com, Google requires limiting access to tokens issued by your GitLab group (an attribute condition).

Grant permissions through service account impersonation:
1. Create a service account and grant it the IAM roles the job needs (for example `roles/storage.objectCreator` on a bucket).
2. Grant the external identity `roles/iam.workloadIdentityUser` on that service account. External identities use the `principalSet://` format:
```text
principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/attribute.user_login/chris
```
`PROJECT_NUMBER` is the project number and `POOL_ID` the pool ID (not its name). The attribute used (here `user_login`) must be mapped in the provider.

## 2. Job
```yaml
job:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.example.com     # must be in the provider's allowed audiences
```
Exchange the ID token for a federated token with the Security Token Service, then impersonate the service account (flow from the docs):
```bash
PAYLOAD="$(cat <<EOF
{
  "audience": "//iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID",
  "grantType": "urn:ietf:params:oauth:grant-type:token-exchange",
  "requestedTokenType": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "https://www.googleapis.com/auth/cloud-platform",
  "subjectTokenType": "urn:ietf:params:oauth:token-type:jwt",
  "subjectToken": "${GITLAB_OIDC_TOKEN}"
}
EOF
)"
curl --fail "https://sts.googleapis.com/v1/token" --header "Accept: application/json" \
  --header "Content-Type: application/json" --data "${PAYLOAD}"        # response field: access_token
```
Then call `https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/SERVICE_ACCOUNT_EMAIL:generateAccessToken`
with `Authorization: Bearer <federated token>` and body `{"scope": ["https://www.googleapis.com/auth/cloud-platform"]}`; the response carries the service account access token.

## Verify
- [ ] The token exchange returns an access token for a job from the allowed group, and fails for a project outside it.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/cloud_services/google_cloud/_index.md: pool and provider options (OIDC provider type, issuer with `https://` and a trailing slash, allowed audiences with `https://` and no trailing slash, attribute mapping `google.subject` to `assertion.sub` and `attribute.X` to `assertion.X`), the warning that GitLab.com projects must be limited to tokens from your group, service account impersonation with `roles/iam.workloadIdentityUser` and the `principalSet://` format, and the STS token exchange and `generateAccessToken` calls. Replaced the gcloud commands, google/cloud-sdk image, `create-cred-config` step, default-audience statement and error strings with the documented flow, because the GitLab page does not cover them. The earlier no-trailing-slash issuer was wrong per the docs.

Method: documentation only; no commands were run.
