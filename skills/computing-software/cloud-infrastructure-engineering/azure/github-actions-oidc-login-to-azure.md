---
id: computing-software.cloud-infrastructure-engineering.azure.github-actions-oidc-login-to-azure
name: github-actions-oidc-login-to-azure
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, github-actions-oidc, azure-login-oidc, github-federation, github-actions-azure-login, azure-login, federated-credentials]
level: practitioner
status: docs-checked
description: "Log GitHub Actions into Azure with OIDC: federated credential subjects for branch, environment and PR, azure/login without secrets, and subject-mismatch troubleshooting."
sources: ["https://learn.microsoft.com/azure/developer/github/connect-from-azure-openid-connect", "https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-azure", "https://github.com/Azure/login", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation-create-trust"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions OIDC login to Azure

**Goal:** workflows deploy to Azure with short-lived tokens bound to a repo + environment —
no client secrets in GitHub.

## 1. Identity
Use a user-assigned managed identity (no app registration needed) or an app registration:
```bash
az identity create -g rg-cicd -n id-gh-orders-prod
az role assignment create --assignee-object-id $(az identity show -g rg-cicd -n id-gh-orders-prod --query principalId -o tsv) \
  --assignee-principal-type ServicePrincipal --role Contributor --scope /subscriptions/<sub>/resourceGroups/rg-orders-prod
```

## 2. Federated credential — the subject must match exactly
The credential's `subject` must match the `sub` claim of the GitHub token exactly. The format depends on the trigger
(environment, branch, tag, pull request) and on GitHub's subject-claim settings; decode a real token (see Troubleshooting) and copy `sub`.
```bash
az identity federated-credential create -g rg-cicd --identity-name id-gh-orders-prod -n gh-prod-env \
  --issuer https://token.actions.githubusercontent.com \
  --subject '<sub claim from the GitHub token>' \
  --audiences api://AzureADTokenExchange
```
Prefer **environment** subjects: GitHub environment protection rules (reviewers, branch filters) then gate the Azure access.

## 3. Workflow
```yaml
permissions:
  id-token: write     # required for OIDC
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: azure/login@v3
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az deployment group create -g rg-orders-prod -f main.bicep
```
IDs are not secrets — store as variables. `allow-no-subscriptions: true` for tenant-level jobs.

## Troubleshooting
- `AADSTS700213` / `AADSTS7002138` (no matching federated identity record) → the credential's issuer, subject or audience differs from the GitHub token; print the token's claims in the job and compare `sub`. GitHub's subject-claim format changed for repositories created after 15 July 2026 (see the GitHub OIDC docs).
- `id-token: write` missing → the workflow cannot request an OIDC token.
- Azure access tokens from a service principal are expected to last 1 hour by default; long jobs need a fresh login.

## Verify
- [ ] No `AZURE_CREDENTIALS`/client secrets remain in repo/org secrets.
- [ ] A workflow from a feature branch targeting the production environment is blocked by environment rules, and no credential exists for that branch.
- [ ] Entra sign-in logs (service principal sign-ins) show federated sign-ins from the identity.

## Checked

Date: 2026-10-28.

Confirmed against Learn (workload identity federation create trust), the Azure/login README and GitHub's OIDC-in-Azure docs: `id-token: write`, audience `api://AzureADTokenExchange`, azure/login v3 supported (v2 is maintenance mode), `allow-no-subscriptions`, 1-hour service principal token default, AADSTS700213/7002138 for no matching credential, July 2026 subject-claim change. CLI commands via check_commands.py.
Removed: the subject-format table, the 20-credential limit and flexible credentials, the token-decode curl and env var names, reusable-workflow subject note, and the actions/checkout version.

Method: documentation only; no commands were run.
