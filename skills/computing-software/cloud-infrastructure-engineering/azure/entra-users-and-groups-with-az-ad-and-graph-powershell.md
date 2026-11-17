---
id: computing-software.cloud-infrastructure-engineering.azure.entra-users-and-groups-with-az-ad-and-graph-powershell
name: entra-users-and-groups-with-az-ad-and-graph-powershell
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, az-ad, microsoft-graph-powershell, users, groups, advanced-queries]
level: practitioner
status: docs-checked
description: "Script Entra users and groups with az ad and the Microsoft Graph PowerShell SDK: create, query with filters, membership changes, and advanced queries."
sources: ["https://learn.microsoft.com/cli/azure/ad/user", "https://learn.microsoft.com/cli/azure/ad/group", "https://learn.microsoft.com/powershell/microsoftgraph/get-started", "https://learn.microsoft.com/graph/aad-advanced-queries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra users and groups with az ad and Graph PowerShell

**Goal:** automate identity admin with supported tooling: `az ad` (calls Microsoft Graph) or the Microsoft.Graph
PowerShell SDK.

## az ad (good for quick ops and pipelines)
```bash
az ad user create --display-name "Ana Silva" --user-principal-name ana@contoso.com \
  --password '<temp>' --force-change-password-next-sign-in true
az ad user list --filter "startswith(displayName,'Ana')" --query "[].{upn:userPrincipalName,id:id}" -o table
az ad group create --display-name sg-app-readers --mail-nickname sg-app-readers
az ad group member add --group sg-app-readers --member-id $(az ad user show --id ana@contoso.com --query id -o tsv)
az ad group member check --group sg-app-readers --member-id <objectId>
az ad signed-in-user show --query id -o tsv
```
`--display-name`, `--password` and `--user-principal-name` are required on `az ad user create`; `az ad group create`
requires `--display-name` and `--mail-nickname`. For properties `az ad` does not expose, use `az rest` against Graph.

## Microsoft Graph PowerShell
```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All"
Get-MgUser -All -Filter "department eq 'Finance'" -Property id,displayName,department
```
Use the Microsoft.Graph.Users and Microsoft.Graph.Groups cmdlet reference for user and group create and membership
cmdlets; confirm cmdlet names and required permissions there before scripting.

## Advanced queries
`$filter` operators such as `endsWith`, `ne` and `not`, plus `$count`, are advanced queries: set the
`ConsistencyLevel` header to `eventual` and, except for `$search`, use `$count=true`:
```powershell
Get-MgUser -Filter "accountEnabled ne true" -CountVariable CountVar -ConsistencyLevel eventual
```
```bash
az rest --method GET --headers ConsistencyLevel=eventual \
  --url "https://graph.microsoft.com/v1.0/users?\$count=true&\$filter=endsWith(mail,'@contoso.com')"
```

## Verify
- [ ] The script is idempotent (checks existence before create) and the signed-in scopes cover the calls.

## Checked
2026-10-27. Confirmed against the az ad user, az ad group and signed-in-user CLI reference, Learn "Advanced query
capabilities on Microsoft Entra ID objects" and Microsoft Graph PowerShell get-started examples (`Connect-MgGraph
-Scopes`, `Get-MgUser`, ConsistencyLevel and -CountVariable). Removed (not found in fetched pages): MSOnline/AzureAD
retirement statement, `New-MgUser`, `New-MgGroupMember`, `Remove-MgGroupMemberDirectoryObjectByRef`, unattended
certificate/managed-identity connect, 100-item page size, `az ad list` auto-paging, UsageLocation and signInActivity
permission notes, and submodule install advice.
Method: documentation only; no commands were run.
