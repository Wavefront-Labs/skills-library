---
id: computing-software.cloud-infrastructure-engineering.azure.export-and-decompile-arm-templates-to-bicep
name: export-and-decompile-arm-templates-to-bicep
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, bicep-decompile, decompile-arm, export-template, iac-adoption, aztfexport]
level: practitioner
status: docs-checked
description: "Bring existing Azure resources under IaC: export templates (portal, CLI, Bicep export), decompile ARM JSON to Bicep, insert resources by ID, and clean up the output."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/bicep/decompile", "https://learn.microsoft.com/azure/azure-resource-manager/templates/export-template-cli", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/visual-studio-code#insert-resource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and decompile ARM to Bicep

**Goal:** a clean, parameterised Bicep starting point for resources that were built by hand.

## Export
```bash
az group export --name rg-app --include-parameter-default-value > rg-app.json
az group export --name rg-app --resource-ids <id1> <id2> > subset.json
```
Portal: resource group (or resource) > Export template; the export can be a Bicep file or ARM JSON.

## Decompile
```bash
az bicep decompile --file rg-app.json            # writes rg-app.bicep, warns on anything it can't map
az bicep decompile-params --file azuredeploy.parameters.json
```
VS Code Bicep extension: **Insert Resource** (paste a resource ID, get the Bicep for that one resource) and
"Paste JSON as Bicep".

## Clean-up checklist (exported code is not production code)
- Remove read-only/runtime properties (`provisioningState`, `etag`, status fields).
- Replace hard-coded IDs, names and locations with parameters/variables; use `resourceId()`/symbolic references.
- Secrets are never exported (passwords, keys, connection strings) - add `@secure()` params or Key Vault references.
- Collapse child resources into parents where cleaner (subnets in VNets) - but avoid subnet churn: decide one style.
- Some resource types or properties can't be exported; compare with the live resource.
- Microsoft's export page warns exported templates are not production-ready: prefer hand-written Bicep for new resources.
- Pin API versions deliberately; exported ones may be old.
- Run the linter, then **what-if** against the live resource group: the goal is *no changes* before you touch anything.

## Gotchas
- Decompilation is best-effort: there is no guaranteed mapping from ARM JSON to Bicep, so expect warnings and fixes, and it can fail.
- Exporting a busy RG produces thousands of lines; export per workload, not per subscription.

## Verify
- [ ] what-if against the existing RG reports NoChange (or only intended changes) for every resource.

## Checked
2026-10-28. Confirmed on the Bicep decompile and export-template-cli pages: `az group export`, export as Bicep or JSON, best-effort decompile with warnings, Insert Resource and Paste JSON as Bicep in VS Code. check_commands confirmed all az commands and flags. Removed: `resourceGuid`, the aztfexport section, the `az resource show` suggestion.
Method: documentation only; no commands were run.
