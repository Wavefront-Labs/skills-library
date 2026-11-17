---
id: computing-software.cloud-infrastructure-engineering.azure.resource-organisation-and-rbac
name: resource-organisation-and-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, management-groups, subscriptions, resource-groups, azure-rbac, entra-id, role-assignments, custom-roles, pim, azure-policy, deny-assignments, managed-identity, workload-identity-federation, tags, resource-locks, cannotdelete, az-cli, landing-zone, caf, abac, deployifnotexists, scope-inheritance]
level: practitioner
status: draft
description: "Organise Azure with management groups, subscriptions and resource groups; assign Entra RBAC at the right scope; enforce with Policy, tags, locks and managed identities."
sources: ["https://learn.microsoft.com/en-us/azure/governance/management-groups/overview", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources", "https://learn.microsoft.com/en-us/azure/role-based-access-control/delegate-role-assignments-overview", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure resource organisation and RBAC — scope everything deliberately

**Goal:** a hierarchy where access and policy are assigned once at the right level and
inherited downward, workloads authenticate with managed identities, and nobody holds
standing Owner.

## 1. Build the hierarchy
Tenant root group › management groups › subscriptions › resource groups › resources.
Everything assigned at a scope (RBAC, Policy) **inherits down**.
- Management groups follow the CAF shape: `platform` (identity, management,
  connectivity), `landingzones` (`corp`, `online`), `sandbox`, `decommissioned`.
  A management group tree supports up to six levels of depth; keep it to 3-4.
- **Subscription = billing, quota and blast-radius boundary.** One per workload per
  environment (`app1-prod`, `app1-nonprod`) is the norm; subscriptions are cheap.
- **Resource group = lifecycle unit.** Things deleted together live together. A
  resource sits in exactly one RG; RG location only stores metadata.
- Move subscriptions: `az account management-group subscription add --name corp --subscription <SUB_ID>`.

## 2. Assign RBAC at the narrowest sensible scope
- Built-in roles first: Reader, Contributor, Owner, **User Access Administrator**, and
  data-plane roles such as *Storage Blob Data Reader* or *Key Vault Secrets User*.
  Contributor does **not** grant data access when the resource uses Entra auth
  (e.g. blob data, Key Vault with RBAC permission model).
- Assign to **Entra groups**, not users:
  ```bash
  az role assignment create --assignee-object-id <GROUP_OBJECT_ID> \
    --assignee-principal-type Group --role "Contributor" \
    --scope /subscriptions/<SUB_ID>/resourceGroups/rg-app1-prod
  ```
- Owner and User Access Administrator only via **PIM** (Privileged Identity
  Management, Entra ID P2) eligible assignments with approval and time limits.
- Delegate role-assignment rights safely with **conditions** on Role Based Access
  Control Administrator (constrain which roles a delegate can assign).
- Custom roles: list `Actions`, `NotActions`, `DataActions`, `AssignableScopes`.
  `NotActions` subtracts from that role only; it is not a deny.
- Real denies come from **deny assignments**, not from RBAC roles you write (see the deny-assignments article for how they are created).

## 3. Enforce with Azure Policy
- Assign initiatives at management-group scope. Effects include `Audit`, `AuditIfNotExists`, `Modify` (e.g. inherit tags from RG),
  `DeployIfNotExists` (e.g. diagnostic settings), `Deny`, `DenyAction` (block delete).
- `Modify` and `DeployIfNotExists` need a managed identity on the assignment plus a
  role for it; existing resources need a **remediation task**.
- Typical baseline: allowed locations, deny public IPs on NICs in corp, require tags
  `owner`, `cost-centre`, `env`, enforce TLS 1.2+, deploy diagnostics to Log Analytics.
- Use exemptions (with expiry) rather than carving holes in definitions.

## 4. Identities for workloads
- **System-assigned** managed identity: lives and dies with the resource.
  **User-assigned**: reusable, survives redeploys, pre-grantable — preferred for
  anything provisioned by IaC.
- CI/CD and external workloads: **workload identity federation** on an app
  registration or user-assigned identity (federated credential with GitHub
  `subject` like `repo:example-org/app:environment:prod`). No client secrets.
- AKS: Microsoft Entra Workload ID (the old pod-identity add-on is deprecated).

## 5. Tags and locks
- Tags do not inherit by default; use the Policy `Modify` effect to copy from RG.
  Limit is 50 tag name-value pairs per resource, resource group and subscription; some resource types do not support tags.
- Locks: `CanNotDelete` or `ReadOnly` at RG or resource level, inherited by children:
  `az lock create --name nodelete --lock-type CanNotDelete --resource-group rg-app1-prod`.

## Gotchas
- `ReadOnly` locks block more than you think: e.g. listing storage account keys is a
  POST, so apps and portal blades break; scaling an App Service plan fails.
- Locks apply to control-plane operations only; they do not stop data deletion inside
  a storage account or database.
- RBAC changes can take several minutes to propagate (cached tokens); a fresh
  assignment "not working" often just needs a new token (`az account get-access-token`).
- Removing a principal leaves orphaned assignments shown as "Identity not found";
  clean them up, they clutter audits.
- Role assignment limits are 5,000 per subscription and 500 per management group — group-based assignment avoids hitting them.
- Moving a resource between subscriptions changes its ID; RBAC assignments and some
  diagnostics do not follow.

## Verify
- [ ] Every subscription sits under a non-root management group with the baseline initiative assigned.
- [ ] No permanent Owner assignments for humans; PIM eligibility used instead.
- [ ] `az role assignment list --all --query "[?principalType=='User']"` returns little or nothing.
- [ ] Policy compliance shows required tags and allowed locations with remediation tasks run.
- [ ] Workloads and pipelines use managed identities or federated credentials, no client secrets.
- [ ] Production RGs carry a `CanNotDelete` lock.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone
