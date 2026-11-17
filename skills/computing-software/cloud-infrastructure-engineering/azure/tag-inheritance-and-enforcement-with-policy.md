---
id: computing-software.cloud-infrastructure-engineering.azure.tag-inheritance-and-enforcement-with-policy
name: tag-inheritance-and-enforcement-with-policy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, tags, tag-inheritance, require-tag, inherit-tag, azure-policy, modify-effect, cost-allocation-tags]
level: practitioner
status: docs-checked
description: "Enforce and inherit Azure tags: require tags on resource groups, inherit to resources with Modify policies, remediate existing resources and enable cost tag inheritance."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/management/tag-policies", "https://learn.microsoft.com/azure/governance/policy/tutorials/govern-tags", "https://learn.microsoft.com/azure/cost-management-billing/costs/enable-tag-inheritance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag inheritance and enforcement via Policy

**Goal:** every resource carries `CostCenter`, `Owner`, `Environment` without relying on
engineers to type them, and cost reports group cleanly.

## Pattern
1. **Require** tags on resource groups (Deny) — humans tag once, at the RG.
2. **Inherit** from RG to resources (Modify) — automatic, fixes drift.
3. **Cost Management tag inheritance** — applies billing, subscription and resource group tags to child resource usage records (not to the resources themselves).

## Built-in definitions
| Purpose | Built-in name |
|---|---|
| Deny RG without tag | *Require a tag on resource groups* |
| Deny resource without tag | *Require a tag on resources* (does not apply to resource groups) |
| Inherit if missing | *Inherit a tag from the resource group if missing* |
| Always overwrite from RG | *Inherit a tag from the resource group* |
| Add default value | *Add a tag to resources* / *Add or replace a tag on resources* (Modify; resource-group and subscription variants also exist) |
| Inherit from subscription | *Inherit a tag from the subscription* (and the *if missing* variant) |
| Legacy | *Append a tag ...* definitions use Append and do not remediate existing resources |
Initiative for three tags = three inherit-if-missing references with `tagName` parameters.

Modify applies when a resource is created or updated; existing resources are fixed by a remediation task (Learn: modify policies use remediation tasks to alter existing non-compliant resources). Modify assignments need a managed identity with enough rights to change tags; see the Azure Policy remediation how-to for the exact role.

## Cost Management tag inheritance
Available for EA, MCA and MPA (with Azure plan subscriptions) accounts; set at the EA billing account, MCA billing profile or subscription scope (Cost Management > Settings > Configuration, Manage billing profile or Manage subscription, then Tag inheritance > Edit). Needs Cost Management Contributor on a subscription, Enterprise Administrator on EA, or Billing profile contributor on MCA to edit.
By default a matching resource tag wins; you can switch so the inherited tag overrides. Usage records update in about 8-24 hours and only the current month is updated (enabled on 20 Oct updates from 1 Oct using the tags as of 20 Oct). Purchases or resources that emit no usage at subscription scope do not get subscription tags.

## Gotchas
- Not all resource types support tags; check Learn's "Tag support for Azure resources" table.
- Values differing in case (`Prod` vs `prod`) can split reports; consider a Require-tag-and-value policy to fix the allowed values.
- If a tag exists with a different value, the "if missing" definitions leave it unchanged; the others replace it.

## Verify
- [ ] Count of resources missing the tag trends to 0 after remediation.
- [ ] Creating an RG without `CostCenter` is denied.
- [ ] Cost analysis grouped by tag `CostCenter` (Group by list) shows no "untagged" bucket beyond expected; budgets can filter on inherited tags 24 hours after enabling.

## Checked
2026-10-31. Confirmed on the tag-policies, govern-tags and enable-tag-inheritance Learn pages: built-in definition names, effects and behaviours, tag inheritance account types, scopes, permissions, override option, 8-24 hour update and current-month scope. Removed: the CLI block (policy GUID, `--mi-system-assigned` and remediation flags unconfirmed), the Tag Contributor / AuthorizationFailed claim, tag count and length limits, the child-resource deny gotcha, and the marketplace example.
Method: documentation only; no commands were run.
