---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workload-identity-federation-from-gitlab-ci
name: workload-identity-federation-from-gitlab-ci
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-gitlab, gitlab-ci-federation, gitlab-id-tokens, keyless-auth, ci-cd]
level: practitioner
status: docs-checked
description: "Authenticate GitLab CI/CD jobs to Google Cloud without keys: OIDC provider for gitlab.com or self-managed, attribute conditions, and id_tokens in .gitlab-ci.yml."
sources: ["https://docs.gitlab.com/ee/ci/cloud_services/google_cloud/", "https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines#gitlab-saas", "https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload Identity Federation from GitLab CI/CD

## Pool and provider
```bash
P=<PROJECT>; PN=$(gcloud projects describe $P --format='value(projectNumber)')
gcloud iam workload-identity-pools create gitlab --location=global --project=$P
gcloud iam workload-identity-pools providers create-oidc gitlab-com \
  --location=global --workload-identity-pool=gitlab --project=$P \
  --issuer-uri="https://gitlab.com/" \
  --allowed-audiences="https://gitlab.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.project_path=assertion.project_path,attribute.ref=assertion.ref,attribute.ref_protected=assertion.ref_protected,attribute.namespace_id=assertion.namespace_id" \
  --attribute-condition="assertion.namespace_id=='1234567' && assertion.ref_protected=='true'"
```
Self-managed GitLab: issuer is your instance URL; Google must reach its `/.well-known/openid-configuration`
over the internet, or upload the JWKS (`--jwk-json-path`) if the instance is private.
GitLab's Google Cloud guide gives the issuer with a trailing slash and the allowed audience without one; confirm both against your token's `iss` and `aud`.
`namespace_id` is the unique group ID and `project_path` is the readable path; prefer the ID in conditions where you can.

## Grant
```bash
gcloud iam service-accounts add-iam-policy-binding deployer@$P.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PN/locations/global/workloadIdentityPools/gitlab/attribute.project_path/acme/infra"
```

## Job
```yaml
deploy:
  image: google/cloud-sdk:slim
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  script:
    - echo "$GITLAB_OIDC_TOKEN" > .ci_job_jwt_file
    - gcloud iam workload-identity-pools create-cred-config
        projects/$PN/locations/global/workloadIdentityPools/gitlab/providers/gitlab-com
        --service-account=deployer@$P.iam.gserviceaccount.com
        --credential-source-file=.ci_job_jwt_file --output-file=.gcp_cred.json
    - gcloud auth login --cred-file=.gcp_cred.json
    - gcloud run deploy ...
```
`aud` must equal one of the provider's allowed audiences.

## Gotchas
- Use the `id_tokens` keyword to obtain the token, as GitLab's ID-token guide shows.
- `ref_protected` is a GitLab token claim (true when the ref is protected); the condition keeps unprotected branches out.

## Verify
- [ ] Protected-branch job deploys; an unprotected branch gets `PERMISSION_DENIED` from STS.

## Checked

- Date: 2026-10-27
- Confirmed against GitLab's Google Cloud and ID-token guides (`id_tokens` with `aud`, issuer with trailing slash, audience without, `namespace_id`, `ref_protected` and `project_path` claims), the WIF deployment-pipelines guide (GitLab claims and `namespace_id`/`project_id` mapping), and gcloud references for `providers create-oidc`, `create-cred-config` and `auth login --cred-file`.
- Changed the issuer URI to the trailing-slash form GitLab documents. Removed the `CI_JOB_JWT` removal note, default-audience claim and token-lifetime note, which were not confirmed.

Method: documentation only; no commands were run.
