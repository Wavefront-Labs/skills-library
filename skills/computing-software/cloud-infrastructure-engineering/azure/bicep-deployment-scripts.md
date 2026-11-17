---
id: computing-software.cloud-infrastructure-engineering.azure.bicep-deployment-scripts
name: bicep-deployment-scripts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, deployment-scripts, deploymentscripts, azure-cli-script, private-networking, iac]
level: advanced
status: docs-checked
description: "Run CLI or PowerShell inside a Bicep deployment with deploymentScripts: identity, outputs, rerun control, retention and cleanup, private networking and when not to."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/bicep/deployment-script-bicep", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/deployment-script-vnet", "https://learn.microsoft.com/azure/templates/microsoft.resources/deploymentscripts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bicep deployment scripts

**Goal:** fill the gaps ARM can't do declaratively (data-plane setup, lookups, Graph calls) inside the same deployment.

## Example
```bicep
param utcValue string = utcNow()

resource script 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: 'ds-create-container'
  location: location
  kind: 'AzureCLI'
  identity: { type: 'UserAssigned', userAssignedIdentities: { '${uami.id}': {} } }
  properties: {
    azCliVersion: '<supported-az-cli-version>'
    forceUpdateTag: utcValue            // rerun on every deployment; omit to run only when inputs change
    timeout: 'PT15M'
    retentionInterval: 'PT1H'
    cleanupPreference: 'OnExpiration'
    environmentVariables: [
      { name: 'ACCOUNT', value: sa.name }
      { name: 'SECRET', secureValue: someSecret }
    ]
    scriptContent: '''
      set -e
      az storage container create --account-name "$ACCOUNT" --name ingest --auth-mode login
      echo "{\"containerUrl\":\"https://$ACCOUNT.blob.core.windows.net/ingest\"}" > "$AZ_SCRIPTS_OUTPUT_PATH"
    '''
  }
}
output containerUrl string = script.properties.outputs.containerUrl
```
PowerShell kind: `azPowerShellVersion`, set `$DeploymentScriptOutputs['key'] = ...`.

## How it runs
The service creates a temporary **storage account** (script/log share) and an **Azure Container Instance** in your RG,
runs the script with the given identity, then cleans up per `cleanupPreference` (default `Always`; `OnExpiration` keeps the resources until `retentionInterval` passes; the default `timeout` is `P1D`). The resource is available only in regions where Azure Container Instances is available.

## Private networking
If storage accounts must be private (policy), supply `storageAccountSettings` (existing account) and
`containerSettings.subnetIds` (subnet delegated to `Microsoft.ContainerInstance/containerGroups`) so the script runs
inside your VNet.

## Gotchas
- The identity needs RBAC for what the script does and must exist before the script (role propagation can take minutes -
  add a retry loop in the script).
- Scripts must be idempotent - they rerun on redeploy when `forceUpdateTag` changes.
- Policies denying ACI or public storage break deployment scripts unless private networking is configured.
- Logs: `az deployment-scripts show-log -g rg --name ds-create-container`.
- If a declarative resource or extension exists for the job, use it instead - scripts are opaque to what-if.

## Verify
- [ ] Deployment succeeds twice in a row (idempotent); outputs populated; temporary ACI/storage removed after the retention interval.

## Checked
2026-10-28. Confirmed against Microsoft Learn deployment-script-bicep, deployment-script-vnet and the Microsoft.Resources/deploymentScripts template reference: API version 2023-08-01, `AzureCLI` kind, `forceUpdateTag`, `retentionInterval`, `cleanupPreference` default Always and OnExpiration, default timeout P1D, `$AZ_SCRIPTS_OUTPUT_PATH`, `$DeploymentScriptOutputs`, supporting storage account and container instance, `storageAccountSettings`, `containerSettings.subnetIds`, ContainerInstance containerGroups delegation, `az deployment-scripts show-log`. Removed: the pinned CLI version 2.63.0, the OnSuccess value and the 1-2 minute overhead (not in the pages).
Method: documentation only; no commands were run.
