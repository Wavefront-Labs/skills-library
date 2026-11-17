---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.resource-hierarchy
name: resource-hierarchy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, resource-hierarchy, management-groups, organizational-units, gcp-folders]
level: practitioner
status: draft
description: "Design the cloud resource hierarchy: AWS OUs and accounts, Azure management groups and subscriptions, GCP folders and projects, for policy and billing."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/recommended-ous-and-accounts.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups", "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource hierarchy design

The hierarchy is where policy inherits and where billing and blast radius are bounded.
Design it for policy and isolation, not to mirror the org chart.

## Patterns
- **AWS Organizations**: OUs Security (log archive, security tooling accounts),
  Infrastructure (network, shared services), Workloads (Prod / NonProd sub-OUs),
  Sandbox, Policy Staging, Suspended. One account per workload per environment.
- **Azure**: tenant root group > intermediate root (your org) > Platform (Identity,
  Management, Connectivity) and Landing Zones (Corp, Online) > Sandbox > Decommissioned.
  Subscriptions per workload/environment in the right group.
- **GCP**: organisation > folders (e.g. bootstrap, common, production, non-production,
  development) > projects per workload/environment.

## Steps
1. List policy differences you need (prod vs non-prod, internet-facing vs internal,
   regulated vs not); each distinct set justifies a branch.
2. Keep it shallow (3-4 levels); deep trees make inheritance hard to reason about.
3. Use the account/subscription/project as the isolation and billing unit; use tags for
   finer attribution.
4. Protect the management/root: no workloads in the management account; break-glass only.
5. Document where each workload type lands, used by account vending.

## Gotchas
- Moving subscriptions/accounts later re-applies policy and can break things; design early.
- Org-chart hierarchies churn with every reorganisation.

## Verify
- [ ] Each branch has a documented policy reason.
- [ ] No workloads in management or root accounts.
