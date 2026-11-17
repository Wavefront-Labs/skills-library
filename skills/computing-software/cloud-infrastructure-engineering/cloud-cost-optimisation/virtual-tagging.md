---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.virtual-tagging
name: virtual-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-allocation, virtual-tagging, retroactive-tagging, cost-category-rules, tag-normalisation, allocation-rules]
level: practitioner
status: docs-checked
description: "Improve allocation without touching resources: derive ownership from accounts and metadata, correct tags after billing data arrives, and shift ownership left."
sources: ["https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retroactive tag correction and derived allocation

## Why
The FinOps Allocation capability says tagging strategies must allow for compliance and
consistency challenges, for differences in how resources can be tagged in different
environments, and for costs that cannot be tagged. It lists tags applied after launch, and
automation, infrastructure as code and tools that manage tags, as ways to make tagging more
effective.

## Techniques the page supports
1. **Account and grouping ownership**: allocate by a known list of owners of accounts, projects,
   subscriptions, resource groups or other logical groupings.
2. **Naming conventions and tags or labels** on resources for finer granularity.
3. **Other sources**: the CMDB, observability or utilisation data for more granular allocation
   or shared cost elements.
4. **Mechanisms that correct or augment the provider's tagging after billing data is received**,
   described at Run maturity as a way to reach high allocation compliance.
5. **Provisioning automation** so resource and account tags and metadata are consistent.

## Steps
1. Measure unallocated and untagged cost, and investigate owners of unknown accounts.
2. Document the tagging strategy: naming standards, required tags, hierarchy groupings.
3. Add correction rules over the billing data where tags are missing or inconsistent.
4. Move enforcement upstream: the page describes requiring ownership and metadata fields in
   provisioning templates (Walk) and blocking creation when they are missing (Run), with an
   escalation path for changes beyond agreed thresholds.
5. Review allocation KPIs and share the rules with teams.

## Verify
- [ ] Allocation coverage is measured and reviewed against a target you set.
- [ ] Correction rules are documented and visible to the teams they affect.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Allocation capability page (read through the functional activities). The AWS cost categories and Azure tag inheritance pages were not readable and were dropped. Removed unconfirmed: the AWS cost category retroactive backfill claim, Azure tag inheritance and GCP project label claims, the rule priority order, the 95 percent target and the dbt/git approach.
