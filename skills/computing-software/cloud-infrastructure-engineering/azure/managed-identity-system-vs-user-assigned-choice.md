---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-system-vs-user-assigned-choice
name: managed-identity-system-vs-user-assigned-choice
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, system-assigned, user-assigned, rbac, iac, blast-radius]
level: practitioner
status: docs-checked
description: "Decide between system-assigned and user-assigned managed identities per workload: lifecycle, pre-provisioned RBAC, sharing, rate limits and blast radius."
sources: ["https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview", "https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations", "https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/managed-identities-faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose system- vs user-assigned managed identity

**Goal:** the right identity type per workload so role assignments exist before first boot, rapid scale-out doesn't hit
Entra limits, and one compromised app can't use another's permissions.

## Comparison
| | System-assigned | User-assigned |
|---|---|---|
| Lifecycle | Shared with the resource; created and deleted with it | Independent Azure resource |
| Sharing | Cannot be shared | Can be shared across resources |
| RBAC before resource exists | No: role assignments can't be created in advance | Yes: configure identity and roles first |
| Name / audit | Service principal named after the resource (slots: `<app>/slots/<slot>`) | Name you choose |

Microsoft's guidance: user-assigned identities are more efficient in a broader range of scenarios; system-assigned fits
when each resource needs its own identity or unique permissions, or its permissions must be removed with it.

## Use user-assigned when
- Resources are created rapidly (ephemeral compute): many system-assigned identities can exceed the Entra rate limit
  for creating identities and the limit on directory resources; a deleted system-assigned identity counts toward the
  limit until fully purged after 30 days.
- Many resources need the same access: one identity means fewer role assignments (four VMs and two storage accounts:
  two assignments instead of eight) and avoids replication delays from many new principals.
- Creating the resource must not need permission to create role assignments, or security must pre-grant roles.
- Identity creation needs an approval process: one shared identity needs fewer approvals.

## Use system-assigned when
- You need to log which **resource** (not identity) acted, or permissions must disappear when the resource is deleted.
- A single resource has its own unique permission set.

## Blast radius rule
Don't share one user-assigned identity across **unrelated** workloads; share only within a workload boundary (same
team, same data access). Pick a naming convention such as `id-<workload>-<env>` and keep it in the workload resource group.

## IaC pattern
Declare the user-assigned identity first, assign roles to its `principalId` at the narrowest scope (set the principal
type to service principal on the assignment), then attach the identity to the compute resource. Look up built-in role
IDs from the Azure built-in roles list rather than copying them from memory. With several identities on one resource,
tell the SDK which one to use by client ID; confirm the setting name in the SDK's identity documentation.

## Gotchas
- Deleting an identity leaves role assignments that show as unknown principals; clean them up.
- A user-assigned identity can't be moved to another resource group or subscription (create a new one).

## Verify
- [ ] Workload doc records identity type and why.
- [ ] `az identity show -n id-orders-prd -g <rg> --query principalId` has the expected role assignments only.

## Checked
2026-10-27. Confirmed against Learn "What are managed identities" and "Best practice recommendations for managed
identities" and the FAQ: lifecycle/sharing/pre-provisioning, rate-limit and 30-day purge note, 8-vs-2 role assignments
example, audit and permission-lifecycle guidance. Removed: federated-credential row, "many per resource up to a limit",
the 4,000-per-subscription limit and 1000-VM example, the Bicep block (API versions and role GUID unconfirmed),
specific replication-delay claim about `principalType`, `AZURE_CLIENT_ID` setting name, and the cross-tenant loss
statement (see the limits skill).
Method: documentation only; no commands were run.
