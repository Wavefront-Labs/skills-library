---
id: computing-software.cloud-infrastructure-engineering.azure.bicep-and-arm-template-deployments
name: bicep-and-arm-template-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, arm-templates, what-if, deployment-scopes, incremental-mode, complete-mode, deployment-stacks, existing-resources, infrastructure-as-code]
level: practitioner
status: docs-checked
description: "Deploy Azure with Bicep/ARM: scopes, what-if gating, incremental vs complete mode, deployment stacks, Key Vault secrets as parameters."
sources: ["https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-modes", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/key-vault-parameter", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-to-subscription"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bicep and ARM deployments: declarative Azure without the JSON

**Goal:** every environment is deployed from a Bicep file by a pipeline that shows
what-if before apply, and no resource is created by hand.

## 1. Scopes and modules
- A file deploys to the resource group by default. Set `targetScope = 'subscription'`
  (also management group and tenant) to deploy higher up; subscription-level files
  commonly create resource groups and then call modules.
- A module reaches another scope with `scope:`, for example `scope: resourceGroup(resourceGroupName)`,
  `scope: subscription(otherSubscriptionID)` or `scope: tenant()`. A module call is a nested
  deployment. The person deploying the parent file needs permission to deploy at each scope it targets.
- Deploy at subscription level with `az deployment sub create`.

## 2. Preview with what-if
- What-if predicts changes without changing anything. It works for resource group, subscription,
  management group and tenant deployments: `az deployment group what-if`, `az deployment sub what-if`,
  `az deployment mg what-if`, `az deployment tenant what-if`.
- `--confirm-with-what-if` (or `-c`) on a `create` command previews and prompts before deploying.
  `--no-pretty-print` returns JSON you can inspect in a script.
- What-if needs write access on the resources plus all operations on `Microsoft.Resources/deployments`.
  It needs Azure CLI 2.14.0 or later (diagnostics for unanalysable parts need CLI 2.75.0 or later).
- Change types include Delete, Ignore and NoChange. Delete appears only for complete-mode JSON
  deployments. When expansion limits are hit, the remaining resources show as Ignore.
- Noise: properties set automatically as defaults during deployment can be reported as deleted
  although they will not change. Unevaluated expressions such as `utcNow()` are shown as written.

## 3. Incremental, complete and deployment stacks
- The default mode is incremental: resources in the resource group but not in the template are
  left alone. Microsoft recommends incremental mode.
- Redeploying a resource reapplies all properties. Properties omitted from the template are reset to
  defaults, so state every non-default value, not just the ones you are changing.
- Subnets: define them in the `subnets` property of the virtual network, not as a separate child
  resource, or a redeploy of the network can lose them.
- Complete mode deletes resources in the resource group that are not in the template. Microsoft says it
  is not recommended and will be gradually deprecated: use deployment stacks for deletes. Run what-if
  first. Complete mode works only on root-level templates, not subscription-level deployments, not the
  portal, and a locked resource group blocks the deletions.
- A deployment stack manages a group of resources as one unit. Removing a resource from the template
  detaches or deletes it according to `actionOnUnmanage`; `--action-on-unmanage` takes `deleteAll`,
  `deleteResources` or `detachAll`. `--deny-settings-mode` takes `none`, `denyDelete` or
  `denyWriteAndDelete`, and it applies to everyone not explicitly excluded (up to 5 excluded
  principals and 200 excluded actions).
- Stacks need Azure CLI 2.61.0 or later. Create them with `az stack group create`, `az stack sub create`
  or `az stack mg create`, each with `--name`, `--template-file`, `--action-on-unmanage` and
  `--deny-settings-mode`; `sub` and `mg` also take `--location`.
- Built-in roles: Azure Deployment Stack Contributor cannot create or delete deny assignments;
  Azure Deployment Stack Owner can.

## 4. Secrets from Key Vault
- Set `enabledForTemplateDeployment` on the vault (`az keyvault update --name <vault> --enabled-for-template-deployment true`).
- The deployer needs `Microsoft.KeyVault/vaults/deploy/action` on the resource group and vault
  (Owner and Contributor have it).
- In Bicep, call `getSecret` on an `existing` Key Vault resource, only inside a module's `params`
  and only for a parameter marked `@secure()`. In a `.bicepparam` file use `az.getSecret()`.
- The vault can be in a different subscription from the deployment target.

## Gotchas
- Changing the location or type of an existing resource fails the deployment; deploy a new resource instead.
- Complete mode with copy loops deletes anything not produced by the resolved loop.

## Verify
- [ ] The pipeline runs what-if and a human or gate reviews Delete changes before create.
- [ ] No pipeline uses `--mode Complete`; deletions go through a deployment stack.
- [ ] Secrets reach templates through `@secure()` parameters sourced from Key Vault.

## Checked
Checked against the five cited Microsoft Learn pages (what-if, deployment modes, deployment stacks, Key Vault parameter, deploy to subscription), each downloaded and read in full. Removed as unconfirmed on those pages: Azure Verified Modules and the module registry, template specs, bicepparam layout, `existing` examples and API versions, `--exclude-change-types`, decompile/export advice, the Bicep versus Terraform comparison, linter settings, and unique-deployment-name advice.
Method: docs-checked 2026-11-09 against the five cited Learn pages; no commands were run.
