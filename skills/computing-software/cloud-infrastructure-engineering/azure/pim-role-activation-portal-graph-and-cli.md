---
id: computing-software.cloud-infrastructure-engineering.azure.pim-role-activation-portal-graph-and-cli
name: pim-role-activation-portal-graph-and-cli
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, pim, pim-activation, role-activation, activate-role, self-activate, selfactivate, deactivate, roleassignmentschedulerequest, az-cli-pim, powershell-pim, activation-automation, token-refresh, pim-approve-requests]
level: practitioner
status: docs-checked
description: "Activate PIM-eligible Entra and Azure roles via portal, Graph, ARM REST and PowerShell with justification/ticket, scheduled start, deactivation, and the token refresh people miss."
sources: ["https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-activate-role", "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-resource-roles-activate-your-roles", "https://learn.microsoft.com/en-us/rest/api/authorization/role-assignment-schedule-requests/create", "https://learn.microsoft.com/en-us/powershell/module/az.resources/new-azroleassignmentschedulerequest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activating PIM roles — portal, Graph, REST, PowerShell, and getting a token that actually has the role

**Goal:** on-call engineers and automation can activate an eligible role in seconds, with the
right justification, and understand why their CLI still says 403 afterwards.

## 1. Portal (humans)
PIM → **My roles** → pick the role type → Eligible assignments → **Activate**, then set duration, an optional
start time, reason and ticket number. See the two PIM activation pages for the current steps.

## 2. Microsoft Graph (Entra roles and groups)
```bash
# Entra directory role
az rest -m POST -u https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignmentScheduleRequests \
  -b '{"action":"selfActivate","principalId":"<MY-OBJECT-ID>","roleDefinitionId":"<ROLE-TEMPLATE-ID>",
       "directoryScopeId":"/","justification":"INC12345 password reset wave",
       "ticketInfo":{"ticketNumber":"INC12345","ticketSystem":"ServiceNow"},
       "scheduleInfo":{"startDateTime":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","expiration":{"type":"afterDuration","duration":"PT2H"}}}'
```
The request body for deactivation uses a different `action`; take it from the Graph roleAssignmentScheduleRequest reference.
PIM for groups uses a separate Graph endpoint; look it up in the Graph reference before scripting it.

## 3. Azure resource roles (ARM)
```bash
SUB=<SUB-ID>; ROLE=<ROLE-DEFINITION-GUID>
az rest -m PUT -u "https://management.azure.com/subscriptions/$SUB/providers/Microsoft.Authorization/roleAssignmentScheduleRequests/$(uuidgen)?api-version=2020-10-01" \
  -b '{"properties":{"requestType":"SelfActivate","principalId":"<MY-OBJECT-ID>",
       "roleDefinitionId":"/subscriptions/'$SUB'/providers/Microsoft.Authorization/roleDefinitions/'$ROLE'",
       "justification":"INC12345","ticketInfo":{"ticketNumber":"INC12345","ticketSystem":"Jira"},
       "scheduleInfo":{"startDateTime":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","expiration":{"type":"AfterDuration","duration":"PT4H"}}}}'
# PowerShell
New-AzRoleAssignmentScheduleRequest -Name (New-Guid) -Scope /subscriptions/$SUB -PrincipalId <id> -RoleDefinitionId <role-def-full-id> -RequestType SelfActivate -Justification "INC12345" -ScheduleInfoStartDateTime (Get-Date).ToUniversalTime() -ExpirationDuration PT4H -ExpirationType AfterDuration
```
The request name must be a new GUID each time. A successful self-activation ends in `Provisioned`; the role's
PIM settings (maximum duration, justification, ticket, MFA) can reject a request.

## 4. The token problem
If an activated role is not visible to a CLI or portal session, sign out and in again (`az logout` then
`az login`) to get a fresh token; cached tokens can predate the activation.

## 5. Approvals (for approvers)
PIM → **Approve requests** → select → Approve or Deny with a justification.

## Gotchas
- Activate at the narrowest eligible scope you have.

## Verify
- [ ] After signing in again, `az role assignment list --assignee <me> --scope <scope>` shows the role and a write action succeeds.
- [ ] The PIM audit history shows the activation with your justification and ticket.

## Checked
2026-10-28. Confirmed on Microsoft Learn (PIM activate Entra roles, PIM activate Azure resource roles, Role Assignment Schedule Requests REST create, `New-AzRoleAssignmentScheduleRequest` pages): Graph `POST /roleManagement/directory/roleAssignmentScheduleRequests` with `selfActivate`, ARM `PUT .../roleAssignmentScheduleRequests/{name}?api-version=2020-10-01` with `SelfActivate`, `AfterDuration` expiration, `ticketInfo` fields, PowerShell cmdlet parameters, `Provisioned` status. Removed: PIM-for-groups request, Graph PowerShell cmdlet and scope, `wids` token claim detail, approval PATCH route and 1-day timeout, error code names, eligibility query, and several gotchas the pages do not state.
Method: documentation only; no commands were run.
