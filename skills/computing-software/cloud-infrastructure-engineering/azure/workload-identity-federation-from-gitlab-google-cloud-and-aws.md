---
id: computing-software.cloud-infrastructure-engineering.azure.workload-identity-federation-from-gitlab-google-cloud-and-aws
name: workload-identity-federation-from-gitlab-google-cloud-and-aws
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, gitlab-oidc, gcp-federation, aws-federation, multicloud, secretless]
level: advanced
status: docs-checked
description: "Access Azure without secrets from GitLab CI and Google Cloud workloads: federated credential issuer, subject and audience values and the token exchange, plus the AWS caveat."
sources: ["https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation", "https://docs.gitlab.com/ci/cloud_services/azure/", "https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload identity federation from GitLab, Google Cloud and AWS

**Goal:** non-Azure workloads get Azure tokens by presenting their own platform's OIDC token - no client secrets.

All three follow the same pattern: create an app registration (or user-assigned managed identity), add a
federated credential with the external **issuer** and **subject**, an audience that matches the token's `aud`
(Microsoft recommends `api://AzureADTokenExchange`), grant RBAC, then exchange the external token for an Azure token.
A parent app or user-assigned managed identity holds at most 20 federated identity credentials. The issuer must
follow OIDC Discovery, which Entra uses to fetch the signing keys.

## GitLab CI
FIC: issuer is your GitLab instance URL (GitLab's Azure guide uses `https://gitlab.example.com` as the example), subject e.g.
`project_path:<mygroup>/<myproject>:ref_type:branch:ref:<branch>`. GitLab's guide sets the FIC audience to the instance URL and
the job's `aud` to match; the example below instead uses Microsoft's recommended value, which works if both sides agree.
```yaml
deploy:
  id_tokens:
    AZURE_OIDC:
      aud: api://AzureADTokenExchange
  script:
    - az login --service-principal -u "$AZURE_CLIENT_ID" -t "$AZURE_TENANT_ID" --federated-token "$AZURE_OIDC"
    - az account set -s "$AZURE_SUBSCRIPTION_ID"
```

## Google Cloud (GCE, GKE, Cloud Run)
FIC: issuer `https://accounts.google.com`, subject = the **Unique ID** of the Google service account, audience
`api://AzureADTokenExchange`. Obtain a Google-signed ID token for that service account with that audience, then:
```bash
az login --service-principal -u <clientId> -t <tenantId> --federated-token "$TOKEN"
```

## AWS
Entra needs an OIDC token from an issuer that follows OIDC Discovery. Microsoft's Learn pages for this skill do not
describe an AWS setup, so confirm the current AWS-side way to mint such a token in AWS's documentation before relying on it.

## Gotchas
- The FIC subject must match the token's `sub` claim and the issuer its `iss` claim, exactly.
- Max 20 FICs per app/identity - plan one identity per workload/environment.

## Verify
- [ ] `az account show` succeeds in the external job.

## Checked
2026-10-28. Confirmed on Microsoft Learn (workload identity federation, create trust pages) and GitLab's Azure guide: 20 FIC limit, recommended audience `api://AzureADTokenExchange`, issuer must follow OIDC Discovery, Google issuer `https://accounts.google.com` with the service account Unique ID as subject, GitLab subject format and `az login --federated-token` usage. Removed: GCE metadata call, SDK class name, Cognito details, token lifetime claim. The AWS section is now only a pointer to AWS's own docs, because the Cognito source was blocked and no Learn page covers it.
Method: documentation only; no commands were run.
