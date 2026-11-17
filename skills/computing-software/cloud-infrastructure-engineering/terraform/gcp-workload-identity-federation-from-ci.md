---
id: computing-software.cloud-infrastructure-engineering.terraform.gcp-workload-identity-federation-from-ci
name: gcp-workload-identity-federation-from-ci
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, gcp-wif, gcp-workload-identity-federation, workload-identity, oidc, google-provider]
level: practitioner
status: docs-checked
description: "Authenticate Terraform to Google Cloud from CI with Workload Identity Federation: pool, mappings, conditions, impersonation."
sources: ["https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines", "https://github.com/google-github-actions/auth"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP Workload Identity Federation from CI

**Goal:** the pipeline running Terraform authenticates to Google Cloud with its own short-lived
OIDC token, with no service account keys stored in CI.

## 1. Pool and provider (once per GitHub org, GitLab group or HCP Terraform org)
- You need Workload Identity Pool Admin (`roles/iam.workloadIdentityPoolAdmin`) on the project. Use a
  dedicated project for pools and providers. Enable the IAM, Resource Manager, Service Account
  Credentials and Security Token Service APIs.
- Create the pool and an OIDC provider:
```bash
gcloud iam workload-identity-pools create POOL_ID --location="global"
gcloud iam workload-identity-pools providers create-oidc PROVIDER_ID \
    --location="global" \
    --workload-identity-pool="POOL_ID" \
    --issuer-uri="https://token.actions.githubusercontent.com/" \
    --attribute-mapping="MAPPINGS" \
    --attribute-condition="CONDITIONS"
```
- Issuer URLs: GitHub Actions `https://token.actions.githubusercontent.com/`, GitLab SaaS
  `https://gitlab.com`, HCP Terraform `https://app.terraform.io`. Provider and pool IDs cannot be
  changed later, and the prefix `gcp-` is reserved.
- Mapping: at minimum `google.subject=assertion.sub` for GitHub. Map every claim you will use in a
  condition or principalSet. For GitHub, prefer the numeric `repository_id` and `repository_owner_id`
  claims over the name fields: names can be re-registered after a repo or organisation is deleted.
  HCP Terraform can map `terraform_workspace_id`; GitLab exposes `namespace_id`, `project_id` and `environment`.
- Condition is mandatory: GitHub, GitLab SaaS and HCP Terraform use one issuer for all customers, so
  restrict to your own tenant, for example `assertion.repository_owner=='ORGANIZATION'`, optionally
  `&& assertion.ref=='refs/heads/main'`. GitLab: `assertion.namespace_id=='GROUP_ID'`. HCP Terraform:
  `assertion.terraform_organization_id=='ORGANIZATION_ID'`. Change it later with
  `gcloud iam workload-identity-pools providers update-oidc ... --attribute-condition`.

## 2. Grant access
- Google recommends direct resource access: grant roles to the federated principal, using the project
  number (not the ID) in identifiers such as
  `principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/attribute.ATTRIBUTE_NAME/ATTRIBUTE_VALUE`.
- Some Google APIs have limitations; then use service account impersonation: create a dedicated service
  account per workload, grant it the needed roles, and give the federated principal
  `roles/iam.workloadIdentityUser` on it (`gcloud iam service-accounts add-iam-policy-binding`).
- HCP Terraform does not support direct resource access; it must use impersonation.

## 3. Pipeline side
- GitHub Actions: give the job `permissions: { id-token: write, contents: read }` and run
  `google-github-actions/auth` with `create_credentials_file: true`,
  `workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID`
  and, for impersonation, `service_account`. With a credentials file the action exports
  `GOOGLE_APPLICATION_CREDENTIALS`, which tools such as Terraform pick up. Pin to a current major
  version of the action.
- GitLab: declare `id_tokens` with `aud: https://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID`,
  write the token to a file, and write an `external_account` credential configuration file (with
  `credential_source.file` and, for impersonation, `service_account_impersonation_url`) pointed to by
  `GOOGLE_APPLICATION_CREDENTIALS`.
- HCP Terraform: set workspace environment variables `TFC_GCP_PROVIDER_AUTH=true`,
  `TFC_GCP_RUN_SERVICE_ACCOUNT_EMAIL`, `TFC_GCP_PROJECT_NUMBER`, `TFC_GCP_WORKLOAD_POOL_ID` and
  `TFC_GCP_WORKLOAD_PROVIDER_ID`.

## Gotchas
- Always set an attribute condition on shared-issuer providers; without one other tenants' tokens match.
- The `principalSet` member needs the project number of the pool's project, not the project ID.

## Verify
- [ ] No service account JSON keys in CI secrets.
- [ ] A repository outside the condition cannot obtain a token.

## Checked
Read in full the Google Cloud page on Workload Identity Federation with deployment pipelines (attribute mapping, conditions, provider creation, access grants, pipeline configuration) and the google-github-actions/auth README sections on inputs and exported variables. Removed as unconfirmed: the Terraform HCL resource blocks (the registry page is not readable), the `create-cred-config` GitLab command, the `getAccessToken` error text, and the claim that Google "now" requires conditions (the page says you must use one for these issuers).
Method: docs-checked 2026-11-09 against the cited Google Cloud page and the action README; no commands were run.
