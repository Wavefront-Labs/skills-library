---
id: computing-software.cloud-infrastructure-engineering.terraform.oidc-cloud-credentials-in-gitlab-and-azure-devops
name: oidc-cloud-credentials-in-gitlab-and-azure-devops
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ci-oidc, oidc, gitlab-ci, azure-pipelines, workload-identity]
level: practitioner
status: docs-checked
description: "Replace static cloud keys in GitLab CI and Azure Pipelines with OIDC: GitLab id_tokens to AWS and Azure, and Azure DevOps workload identity service connections for Terraform."
sources: ["https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html", "https://docs.gitlab.com/ee/ci/cloud_services/aws/", "https://learn.microsoft.com/en-us/azure/devops/pipelines/library/connect-to-azure?view=azure-devops#create-an-azure-resource-manager-service-connection-that-uses-workload-identity-federation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC in GitLab CI and Azure Pipelines

## GitLab -> AWS
```yaml
plan:
  id_tokens:
    AWS_OIDC_TOKEN:
      aud: sts.amazonaws.com   # must match the audience set on the IAM OIDC provider
  script:
    - echo "$AWS_OIDC_TOKEN" > /tmp/web-identity-token
    - export AWS_ROLE_ARN=arn:aws:iam::<ACCOUNT_ID>:role/gitlab-payments-plan
    - export AWS_WEB_IDENTITY_TOKEN_FILE=/tmp/web-identity-token
    - terraform init -input=false && terraform plan -input=false
```
The AWS provider can assume a role from `AWS_ROLE_ARN` + `AWS_WEB_IDENTITY_TOKEN_FILE`
(see the AWS provider docs for web identity). IAM setup per GitLab's AWS guide: add
GitLab as an IAM OIDC provider (publicly reachable provider URL, plus an audience),
then a role whose trust policy allows `sts:AssumeRoleWithWebIdentity` with a condition on
`gitlab.com:sub` such as `project_path:corp/payments-infra:ref_type:branch:ref:main`.
On GitLab.com, `namespace_id` and `project_id` condition keys are more stable than paths;
self-managed instances support only `sub` and `aud`.

## GitLab -> Azure
```yaml
  id_tokens:
    ARM_OIDC_TOKEN:
      aud: api://AzureADTokenExchange
  variables:
    ARM_USE_OIDC: "true"
    ARM_CLIENT_ID: <app id>
    ARM_TENANT_ID: <tenant>
    ARM_SUBSCRIPTION_ID: <sub>
```
azurerm reads `ARM_OIDC_TOKEN` directly. Add the federated credential on the app
registration with the generic (other) issuer scenario; the issuer, subject and audience
must match the token's values case-sensitively. Use a GitLab subject like
`project_path:corp/payments-infra:ref_type:branch:ref:main`.

## Azure DevOps
Create an **Azure Resource Manager service connection** with **Workload identity
federation**. Then:
```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: sc-payments-prod
    addSpnToEnvironment: true
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: |
      export ARM_CLIENT_ID=$servicePrincipalId ARM_TENANT_ID=$tenantId
      export ARM_OIDC_TOKEN=$idToken ARM_USE_OIDC=true
      export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
      terraform init -input=false && terraform plan -input=false
```
`TerraformTaskV4@4` is not available by default: it comes from the Microsoft DevLabs
Terraform extension, which must be installed in the organization. The azurerm provider
guide recommends `AzureCLI@2`, and also describes `ARM_ADO_PIPELINE_SERVICE_CONNECTION_ID`
with `SYSTEM_ACCESSTOKEN` and `SYSTEM_OIDCREQUESTURI` as an alternative to `idToken`.

## Rules
- Separate plan (read-only) and apply roles; bind apply to protected branches/environments.
- GitLab ID tokens expire at the job timeout if one is set, otherwise after 5 minutes.

## Verify
- [ ] No static cloud secrets remain in CI variables.
- [ ] Non-protected branches cannot assume the apply identity.

## Checked
- 2026-10-28. Confirmed against GitLab's "ID token authentication" page (`id_tokens`, `aud`, token expiry of job timeout or 5 minutes), GitLab's "Configure OpenID Connect in AWS" page (IAM OIDC provider, audience guidance, `sts:AssumeRoleWithWebIdentity`, `gitlab.com:sub` example, `namespace_id` / `project_id` on GitLab.com only), the AWS CLI environment-variable page (`AWS_ROLE_ARN`, `AWS_WEB_IDENTITY_TOKEN_FILE`), the azurerm OIDC guide (`ARM_OIDC_TOKEN`, `api://AzureADTokenExchange`, generic issuer, Azure DevOps variables, `TerraformTaskV4@4` extension note), the `AzureCLI@2` reference (`addSpnToEnvironment` exposes `servicePrincipalId`, `idToken`, `tenantId`) and the Azure DevOps workload identity service connection page.
- Removed: the GitLab to GCP section, the ~1 hour cloud session claim and the claim that the S3 backend reads the web-identity variables natively (not in the fetched docs). Changed the AWS audience from the GitLab URL to the AWS-recommended pattern.
Method: documentation only; no commands were run.
