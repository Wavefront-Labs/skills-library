---
id: computing-software.database-administration.sql-server.azure-automation-runbooks-for-database-tasks
name: azure-automation-runbooks-for-database-tasks
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, azure-automation-runbook, managed-identity, powershell]
level: practitioner
status: docs-checked
description: "Run Azure SQL Database maintenance from Azure Automation PowerShell runbooks that sign in with the Automation account's managed identity."
sources:
  - https://learn.microsoft.com/en-us/azure/automation/automation-runbook-types
  - https://learn.microsoft.com/en-us/azure/automation/enable-managed-identity-for-automation
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-azure-ad-user-assigned-managed-identity
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Automation runbooks for database tasks

Use Azure Automation when a scheduled task mixes control-plane work on the Azure resource with T-SQL against the database. The runbook authenticates as the Automation account's managed identity, so no secret is stored.

## Set up
1. Enable a **system-assigned managed identity** on the Automation account (portal, PowerShell, REST API or ARM template). It gets a service principal in the Microsoft Entra tenant.
2. Control plane: assign an Azure role to the identity on the target resource. Assigning roles needs `Microsoft.Authorization/roleAssignments/write` (for example User Access Administrator or Owner). The Learn page uses Contributor only as an example; pick the narrowest role that works.
3. Data plane: the SQL guidance is to create a SQL user from the managed identity in the target database with `CREATE USER ... FROM EXTERNAL PROVIDER`, then grant what the task needs. Provisioning a Microsoft Entra admin is covered in the SQL Database Entra admin article.
   ```sql
   CREATE USER [<AUTOMATION_ACCOUNT_NAME>] FROM EXTERNAL PROVIDER;
   ```
4. Runtime: PowerShell is the recommended runbook type; supported versions are 7.6, 7.4 and 5.1 (7.1 and 7.2 are no longer supported by PowerShell itself). PowerShell 7.x does not support workflows or signed runbooks.

## Sign in from the runbook
```powershell
$AzureContext = (Connect-AzAccount -Identity).context
```
This is the Learn pattern for the system-assigned identity with the current `Az` modules (`Az.Accounts` and others).

## Gotchas
- `#Requires` is not supported in the Azure sandbox or on Hybrid Runbook Workers and can make a job fail.
- PowerShell 7.4/7.6 runbooks need their module dependencies imported explicitly; imports are validated at job run time.
- Do not import `Az.Accounts` 2.4.0 for a PowerShell 7 runtime; Learn warns of unexpected behaviour.
- Enabling the Automation account identity overrides a VM-level system-assigned identity used by hybrid jobs on Azure VMs.

## Verify
A manual test run signs in, performs the task and the job output shows no errors.

## Checked
2026-11-09. Read in part (searched for each claim, not read end to end): the runbook-types and managed-identity Learn pages and the user-assigned managed identity SQL page. Confirmed items above. Removed as unconfirmed: the Ola Hallengren IndexOptimize example, `Set-AzSqlDatabase` scaling, schedule cmdlets, Log Analytics table names, the 3-hour fair-share limit, `Invoke-Sqlcmd` timeout default, access-token code, the role names `SQL DB Contributor` and `db_owner`, and sandbox firewall advice.
Method: documentation only; no commands were run.
