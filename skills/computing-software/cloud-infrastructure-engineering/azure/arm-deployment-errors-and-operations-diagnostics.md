---
id: computing-software.cloud-infrastructure-engineering.azure.arm-deployment-errors-and-operations-diagnostics
name: arm-deployment-errors-and-operations-diagnostics
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, deployment-errors, deployment-operations, deployment-troubleshooting, arm-templates, correlation-id]
level: practitioner
status: docs-checked
description: "Diagnose failed ARM/Bicep deployments: find the failing operation and inner error, decode common codes (InvalidTemplate, Conflict, quota, policy) and use debug logging."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/troubleshooting/common-deployment-errors", "https://learn.microsoft.com/azure/azure-resource-manager/troubleshooting/find-error-code", "https://learn.microsoft.com/azure/azure-resource-manager/troubleshooting/enable-debug-logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARM deployment errors and operations diagnostics

**Goal:** from "DeploymentFailed" to the specific resource, property and fix in a few commands.

## 1. Validation vs deployment errors
- **Validation** (before anything deploys): `InvalidTemplate`, `InvalidTemplateDeployment` (check template syntax), `MissingSubscriptionRegistration` (register the resource provider). Reproduce with `az deployment group validate`.
- **Deployment** (during): per-resource provider errors. The top-level `DeploymentFailed` is only a wrapper.

## 2. Find the failing operation
```bash
az deployment group list -g rg --query "[?properties.provisioningState=='Failed'].{name:name,ts:properties.timestamp}" -o table
az deployment operation group list -g rg -n <deployment> \
  --query "[?properties.provisioningState=='Failed'].{res:properties.targetResource.resourceName,type:properties.targetResource.resourceType,code:properties.statusMessage.error.code,msg:properties.statusMessage.error.message}" -o json
```
Bicep modules are nested deployments: the outer failure points to a module; list operations of
that nested deployment name (the module's deployment name). The resource group's Activity log also lists each deployment operation and its message.

## 3. Common codes
| Code | Usual cause / fix |
|---|---|
| `RequestDisallowedByPolicy` | A resource policy blocks the action; find the policy and change the deployment to meet it |
| `QuotaExceeded` / `ResourceQuotaExceeded` / `OperationNotAllowed` | Exceeds quota for subscription, resource group or region (or an operation not allowed on that SKU); revise or request a quota change |
| `SkuNotAvailable` / `AllocationFailed` | Pick a SKU or VM size available in the location; for allocation failures retry later or choose another size |
| `Conflict` | Operation not allowed in the resource's current state (for example disk resize on a running VM) |
| `AnotherOperationInProgress` | Wait for the concurrent operation to complete |
| `ResourceNotFound` | Template references a resource that can't be resolved; check the `reference` function parameters |
| `NotFound` | A dependent resource is deployed in parallel with its parent; add a dependency |
| `InvalidResourceReference` | Resource doesn't exist yet or is referenced incorrectly; check dependencies |
| `StorageAccountAlreadyTaken` / `StorageAccountAlreadyExists` | Provide a unique storage account name |
| `DeploymentQuotaExceeded` | Limit of 800 deployments per resource group; delete old deployments from history |
| `LinkedAuthorizationFailed` | Check the account belongs to the same tenant as the resource group being deployed to |

## 4. More detail
```bash
New-AzResourceGroupDeployment -DeploymentDebugLogLevel All ...             # All, RequestContent or ResponseContent; can log secrets
```
Debug logging can expose passwords and `listKeys` results; enable it only while troubleshooting, then remove the debug deployment history.

## Gotchas
- `DeploymentFailed` is a general wrapper; look in the error details for the inner code.
- Debug logging stores request/response content in deployment history; remove that history afterwards.

## Verify
- [ ] Failing operation, resource and inner error code identified and documented in the PR/incident.
- [ ] Re-run succeeds; `az deployment group show ... --query properties.provisioningState` = Succeeded.

## Checked
Date: 2026-10-31. Checked against Microsoft Learn: Common Azure deployment errors, Find error code, Enable debug logging.
- Confirmed: error code meanings in the table, 800-deployment limit, `az deployment group validate` and `az deployment operation group list`, `DeploymentDebugLogLevel` values, secret exposure warning and history removal, Activity log.
- Removed as unconfirmed: `PrincipalNotFound`, `VaultAlreadyExists`, undefined-resource row, `dependsOn`/`@batchSize` advice, CLI `--debug`, correlation-ID and support guidance, portal Operation details path, custom-script gotcha, Bicep linter claim.
Method: documentation only; no commands were run.
