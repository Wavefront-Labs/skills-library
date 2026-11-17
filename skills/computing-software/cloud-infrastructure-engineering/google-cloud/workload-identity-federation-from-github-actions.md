---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workload-identity-federation-from-github-actions
name: workload-identity-federation-from-github-actions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, github-actions-wif, google-github-actions-auth, github-oidc, id-token-write, repository-claim, direct-workload-identity, keyless-ci, attribute-condition-github, setup-gcloud]
level: practitioner
status: docs-checked
description: "Authenticate GitHub Actions to GCP with google-github-actions/auth and Workload Identity Federation: GitHub OIDC provider, attribute condition, direct vs SA impersonation."
sources: ["https://github.com/google-github-actions/auth", "https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines", "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload Identity Federation from GitHub Actions

**Goal:** CI deploys to GCP with a token that only a specific repo and branch can obtain —
no `GCP_SA_KEY` secret in GitHub.

## 1. GCP side (once per org/env)
```bash
gcloud iam workload-identity-pools create github --location=global --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc github --workload-identity-pool=github --location=global \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.repository_owner=='my-org'"
```
The condition is the fence: without `repository_owner==...`, any public GitHub repo could
present a token to this provider. Tighten further per environment with `assertion.ref=='refs/heads/main'`
or `assertion.environment=='prod'` (GitHub *environments* with required reviewers give you an
approval gate that the claim carries).

## 2. Two ways to grant
**Direct** (preferred, no SA): grant roles to the principalSet.
```bash
gcloud projects add-iam-policy-binding <P> --role=roles/run.developer \
  --member="principalSet://iam.googleapis.com/projects/<NUM>/locations/global/workloadIdentityPools/github/attribute.repository/my-org/payments-api"
```
**Impersonation** (when a product does not accept federated principals, or you want one SA per env):
```bash
gcloud iam service-accounts add-iam-policy-binding deploy-prod@<P>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/<NUM>/locations/global/workloadIdentityPools/github/attribute.repository/my-org/payments-api"
```

## 3. Workflow
```yaml
permissions: { contents: read, id-token: write }      # id-token: write is mandatory
steps:
  - uses: actions/checkout@v7
  - id: auth
    uses: google-github-actions/auth@v3
    with:
      project_id: <PROJECT_ID>
      workload_identity_provider: projects/<NUM>/locations/global/workloadIdentityPools/github/providers/github
      # service_account: deploy-prod@<P>.iam.gserviceaccount.com    # only for impersonation mode
  - uses: google-github-actions/setup-gcloud   # pin the current major version from its README
  - run: gcloud run deploy payments-api --image=... --region=europe-west1
```
With `create_credentials_file` true (the default), `auth` writes a credential-config file and exports
`CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`, `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_GHA_CREDS_PATH`, plus project variables
such as `GOOGLE_CLOUD_PROJECT`, so later steps pick them up. Set `token_format: access_token` if you need a raw
token (`steps.auth.outputs.access_token`) for `docker login`/curl.

## 4. Docker and Artifact Registry
```yaml
  - uses: docker/login-action@v3
    with: { registry: europe-docker.pkg.dev, username: oauth2accesstoken, password: ${{ steps.auth.outputs.access_token }} }
```
Needs `token_format: access_token` on the auth step and `roles/artifactregistry.writer` for the principal.

## Gotchas
- `google.subject` is limited to 127 characters, and GitHub's `sub` (for example `repo:<owner>/<repo>:environment:prod`) can exceed that for long names; map it anyway, but grant on `attribute.repository`.
- Not every product accepts federated principals directly (see the *federated identity supported products* page); use impersonation for those jobs.

## Verify
- [ ] Workflow run on `main` deploys; the same workflow on a fork PR fails at the auth step.
- [ ] Repository secrets contain no JSON key.

## Checked

- Date: 2026-10-27
- Confirmed against the google-github-actions/auth README (`auth@v3`, `id-token: write`, `workload_identity_provider`, optional `service_account`, direct federation preferred, `token_format` must be `access_token`, exported environment variables), the GitHub OIDC hardening page (issuer `https://token.actions.githubusercontent.com`, `sub`/`environment`/`repository` claims), the deployment-pipelines WIF guide (repository, repository_owner claims), the best-practices page (attribute conditions for GitHub) and the gcloud references for `providers create-oidc`.
- Updated action versions to the README's `auth@v3` and `checkout@v7`; removed unpinned `setup-gcloud@v2`, fork-PR and reusable-workflow claims, job-level permission override note and the audit-log verify step.

Method: documentation only; no commands were run.
