---
id: computing-software.cloud-infrastructure-engineering.terraform.gcp-service-account-impersonation
name: gcp-service-account-impersonation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, gcp-impersonation, impersonate-service-account, google-provider, adc, workload-identity-federation, provider-authentication]
level: practitioner
status: docs-checked
description: "Run the google provider and gcs backend as an impersonated service account from user ADC or CI federation, with the IAM bindings and debug steps."
sources: ["https://developer.hashicorp.com/terraform/language/backend/gcs", "https://cloud.google.com/iam/docs/service-account-impersonation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP service account impersonation

Humans and CI authenticate as themselves, then **impersonate** a deploy service
account that holds the actual permissions. No SA keys.

## IAM
```bash
gcloud iam service-accounts add-iam-policy-binding \
  tf-deployer@acme-prod.iam.gserviceaccount.com \
  --member="group:platform-admins@acme.com" \
  --role="roles/iam.serviceAccountTokenCreator"
```
The SA itself gets the project roles it needs (as narrow as possible) and the Storage
Object Admin role (`roles/storage.objectAdmin`) on the state bucket. Impersonating needs
the `iam.serviceAccounts.getAccessToken` permission, which `roles/iam.serviceAccountTokenCreator` includes.

## Local
```bash
gcloud auth application-default login
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=tf-deployer@acme-prod.iam.gserviceaccount.com
terraform init && terraform plan
```

## Config
```hcl
terraform {
  backend "gcs" {
    bucket                      = "acme-tf-state"
    prefix                      = "prod/network"
    impersonate_service_account = "tf-deployer@acme-prod.iam.gserviceaccount.com"
  }
}

provider "google" {
  project                     = "acme-prod"
  region                      = "europe-west1"
  impersonate_service_account = var.deployer_sa
}
```
Backend and provider are configured separately; set both. The backend also reads
`GOOGLE_BACKEND_IMPERSONATE_SERVICE_ACCOUNT` and `GOOGLE_IMPERSONATE_SERVICE_ACCOUNT`; check the google provider's
documentation for how the provider side is configured.

## CI
Use Workload Identity Federation to get Application Default Credentials as the CI
identity (Google documents credential configuration files for applications that use
Workload Identity Federation), then impersonate per environment if needed.

## Chains
The gcs backend takes `impersonate_service_account_delegates` for a delegation chain;
avoid unless required by org structure.

## Debug
```bash
gcloud auth print-access-token --impersonate-service-account=tf-deployer@acme-prod.iam.gserviceaccount.com
```
A denied `iam.serviceAccounts.getAccessToken` means the caller lacks the Token Creator
role (or equivalent permission) on that service account.

## Verify
- [ ] Audit logs show actions by `tf-deployer@...`.
- [ ] No `credentials` JSON key files in repo or CI secrets.

## Checked
2026-10-31. Confirmed against the Terraform gcs backend page and Google's service account impersonation page: backend `impersonate_service_account` and its three environment variables, `impersonate_service_account_delegates`, `roles/iam.serviceAccountTokenCreator`, the `iam.serviceAccounts.getAccessToken` permission, Storage Object Admin on the bucket, Workload Identity Federation credential configuration, `--impersonate-service-account` on gcloud (gcloud command verified by check_commands). Removed: `roles/editor`, the API-not-enabled error and `iamcredentials` service, the audit-log field, the GitHub Action inputs, and the claim that the provider honours the environment variable (the registry page is a stub and the provider guides fetched do not cover it).
Method: documentation only; no commands were run.
