---
id: computing-software.cloud-infrastructure-engineering.azure.subscription-policies-and-directory-transfer-control
name: subscription-policies-and-directory-transfer-control
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, subscription-policies, leave-tenant, enter-tenant, directory-transfer, exempted-users, subscription-governance, tenant-isolation, change-directory, global-administrator, elevate-access, security-baseline]
level: practitioner
status: docs-checked
description: "Lock a tenant against subscriptions leaving or entering it with Azure subscription policies (Global Admin, elevated access) and an exempted-users list."
sources: ["https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/manage-azure-subscription-policy", "https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscription policies — stop subscriptions walking out of (or into) your tenant

**Goal:** no subscription Owner can move a subscription to another Entra tenant and no foreign
subscription can be dropped into the tenant without the platform team, while a named
exemption list keeps mergers possible.

## 1. What the policy does
Two policies plus an exemption list:
- **Subscriptions leaving a Microsoft Entra ID directory**: *Allow no users (recommended)* or *Allow all users*.
- **Subscriptions entering a Microsoft Entra ID directory**: same two options.
- **Exempted users**: a list of users who bypass both policies.
"Allow all users" means all authorised users on a subscription, including authorised guests,
not all directory users. Default is Allow no users: from 1 May 2026 Microsoft changed the
default so transfers in or out need an explicit global administrator opt-in; an explicitly set
policy is kept. Workflows that relied on the old default break until a global administrator
sets Allow all users.
Risk to know: a user (or guest) can create a subscription in another directory where they hold
billing permissions and transfer it in, which Allow no users prevents.

## 2. Set it
Only global administrators with a direct role assignment can edit, and they must first
**elevate access** (see the elevate-access skill). Then: Azure portal > Subscriptions >
**Manage Policies** on the command bar > set the policies, add or remove exempted users >
**Save changes** (effective immediately). Remove the elevated access afterwards.

## 3. Operate
- Approved transfers (acquisition, divestiture): temporarily add the executing admin to the
  exempted list, do the move, remove them, with a ticket.
- Non-global-administrators can read the policy settings but cannot edit them or see the
  exempted-users list. They can view the global administrators to request changes.
- Subscriptions moved in or out must stay associated with a Billing Tenant so billing continues.

## Gotchas
- The setting is per directory; it cannot allow dev subscriptions to leave while blocking prod.
- Forgetting to drop elevated access afterwards leaves User Access Administrator at root.

## Verify
- [ ] Manage Policies shows both policies on Allow no users and only the intended exempted users (as a global administrator).
- [ ] A non-global-administrator subscription Owner cannot transfer a test subscription.

## Checked
2026-10-28. Confirmed on the Learn pages "Manage Azure subscription policies" and "Elevate access...": option names, default and May 2026 change, prerequisites (direct global administrator, elevate first), portal path, immediate effect, read-only view for others, exempted-users privacy, billing-tenant requirement. Removed (not found in those pages, REST page not readable): the REST `Microsoft.Subscription/policies` calls and property names, `SubscriptionPolicyViolation`, audit operation names, "non-GA exempted ids have no effect", cross-tenant billing and Defender/Secure Score claims, the DenyAction aside, Permit/Permit-no-one wording.
Method: documentation only; no commands were run.
