---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.tagging-strategy
name: tagging-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-allocation, tagging-strategy, tagging, labels, tag-dictionary, mandatory-tags, untaggable-resources]
level: practitioner
status: docs-checked
description: "Design a cost allocation tagging strategy: allocation groupings, naming standards, required metadata, enforcement at provisioning and handling untaggable spend."
sources: ["https://www.finops.org/framework/capabilities/allocation/", "https://www.finops.org/framework/capabilities/reporting-analytics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagging strategy for cost allocation

## Design
1. **Start from the allocation strategy**: define the organisational groupings you allocate all cost to (cost centre,
   business unit, application, environment) and the terminology for each. Finance, engineering and operations may each
   need a different slice of the same data.
2. **Define the tagging or metadata strategy**: naming standards for resources, accounts, projects and subscriptions;
   the tags or labels used to identify a grouping; how accounts are segregated and grouped; and how it is all
   aggregated. Write a tag dictionary with key, purpose, allowed values and owner.
3. **Account for constraints** the Framework names: compliance and consistency are hard, resources are taggable
   differently in different environments, and some costs cannot be tagged at all.
4. **Prefer account, project or subscription ownership lists** where whole accounts belong to one owner; tags
   then only need to cover shared accounts. The Framework lists this as the Crawl-level approach and says allocation
   granularity improves with resource-level naming and tags.
5. **Automate**: the Framework says tagging is more effective using automation, infrastructure as code, or tools that
   manage tags after launch. At Walk, required ownership and metadata fields are in the provisioning template with
   periodic compliance checks; at Run they are enforced as a precondition and requests missing them are blocked, with an
   escalation path.
6. **Coordinate with other owners**: the tagging strategy may be owned by a Centre of Excellence, Data Platform or
   DevOps team and can be combined with operations, automation and security needs.

## Untaggable and shared spend
Use a shared cost strategy: choose per shared item whether it is allocated to cost-centre budgets or funded centrally
(the Framework calls the latter "informed ignore"), and the split method (fixed, proportional, or proxy metrics).

## Verify
- [ ] Tag dictionary and naming standards are published, and provisioning templates set required metadata.
- [ ] Tagging compliance is measured; the Framework cites overall tagging compliance above 90 percent as a measure of success.

## Checked
Confirmed on the FinOps Framework Allocation page (allocation, tagging and shared cost strategies, tagging
constraints, automation and IaC, COE ownership, Crawl/Walk/Run enforcement, shared cost methods, informed ignore) and
the Reporting and Analytics page (tagging compliance above 90 percent). Removed: the 4-6 mandatory tag count and
example keys, GCP label length and character limits, Azure and AWS case-sensitivity claims, Terraform default_tags and
Azure Policy inheritance, AWS cost allocation tag activation and 12-month backfill, the GCP tags versus labels
distinction, and the AWS, Microsoft and Google source pages (unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Allocation and Reporting and Analytics capability pages
