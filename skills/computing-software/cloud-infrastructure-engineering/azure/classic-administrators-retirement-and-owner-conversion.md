---
id: computing-software.cloud-infrastructure-engineering.azure.classic-administrators-retirement-and-owner-conversion
name: classic-administrators-retirement-and-owner-conversion
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, classic-administrators, co-administrator, service-administrator, asm-retirement]
level: practitioner
status: docs-checked
description: "Find leftover classic Service Administrator and Co-Administrator access after the 2024 retirement and replace it with scoped Azure RBAC role assignments."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/classic-administrators", "https://learn.microsoft.com/azure/role-based-access-control/role-assignments-list-portal"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Classic administrators retirement

**Goal:** no one's access depends on the retired classic roles (Service Administrator, Co-Administrator),
and the equivalent access is explicit, least-privilege Azure RBAC. The Account Administrator role (billing
owner) is not being deprecated and needs no conversion.

## Background
Classic administrator roles were tied to Azure Service Manager and were retired on 31 August 2024. Per Microsoft Learn, from December 2025 Azure automatically assigned the **Owner** role at subscription scope to public-cloud users who still held Co-Administrator or Service Administrator (assignment description: "The Classic Admin role was converted to an Azure Owner role on behalf of the user due to Classic Admin retirement"), and as of May 2026 the Classic Administrators tab is removed from the portal. Co-Administrators had Owner-equivalent access to the whole subscription and were invisible to most RBAC reviews, so review those auto-created Owner assignments and replace them with least privilege.

## Inventory
```bash
az role assignment list --subscription <subId> --role Owner --all \
  --query "[?contains(description,'Classic Admin role was converted')].{who:principalName,scope:scope}" -o table
```
The Classic administrators tab was removed from the portal in May 2026; the converted Owner assignments carry the description above.

## Convert
1. For each Co-Administrator decide the real need - usually Contributor or Reader at a resource group, not Owner at subscription.
2. Create the RBAC assignment (ideally PIM-eligible):
```bash
az role assignment create --assignee <upn-or-objectId> --role Contributor --scope /subscriptions/<subId>/resourceGroups/<rg>
```
3. Remove the auto-created Owner assignment once the scoped role is in place (the classic entries themselves are retired).
4. Service Administrator: for Azure billing access move the person to the correct billing role (Account owner /
   Billing account owner) and give subscription Owner via RBAC only if justified.

## Gotchas
- Azure classic resources and Azure Service Manager are retired too; automation that still targets them needs moving to Azure Resource Manager (Az / CLI).
- Owner granted as a like-for-like replacement just recreates the over-privilege; review with the business owner.

## Verify
- [ ] No classic administrators remain; access review on subscription Owners lists only expected (preferably PIM-eligible) principals.

## Checked

Date: 2026-10-28.

Confirmed against Learn (classic administrator roles retirement): retirement on 31 August 2024, automatic Owner assignment at subscription scope from December 2025 with the quoted description, Classic Administrators tab removed May 2026, Account Administrator not deprecated and needing no conversion.
Removed: the `--include-classic-administrators` inventory command (flagged by check_commands.py; replaced with a query on the converted Owner assignments), ASM cmdlet and Cloud Services claims.

Method: documentation only; no commands were run.
