---
id: computing-software.cloud-infrastructure-engineering.azure.azure-rbac-and-governance
name: azure-rbac-and-governance
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, policy-effects, deny, modify, deployifnotexists, denyaction, custom-roles, deployment-stacks, deny-settings]
level: advanced
status: docs-checked
description: "Azure governance guardrails: choosing Policy effects and evaluation order, layered assignments, custom role limits, deployment stack deny settings."
sources: ["https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks", "https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles", "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure RBAC and governance: effects, custom roles, deployment stack deny settings

**Goal:** guardrails that are chosen deliberately, roll out safely and stay in code. The
hierarchy, built-in roles and baseline assignments are in
`computing-software.cloud-infrastructure-engineering.azure.resource-organisation-and-rbac`.

## 1. Pick the Policy effect
- Each policy definition has one effect in its `policyRule`. Supported effects: addToNetworkGroup,
  append, audit, auditIfNotExists, deny, denyAction, deployIfNotExists, disabled, manual, modify, mutate.
- Parameterise the effect with `allowedValues` so one definition can be assigned as audit and later
  switched to deny. Not every effect is interchangeable: audit, deny and modify or append often
  are; auditIfNotExists and deployIfNotExists often are; manual is not; disabled is interchangeable
  with any effect. auditIfNotExists needs extra detail in the rule that audit does not, because it
  judges a child or extension resource rather than the resource's own properties.
- Typical rollout: start with an audit-type effect to measure, then move to deny or a remediating
  effect once owners are warned.

## 2. Order of evaluation
On create or update, Azure Policy evaluates all applicable assignments. In Resource Manager mode the
order before the resource provider is: disabled, then append and modify (they can change the
request so that an audit or deny no longer triggers), then deny (before audit, to avoid double
logging), then audit, manual, auditIfNotExists, and denyAction last. After the provider returns
success, auditIfNotExists and deployIfNotExists evaluate. A PATCH that changes only tags is evaluated
only against policies whose conditions inspect tags.

## 3. Layered assignments
Each assignment is evaluated independently, at the same or different scopes, so nothing slips through
a scope gap. The net effect is cumulative and most restrictive: two overlapping deny policies can
block a resource outright. If a resource must still be created, review the exclusions on each
assignment.

## 4. Custom roles
- Start from a built-in role and change it; add control plane operations to `Actions`/`NotActions` and
  data plane operations to `DataActions`/`NotDataActions`.
- Wildcards are allowed in action strings, but Microsoft recommends listing actions explicitly because
  future actions under a wildcard grant access you may not want. Only one wildcard per action string.
- Limits: 5,000 custom roles per tenant (2,000 for Azure operated by 21Vianet); maximum 2,000
  `AssignableScopes`; `AssignableScopes` cannot be the root scope `/` or contain wildcards; only one
  management group may be listed.
- A custom role with `DataActions` cannot be assigned at management group scope. You can still list one
  management group in its `AssignableScopes` and assign it in the subscriptions within it.
- Creating, updating or deleting a role needs `Microsoft.Authorization/roleDefinitions/write` on all of
  its `AssignableScopes`. Before deleting a custom role, remove every assignment of it (including
  eligible assignments in Privileged Identity Management), or the delete fails with
  `RoleDefinitionHasAssignments`.
- Use the role ID rather than its name in scripts, because the ID does not change if the role is renamed.

## 5. Deployment stack deny settings
- A deployment stack blocks unwanted changes to the resources it manages. `--deny-settings-mode` takes
  `none`, `denyDelete` or `denyWriteAndDelete`; the restriction applies to everyone unless explicitly
  excluded.
- Exclude identities with `--deny-settings-excluded-principals` (up to 5 Entra principal IDs; a group
  object ID is recommended) and operations with `--deny-settings-excluded-actions` (up to 200).
- The deny assignment lives where the stack lives. A stack at subscription scope that deploys into a
  resource group keeps developers with resource-group access from editing the stack or its deny assignment.
- The built-in role Azure Deployment Stack Contributor cannot create or delete deny assignments; Azure
  Deployment Stack Owner can.

## Verify
- [ ] Every deny policy was assigned as an audit effect first and its compliance reviewed.
- [ ] Overlapping assignments at different scopes were reviewed for cumulative deny.
- [ ] Custom roles list explicit actions and have no assignments left before deletion.
- [ ] Excluded principals on deny settings are groups the platform team controls.

## Checked
Read in full: the Azure Policy effect basics page, the Azure custom roles page, and the Bicep deployment stacks page (all downloaded as text). Removed as unconfirmed on those pages: policy aliases and the Indexed and All modes, EPAC, exemption categories, compliance scan timing, remediation tasks, ABAC conditions, PIM for groups, access reviews, and the claim that Deny leaves existing resources untouched.
Method: docs-checked 2026-11-09 against the three cited Learn pages; no commands were run.
