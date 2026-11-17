---
id: computing-software.database-administration.sql-server.deploying-azure-sql-with-bicep-and-cli
name: deploying-azure-sql-with-bicep-and-cli
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-agent, azure-sql-database, bicep-azure-sql, az-sql, infrastructure-as-code, arm-templates]
level: practitioner
status: docs-checked
description: "Deploy Azure SQL logical servers and databases repeatably with Bicep and az sql: Entra-only admin, SKU, backup redundancy, private endpoint and what-if checks."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-bicep-quickstart
  - https://learn.microsoft.com/en-us/cli/azure/sql/db
  - https://learn.microsoft.com/en-us/azure/templates/microsoft.sql/servers/databases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Azure SQL with Bicep and Azure CLI

## Bicep
```bicep
param location string = resourceGroup().location
param serverName string
param dbName string
param adminGroupName string
param adminGroupObjectId string

resource sql 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: serverName
  location: location
  properties: {
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
    administrators: {
      administratorType: 'ActiveDirectory'
      azureADOnlyAuthentication: true          // no SQL logins at all
      login: adminGroupName
      sid: adminGroupObjectId
      principalType: 'Group'
      tenantId: subscription().tenantId
    }
  }
}

resource db 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sql
  name: dbName
  location: location
  sku: { name: 'GP_Gen5', tier: 'GeneralPurpose', family: 'Gen5', capacity: 4 }
  properties: {
    zoneRedundant: true
    requestedBackupStorageRedundancy: 'Geo'     // Local | Zone | Geo | GeoZone
    maxSizeBytes: 274877906944
  }
}
```
Add retention-policy, auditing and private-endpoint resources as child/sibling resources;
look up their exact types and properties in the ARM template reference.

```bash
az deployment group what-if  -g rg-data -f sql.bicep -p @sql.prod.parameters.json
az deployment group create   -g rg-data -f sql.bicep -p @sql.prod.parameters.json
```
Run `what-if` in CI before `create` to see what a deployment would change.

## Azure CLI for day-two tasks
```bash
az sql db list -g rg-data -s sql-prod -o table
az sql db update -g rg-data -s sql-prod -n sales --service-objective GP_Gen5_8   # scale
az sql db copy   -g rg-data -s sql-prod -n sales --dest-name sales_copy
az sql db restore -g rg-data -s sql-prod -n sales --dest-name sales_pitr --time 2026-10-18T08:30:00Z
az sql server firewall-rule create -g rg-data -s sql-prod -n office --start-ip-address 203.0.113.10 --end-ip-address 203.0.113.10
```

## Gotchas
- Choose `requestedBackupStorageRedundancy` upfront; check the docs before changing it on a live database.
- Don't keep SQL admin passwords in parameter files; with `azureADOnlyAuthentication` there is none.

## Verify
`az sql db show -g rg-data -s sql-prod -n sales --query "{sku:currentSku.name,backup:requestedBackupStorageRedundancy,zr:zoneRedundant}"`
matches the template, and a second `what-if` shows no changes.

## Checked
2026-11-01. Confirmed against the ARM template reference pages for `Microsoft.Sql/servers` and `servers/databases` (API version 2023-08-01-preview; administrators fields, `minimalTlsVersion`, `publicNetworkAccess`, `zoneRedundant`, `maxSizeBytes`, `requestedBackupStorageRedundancy` values Local/Zone/Geo/GeoZone) and the `az sql db` and `az sql server firewall-rule` CLI reference (commands and flags). Removed: PITR day range, private endpoint group id, Hyperscale and future-backup redundancy notes, what-if Modify claim, scale-disconnect note, database-object note.
Method: documentation only; no commands were run.
