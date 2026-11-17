---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.community-cloud
name: community-cloud
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, community-cloud, consortium, shared-regulation, government-cloud]
level: practitioner
status: draft
description: "Evaluate and govern a community cloud for organisations sharing regulation or mission: eligibility, governance charter, cost sharing, isolation and exit."
sources: ["https://csrc.nist.gov/pubs/sp/800/145/final", "https://aws.amazon.com/govcloud-us/", "https://learn.microsoft.com/azure/azure-government/documentation-government-welcome"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Community cloud for consortiums and shared-regulation groups

## When
Several organisations share a compliance regime or mission (government agencies, health trusts,
research consortia, financial market utilities) and want infrastructure scoped to that community.
NIST defines it as provisioned for exclusive use by a specific community; it may be owned by
members, a third party or both.

## Steps
1. **Check if a provider community offering already fits**: government regions (AWS GovCloud,
   Azure Government, sovereign partner clouds) are community clouds operated by a provider;
   usually cheaper than building one.
2. **If building or sharing**: write a governance charter covering membership criteria,
   decision rights, change approval, security baseline every member must meet, incident
   notification duties and audit rights.
3. **Cost-sharing model**: fixed share, usage-metered, or hybrid; define who funds capacity
   growth and what happens when a member leaves.
4. **Tenant isolation**: separate accounts/subscriptions/projects per member, no shared data
   planes unless the use case is data sharing, then a governed exchange with data agreements.
5. **Shared services**: identity federation across members, common logging and SOC, shared
   compliance evidence (one assessment reused by all members).
6. **Exit plan**: data return format, timelines, and how shared assets are split.

## Gotchas
- Consortium decision-making is slow; pre-agree a fast path for security patches.
- The weakest member's controls become everyone's risk; enforce the baseline technically.

## Verify
- [ ] Charter signed with membership, decision and exit terms.
- [ ] Per-member isolation and shared baseline enforced by policy.
