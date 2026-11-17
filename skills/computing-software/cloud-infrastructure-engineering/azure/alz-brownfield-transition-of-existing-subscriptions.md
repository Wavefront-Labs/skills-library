---
id: computing-software.cloud-infrastructure-engineering.azure.alz-brownfield-transition-of-existing-subscriptions
name: alz-brownfield-transition-of-existing-subscriptions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, brownfield-alz, alz-brownfield, management-groups, policy-rollout, migration]
level: advanced
status: docs-checked
description: "Move an existing Azure estate into the ALZ management group hierarchy without outages: policy impact analysis, DoNotEnforce rollout, network adoption and subscription moves."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/enterprise-scale/transition", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance", "https://learn.microsoft.com/azure/governance/policy/concepts/assignment-structure#enforcement-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brownfield transition into Azure landing zones

**Goal:** adopt the ALZ hierarchy and policy baseline over an estate that already runs production, without
deny policies breaking deployments the day subscriptions move.

## 1. Assess
- Inventory subscriptions, owners, existing management groups, policy and RBAC at each scope (Azure Resource Graph helps).
- Classify each subscription: platform (identity, connectivity, management), corp, online, sandbox, decommission.
- Note existing hubs, firewalls, DNS, Log Analytics workspaces you will adopt rather than rebuild.

## 2. Deploy the hierarchy alongside
Deploy ALZ management groups and policy definitions (accelerator) under the tenant root **without** moving
subscriptions. Assign policy initiatives with `enforcementMode: DoNotEnforce` first where you need impact data.

## 3. Impact analysis before moving
- Temporarily assign the target initiatives at the subscription (audit/DoNotEnforce) or move one low-risk
  subscription first.
- Read compliance: every deny-type finding is a future deployment failure; every DINE finding is a future
  remediation change (diagnostics, Defender plans, private DNS records).
- Fix, exempt (with expiry), or parameterise per landing zone.

## 4. Move subscriptions in waves
```bash
az account management-group subscription add --name corp --subscription <subId>
```
- Moving changes inherited RBAC and policy; the caller needs Owner on the subscription (direct assignment) and write permission on the target management group. New writes in the moved subscription are subject to the inherited policies.
- Run remediation tasks deliberately after the move (not all at once for DINE on hundreds of resources).

## 5. Adopt platform pieces
- Existing hub VNet: move into the connectivity subscription (resource move) or re-peer spokes to a new hub
  during a maintenance window. Watch for address overlaps and gateway transit flags.
- Consolidate Log Analytics: repoint diagnostic settings via policy; keep old workspaces for retention period.
- Replace subscription-level legacy policies that duplicate ALZ ones to avoid conflicting results.

## Gotchas
- Subscription moves with Owner-at-subscription users don't remove those assignments - review RBAC separately.
- Deny policies on public network access will block teams' next deploy if they rely on public endpoints - agree timelines.
- Don't flip all assignments to Default enforcement in one go; go initiative by initiative.

## Verify
- [ ] Each wave: compliance baseline captured before, no failed deployments reported after one week, exemptions tracked with expiry.

## Checked

2026-10-28. Confirmed on the CAF transition page and the Azure Policy enforcement mode page: DoNotEnforce mode evaluates without enforcing, a subscription move needs subscription Owner plus write on the target management group, new writes then follow inherited policy. az account management-group subscription add exists (command check). Removed: the Governance Visualizer reference and the write-on-source requirement.

Method: documentation only; no commands were run.
