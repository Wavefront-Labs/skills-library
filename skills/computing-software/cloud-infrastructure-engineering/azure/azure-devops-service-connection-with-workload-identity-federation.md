---
id: computing-software.cloud-infrastructure-engineering.azure.azure-devops-service-connection-with-workload-identity-federation
name: azure-devops-service-connection-with-workload-identity-federation
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, service-connection-wif, azure-devops-wif, wif-service-connection, azure-resource-manager-connection, oidc]
level: practitioner
status: docs-checked
description: "Create or convert Azure DevOps ARM service connections to workload identity federation: automatic vs manual setup, issuer/subject values, conversion and rollback."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/library/connect-to-azure", "https://learn.microsoft.com/azure/devops/pipelines/release/configure-workload-identity", "https://learn.microsoft.com/azure/devops/pipelines/release/troubleshoot-workload-identity", "https://learn.microsoft.com/azure/devops/pipelines/release/convert-service-connections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure DevOps service connection with workload identity federation

**Goal:** every Azure Resource Manager service connection uses federation — no expiring secrets,
nothing to rotate.

## Automatic (you have rights to create app registrations and assign roles)
Project settings -> Service connections -> New -> Azure Resource Manager -> **App registration (automatic)** with the credential *Workload identity federation*, then choose the scope (subscription, management group or Machine Learning workspace). Azure DevOps creates the workload identity federation for you. Requirements include the Owner role on the subscription, and it is not available for Azure Stack or Azure US Government. There is also a **Managed identity** option that creates the federated credential on an existing user-assigned managed identity.

## Manual (platform team pre-creates identity - recommended in enterprises)
1. Create a user-assigned managed identity (or app registration) in Azure.
2. Create the service connection in Azure DevOps and save it as a draft; Azure DevOps shows the **Issuer** and **Subject identifier**:
   - New service connections use the Microsoft Entra issuer `https://login.microsoftonline.com/<entra-tenant-id>/v2.0` with subject `<microsoft entra prefix>/sc/<organization id>/<service connection id>`.
   - The older Azure DevOps issuer `https://vstoken.dev.azure.com/<organization id>` with subject `sc://<organization name>/<project name>/<service connection name>` is deprecated and retires on July 1, 2027 (public cloud, single-tenant apps and managed identities; non-public clouds and multitenant apps are out of scope).
3. Add the federated credential, copying issuer and subject from the UI:
```bash
az identity federated-credential create -g rg-cicd --identity-name id-ado-orders -n ado-orders-prod \
  --issuer "<issuer from UI>" --subject "<subject from UI>" --audiences api://AzureADTokenExchange
```
4. Grant the identity the roles it needs on the target resources (for example Contributor on a resource group), then **Verify and save** the service connection.
With the legacy name-based subject, renaming the organization, project or service connection changes the subject and requires updating the credential.

## Convert existing secret-based connections
In Project settings -> Service connections, select the connection and choose **Convert**. The conversion tool works only for connections Azure DevOps created itself (it cannot modify credentials it did not create) and used by one project (cross-project connections cannot be converted). Connections still on the deprecated Azure DevOps issuer are flagged in the list; select **Update** to move them to the Microsoft Entra issuer. If you lack the identity permissions for the automated flow, add the federated credential manually and then finish the setup in Azure DevOps. For manually created connections, add a federated credential to the existing identity and complete the setup in the connection.

## Pipeline usage (unchanged)
```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: sc-orders-prod
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: az deployment group create -g rg-orders-prod -f main.bicep
```
Almost all Azure tasks support workload identity federation; the troubleshooting article lists task support by version.

## Troubleshooting
- `AADSTS700213` / `AADSTS700211` (no matching federated identity record for subject / issuer) -> compare issuer and subject with the connection's values; for new connections the issuer starts with `https://login.microsoftonline.com`.
- `cannot request token: Get ...?audience=api://AzureADTokenExchange: unsupported protocol scheme` or `Could not fetch access token for Azure` -> the task does not support workload identity federation.
- `UnrecognizedArgumentError: unrecognized arguments: --federated-token` -> the agent has an older Azure CLI than workload identity federation requires.
- `AADSTS700223` or `AADSTS700238` -> workload identity federation is disabled in the Microsoft Entra tenant.

## Verify
- [ ] Service connections list shows workload identity federation for the ARM connections and none are flagged as deprecated.
- [ ] The app registration has no client secrets or certificates, and a pipeline run using the connection succeeds.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-devops-docs (pipelines/library/connect-to-azure, pipelines/release/configure-workload-identity, troubleshoot-workload-identity, convert-service-connections; main branch).
- Corrected: new workload identity federation service connections use the Microsoft Entra issuer and ID-based subject; the Azure DevOps issuer is deprecated and retires on July 1, 2027; AzurePowerShell@4 does support workload identity federation, so the claim that it does not was removed.
- Confirmed: automatic and managed-identity creation paths and the Owner requirement; manual draft-federate-grant-save flow; conversion tool prerequisites and the flagged-connection Update flow; documented error messages for unsupported tasks and old Azure CLI; AADSTS700223 and AADSTS700238.
- Removed as unconfirmed: the 7-day rollback window, the REST conversion call, the `addSpnToEnvironment` and `idToken` guidance, the automatic Contributor assignment and app rename advice, and the "Federated token" log line.
Method: documentation only; no commands were run.
