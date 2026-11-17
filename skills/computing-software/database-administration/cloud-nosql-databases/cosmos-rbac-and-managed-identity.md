---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-rbac-and-managed-identity
name: cosmos-rbac-and-managed-identity
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-rbac-and-managed-identity, cosmos-security, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use Microsoft Entra ID instead of account keys for data access."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/role-based-access-control
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb/sql/role/assignment
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC and managed identity

**Goal:** Use Microsoft Entra ID instead of account keys for data access.

## Steps
- Assign data-plane roles: az cosmosdb sql role assignment create -a ACCOUNT -g RG --role-definition-name "Cosmos DB Built-in Data Contributor" --principal-id PRINCIPAL_ID --scope "/"
- Have the application authenticate with a Microsoft Entra identity, such as a managed identity, instead of the account key.
- Disable key-based authentication: az cosmosdb update --disable-local-auth true (the RBAC page does the same by setting properties.disableLocalAuth with az resource update).
- Control-plane roles (Azure RBAC) are separate from the native data-plane roles, and you need control-plane access to create data-plane definitions and assignments.

## Gotcha
Disabling local auth breaks tools and apps still using keys; migrate them first.

## Checked

2026-11-03. Confirmed against "Configure role-based access control with Microsoft Entra ID" (built-in Data Reader and Data Contributor roles, scope "/", managed identity for applications, disabling key-based auth, control plane versus data plane) and the az cosmosdb sql role assignment create reference (--account-name, --resource-group, --principal-id, --scope required; --role-definition-name optional) and az cosmosdb update (--disable-local-auth).
Removed: the DefaultAzureCredential class name (not on the page).
Method: documentation only; no commands were run.

## Verify
- [ ] The app reads and writes using the managed identity and key-based calls are rejected.
