---
id: computing-software.cloud-infrastructure-engineering.azure.pipeline-secrets-variable-groups-and-service-connections
name: pipeline-secrets-variable-groups-and-service-connections
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-pipelines, pipeline-secrets, variable-groups, service-connections, workload-identity-federation, service-connection-security, key-vault-variable-group, azurekeyvault-task, secure-files, secret-variables, secret-masking, pipeline-security, system-accesstoken, pat-hygiene, least-privilege-pipelines, job-authorization-scope, approvals-on-service-connections, github-actions-azure-login, oidc]
level: practitioner
status: draft
description: "Keep secrets out of pipelines: service connections with workload identity federation, RG-scoped RBAC, checks on connections, Key Vault variable groups vs task, secure files, masking, PAT hygiene."
sources: ["Microsoft Learn - Azure Resource Manager service connections with workload identity federation", "Microsoft Learn - Variable groups, link secrets from Azure Key Vault and the AzureKeyVault@2 task", "Microsoft Learn - Secure files, secret variables and how secrets are masked in logs", "Microsoft Learn - Securing Azure Pipelines: job authorization scope, protected resources, checks on service connections", "Microsoft Learn - Use GitHub Actions to connect to Azure (azure/login with OIDC)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pipeline secrets and service connections — identities instead of secrets, scopes instead of trust

**Goal:** pipelines deploy with federated identities that have exactly the RBAC they
need, secrets reach jobs from Key Vault at run time and never from YAML/variables,
and every protected resource records who may use it.

## 1. Service connections (Azure Resource Manager)
- **Workload identity federation** (recommended; no client secret): the connection is an
  Entra app/managed identity with a federated credential whose issuer is
  `https://vstoken.dev.azure.com/<org-id>` and subject `sc://<org>/<project>/<connection-name>`.
  Automatic mode creates the app for you; manual mode lets you use a **user-assigned managed identity** (preferred: no app registration, no secret, lives in your subscription):
```bash
az identity create -g rg-cicd -n id-sc-prod
az identity federated-credential create --identity-name id-sc-prod -g rg-cicd -n ado-prod --issuer https://vstoken.dev.azure.com/<org-guid> --subject "sc://<org>/<project>/sc-prod" --audiences api://AzureADTokenExchange
az role assignment create --assignee-object-id <id-principal> --assignee-principal-type ServicePrincipal --role Contributor --scope /subscriptions/<sub>/resourceGroups/rg-app-prod
# Azure DevOps: Project settings → Service connections → New → Azure Resource Manager → Workload Identity federation (manual) → enter the identity's clientId/tenantId, subscription
```
- Convert existing secret-based connections (*Convert* button) — the secret is deleted after validation. Service principal secrets expire; PAT-style outages disappear with federation.
- **Scope**: one connection per environment (and per subscription), roles at **resource group** scope, not subscription; custom role for deploy-only if Contributor is too broad; *User Access Administrator* only for the landing-zone pipeline that assigns roles (with conditions limiting assignable roles).
- **Security tab**: untick *Grant access permission to all pipelines*; authorise pipelines explicitly; add **checks** (approvals, branch control, required template) to the prod connection; *User permissions*: readers only for most, administrators = platform group.
- Other connection types (GitHub, Docker registry, Kubernetes, generic) — prefer the Azure RM connection + `az aks get-credentials`/`az acr login` in steps over separate credentials.

## 2. Secrets at run time
| Mechanism | Use |
|---|---|
| **AzureKeyVault@2 task** (`KeyVaultName`, `SecretsFilter: 'db-password,api-key'`, `RunAsPreJob: true`) | per-pipeline fetch at job start → secret variables; needs the connection's identity *Key Vault Secrets User* on the vault (RBAC) and a vault firewall that admits the agent — Key Vault's trusted-services bypass does **not** cover hosted agents, so use self-hosted/Managed DevOps Pools in the VNet or allow the published agent IP ranges |
| **Variable group linked to Key Vault** | same secrets shared across pipelines; refreshed at run start; values appear as secret variables; group-level permissions + checks |
| **Secret variables** in pipeline/variable group (lock icon) | last resort for non-Azure secrets; set via `az pipelines variable create --secret true` or UI; never visible after save |
| **Secure files** | certificates, kubeconfigs, mobile signing keys — `DownloadSecureFile@1`, deleted after the job; checks + authorised pipelines |
- Secret variables aren't exposed as env vars automatically — map explicitly: `env: { DB_PASSWORD: $(db-password) }` on the step that needs it; never `echo $(secret)`.
- Pass secrets between jobs/stages only via Key Vault or `isOutput` variables marked secret (`issecret=true` in `setvariable`), never through artifacts/files.
- **Masking** replaces exact matches of secret values in logs — it won't catch `base64`, URL-encoded, split, or JSON-escaped forms; `set -x`/verbose tasks leak transformed secrets. Treat masking as best-effort, not a control.
- `System.AccessToken` (`$(System.AccessToken)`/`env: SYSTEM_ACCESSTOKEN`) is the build identity's token for Azure DevOps APIs (feeds, repos, work items) — scope it with *Limit job authorization scope to current project (release/non-release)* and *Protect access to repositories*; grant the build service only what the pipeline needs (feed Contributor, repo Contribute for tagging).

## 3. GitHub Actions to Azure (same principles)
```yaml
permissions: { id-token: write, contents: read }
- uses: azure/login@v2
  with: { client-id: ${{ vars.AZURE_CLIENT_ID }}, tenant-id: ${{ vars.AZURE_TENANT_ID }}, subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }} }   # OIDC, no secret
```
Federated credential on the identity/app: issuer `https://token.actions.githubusercontent.com`, subject `repo:org/repo:environment:prod` (environment-scoped — never `ref:refs/heads/*` wildcards for prod), audience `api://AzureADTokenExchange`. GitHub **environments** with required reviewers + deployment branch policies mirror Azure DevOps checks; secrets as environment secrets, or better, fetched from Key Vault after login.

## 4. Hygiene and detection
- **PATs**: org policy *Restrict personal access token creation/scope/lifespan* (max 30–90 days, no full-scope); audit PAT usage (`Token.PatCreateEvent`, usage in audit stream); tools that need PATs (npm login, legacy agents) get dedicated service accounts with PIM-approved rotation. Agent registration: use the *Managed DevOps Pools*/VMSS pools or short-lived PATs — registration PATs are only needed at registration.
- Audit stream → Log Analytics/Sentinel: `Pipelines.*` and `Library.*` events (variable group changes, service connection shares), `Policy.PolicyConfigModified`.
- Secret scanning: Advanced Security for Azure DevOps push protection + repo scanning (devsecops skill); `gitleaks` in PR build as a cheap fallback.
- Rotate: identities with federation have nothing to rotate; for remaining secrets, Key Vault rotation + consumers reading unversioned secrets at run time means rotation is a non-event.
- Inventory: `az devops service-endpoint list -p <project> --query "[].{n:name,t:type,auth:authorization.scheme}" -o table` — anything with `ServicePrincipal` (secret) scheme is a migration ticket.

## Gotchas
- *Grant access permission to all pipelines* on a new connection is ticked by default in the UI — the single most common over-exposure.
- Workload identity subjects are exact strings; renaming the service connection or moving the project breaks federation (`AADSTS70021`) — update the federated credential subject.
- Variable groups linked to Key Vault pull **all** selected secrets at the start of every run — a group with 50 secrets used by 200 pipelines is a Key Vault throttling and audit noise source; split by purpose.
- Secrets referenced as `$(secret)` inside `condition:` or template expressions aren't expanded; secrets are only available to steps.
- Forked-PR builds get no secrets (good) but *also* no Key Vault — tests that need them must be skipped by `condition`.
- Hosted agents can't reach a Key Vault with public access disabled; the AzureKeyVault task then fails with 403 `Forbidden by firewall` — plan private agents for private vaults.
- Secret variables set in YAML (`variables: { pw: 'literal' }`) are plain text in Git; the lock icon exists only in the UI/variable groups.

## Verify
- [ ] `az devops service-endpoint list` shows every Azure RM connection with `WorkloadIdentityFederation`; none with secrets; prod connection has checks and no "all pipelines" access.
- [ ] Role assignments for the connection identities are RG-scoped (`az role assignment list --assignee <id> --all -o table` shows no subscription-level Contributor/Owner).
- [ ] A test pipeline fetches a Key Vault secret via the task and uses it; the log shows `***`; a grep of the raw log download for the value (and its base64) finds nothing.
- [ ] PAT policy enforced (creation of a full-scope, 1-year PAT is rejected); audit events for service-connection changes arrive in the SIEM.
