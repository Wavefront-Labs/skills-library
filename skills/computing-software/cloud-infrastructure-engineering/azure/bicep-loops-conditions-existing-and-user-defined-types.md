---
id: computing-software.cloud-infrastructure-engineering.azure.bicep-loops-conditions-existing-and-user-defined-types
name: bicep-loops-conditions-existing-and-user-defined-types
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, bicep-loops, user-defined-types, existing-keyword, conditional-deployment, lambda-functions]
level: practitioner
status: docs-checked
description: "Write expressive Bicep: for-loops with index and batchSize, conditional resources, existing references across scopes, user-defined and imported types, nullable and lambda helpers."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/bicep/loops", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/user-defined-data-types", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/existing-resource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bicep loops, conditions, existing and types

**Goal:** one typed, data-driven template instead of copy-pasted resources.

## User-defined types
```bicep
// types.bicep
@export()
type subnetType = {
  name: string
  addressPrefix: string
  @description('Resource ID of an NSG to attach')
  nsgId: string?          // optional (nullable)
  delegation: ('Microsoft.Web/serverFarms' | 'Microsoft.ContainerInstance/containerGroups')?
}
```
```bicep
// main.bicep
import { subnetType } from 'types.bicep'
param subnets subnetType[]
```
Mark a type with `@export()` so other Bicep files can import it. Resource API versions in these samples are illustrative; take current ones from the template reference.

## Loops
```bicep
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: { addressPrefixes: [ vnetPrefix ] }
    subnets: [for s in subnets: {
      name: s.name
      properties: {
        addressPrefix: s.addressPrefix
        networkSecurityGroup: s.?nsgId == null ? null : { id: s.nsgId! }
      }
    }]
  }
}

@batchSize(2)       // deploy two at a time instead of all in parallel
resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = [for (name, i) in storageNames: {
  name: name
  location: location
  sku: { name: i == 0 ? 'Standard_GZRS' : 'Standard_LRS' }
  kind: 'StorageV2'
}]
output saIds array = [for (n, i) in storageNames: sa[i].id]
```
Loop limit: 800 iterations per loop. Filter with lambdas: `filter(subnets, s => s.?delegation != null)`.

## Conditions
```bicep
resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = if (enablePrivateEndpoint) { ... }
output peId string = enablePrivateEndpoint ? pe.id : ''
```
Guard outputs and dependants of a conditional resource with the same condition.

## existing (reference, don't deploy)
```bicep
resource hubVnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: 'vnet-hub'
  scope: resourceGroup(hubSubId, 'rg-hub')
}
```

## Handy operators
`.?` safe dereference, `??` coalesce, `!` non-null assertion, `union()`, `items()` to loop over objects.

## Verify
- [ ] `bicep build` clean; what-if shows one subnet per array element; removing an element plans a delete (expected).

## Checked
2026-10-28. Confirmed on the Bicep loops and user-defined types pages: 800 iteration limit, `@batchSize`, `@export()` for types, nullable types. Removed: `toObject()` and `reduce()` (not on fetched pages), the build-time error claim, the runtime-failure claim about conditional resources.
Method: documentation only; no commands were run.
