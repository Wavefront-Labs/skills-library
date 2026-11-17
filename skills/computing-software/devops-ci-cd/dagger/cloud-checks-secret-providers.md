---
id: computing-software.devops-ci-cd.dagger.cloud-checks-secret-providers
name: cloud-checks-secret-providers
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, dagger-cloud, checks, secret-providers, oidc, aws, gcp, 1password, vault]
level: practitioner
status: docs-checked
description: "Run Dagger Cloud Checks on managed infrastructure and give them secrets via env vars or providers: AWS, AWS OIDC, GCP OIDC, 1Password, Vault."
sources: [https://docs.dagger.io/0.21/reference/configuration/cloud]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger Cloud Checks and secret providers

Goal: have Dagger Cloud run your module's check functions on push and supply secrets safely. Dagger 0.21 docs.

## How checks run

Prerequisites: Team account; GitHub repo with `dagger.json` at its root; at least one check function; the Cloud GitHub App installed. On each new commit Cloud loads the module, discovers checks, runs them on managed engines and reports GitHub commit statuses. Results show on the Checks page. Rerun with the replay icon (load failures can be rerun separately); cancel via the cancel icon; a newer commit on the same branch or PR cancels older runs.

## Secrets

- Environment variables: module settings (icon next to the module on Checks). They are injected as a `.env` file in the check working directory.
- Providers: Settings > CI, expand provider, fill credentials, pick Linked Modules, Save. Providers: AWS static (`AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`); AWS OIDC (`AWS_ROLE_ARN`, `AWS_REGION`); GCP OIDC (`GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL`); 1Password (`OP_SERVICE_ACCOUNT_TOKEN`); HashiCorp Vault (`VAULT_ADDR`, `VAULT_TOKEN`, optional AppRole fields).
- Secrets are never injected for PRs from forks.

## AWS OIDC setup

```sh
aws iam create-open-id-connect-provider \
  --url https://api.dagger.cloud \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 0000000000000000000000000000000000000000
```

Create a role (`aws iam create-role --role-name dagger-cloud-checks --assume-role-policy-document file://trust-policy.json`) whose trust policy allows `sts:AssumeRoleWithWebIdentity` from `arn:aws:iam::<ACCOUNT_ID>:oidc-provider/api.dagger.cloud` with condition `api.dagger.cloud:aud` = `sts.amazonaws.com`. Attach only needed permissions. Optionally scope the trust with `StringLike` on `api.dagger.cloud:sub`, e.g. `org:*:repo:github.com/myorg/*`.

## GCP OIDC setup

1. `gcloud iam workload-identity-pools create dagger-cloud --location=global`
2. `gcloud iam workload-identity-pools providers create-oidc dagger-cloud --location=global --workload-identity-pool=dagger-cloud --issuer-uri=https://api.dagger.cloud --allowed-audiences="//iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/dagger-cloud/providers/dagger-cloud" --attribute-mapping="google.subject=assertion.sub"`
3. Create service account `dagger-cloud-checks`; bind `roles/iam.workloadIdentityUser` to the pool principalSet; grant it needed roles (e.g. `roles/secretmanager.secretAccessor`).
4. Optional: `--attribute-condition="assertion.sub.startsWith('org:MY_ORG_ID:')"`.

## Troubleshooting (from the page)

- No checks: GitHub App missing, no `dagger.json` at root, or no new commit pushed.
- Not run: merge conflicts with the default branch block the merge commit Cloud builds.
- Load-phase failure: syntax errors or missing deps; reproduce locally with `dagger check`.
- Secrets missing: provider not linked to module, no env vars configured, or fork PR.
- Statuses missing on GitHub: app needs Commit statuses read/write.
- AWS "Request ARN is invalid": use the role ARN, not the provider ARN. "Access denied": role lacks permissions. "Could not assume role": check issuer URL, audience `sts.amazonaws.com`, trust policy provider ARN.
- GCP exchange fails: check issuer URI, audience, `workloadIdentityUser` grant and the `google.subject=assertion.sub` mapping.

Related: computing-software.devops-ci-cd.dagger.cloud-traces-ci-token.

## Checked

2026-11-07

Read in full from the docs source: reference/configuration/cloud.mdx (Checks, CI secrets, AWS OIDC, GCP OIDC, troubleshooting sections). Confirmed prerequisites, secret provider fields, fork PR rule, the AWS and GCP commands and trust policy details, and each troubleshooting item. No corrections needed.

Method: documentation only; no commands were run.
