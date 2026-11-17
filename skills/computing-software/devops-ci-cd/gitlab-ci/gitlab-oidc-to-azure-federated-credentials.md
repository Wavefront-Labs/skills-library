---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-oidc-to-azure-federated-credentials
name: gitlab-oidc-to-azure-federated-credentials
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-azure-federated, azure-workload-identity-gitlab, federated-identity-credential]
level: advanced
status: docs-checked
description: "Log GitLab CI into Azure without client secrets: federated identity credentials matching GitLab sub claims, and az login with the job ID token."
sources: ["https://docs.gitlab.com/ci/cloud_services/azure/", "https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/cloud_services/azure/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab ID tokens to Azure federated credentials

## 1. Azure side
Prerequisites in the docs: an Azure subscription with `Owner` access, a Microsoft Entra ID tenant with at least `Application Developer`, the Azure CLI, and a GitLab instance that is publicly reachable (Azure must call `GET /.well-known/openid-configuration` and `GET /oauth/discovery/keys`).

```bash
appId=$(az ad app create --display-name gitlab-oidc --query appId -otsv)
az ad sp create --id $appId --query appId -otsv
objectId=$(az ad app show --id $appId --query id -otsv)
```
Federated credential for one branch (JSON body, posted with `az rest` to Microsoft Graph):
```json
{
  "name": "gitlab-federated-identity",
  "issuer": "https://gitlab.example.com",
  "subject": "project_path:<mygroup>/<myproject>:ref_type:branch:ref:<branch>",
  "description": "GitLab service account federated identity",
  "audiences": ["https://gitlab.example.com"]
}
```
```bash
az rest --method POST --uri "https://graph.microsoft.com/beta/applications/$objectId/federatedIdentityCredentials" --body @body.json
```
For any branch or tag, use a flexible federated identity credential: set `"subject": null` and
`"claimsMatchingExpression": {"value": "claims['sub'] matches 'project_path:<mygroup>/<myproject>:ref_type:branch:ref:*'", "languageVersion": 1}`
(use `ref_type:tag` for tags).

Grant the service principal access (the docs use `Reader` at subscription scope and tell you to apply least privilege):
```bash
az role assignment create --assignee $appId --role Reader --scope /subscriptions/<subscription-id>
```

## 2. Job (from the docs)
```yaml
default:
  image: mcr.microsoft.com/azure-cli:latest
variables:
  AZURE_CLIENT_ID: "<client-id>"
  AZURE_TENANT_ID: "<tenant-id>"
auth:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com        # must equal an audience in the federated credential
  script:
    - az login --service-principal -u $AZURE_CLIENT_ID -t $AZURE_TENANT_ID --federated-token $GITLAB_OIDC_TOKEN
    - az account show
```

## 3. Errors
- `AADSTS70021: No matching federated identity record found for presented assertion`: check the issuer (for example `https://gitlab.com` or your GitLab URL), the subject (for `gitlab-group/gitlab-project` on `main`: `project_path:gitlab-group/gitlab-project:ref_type:branch:ref:main`) and the audience in the credential.
- `AADSTS501661: Request to External OIDC endpoint failed`: the instance is not publicly reachable; after fixing the firewall the docs say to clear the Redis cache and retry.
- `AADSTS700212 ... presented assertion audience`: the job's `aud` differs from the audience used to create the credential.

## Verify
- [ ] `az account show` works in a job on the allowed branch; a pipeline on another ref fails with AADSTS70021.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/cloud_services/azure/_index.md: app and service principal creation, the federated credential JSON (`issuer`, `subject`, `audiences`) created through Microsoft Graph, flexible federated credentials with `claimsMatchingExpression` for any branch or tag, the `az role assignment create` step, the `az login --service-principal ... --federated-token` job, the three troubleshooting errors (AADSTS70021, AADSTS501661, AADSTS700212) and the two public endpoints Azure must reach. Removed the 20-credential limit, the Terraform `ARM_*` variables, the portal click path beyond what the page shows, the `az webapp deploy` step and the claim about token lifetime, which that page does not state.

Method: documentation only; no commands were run.
