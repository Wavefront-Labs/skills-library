---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-enrichment
name: cost-data-enrichment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-ingestion, cost-data-enrichment, cmdb, service-catalogue, account-metadata, business-mapping, cost-centre-mapping, tag-normalisation]
level: practitioner
status: docs-checked
description: "Join billing data with business metadata (account owners, CMDB, org structure, cost centres) so costs map to teams and products even without perfect tagging."
sources: ["https://www.finops.org/framework/capabilities/data-ingestion/", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enriching cost data with business metadata

Tags are only one source of ownership. The FinOps Data Ingestion capability expects internal business data to be brought
in to contextualise cost and usage and to support the Allocation strategy.

## Sources to join (as named in the framework)
1. Account, project and subscription hierarchy and naming standards, plus tags and labels, which Data Ingestion gathers and
   maps to internal allocation metadata.
2. CMDB or other service management metadata, including the service catalogue and registry.
3. Specialised tooling data such as Kubernetes usage, plus observability and utilisation data, which the Allocation page
   lists as sources for finer or shared-cost allocation.
4. Business data such as revenue, number of customers or transactions.
5. The finance hierarchy of cost centres and departments (an input to the chargeback process).

## Steps
1. Decide with the Allocation capability which organisational groupings and metadata keys are required (project names,
   application IDs, cost centre IDs), then map each source to them.
2. Consolidate existing tag and label standards and normalise names so one meaning has one key (the Allocation page lists
   this as an input).
3. Keep the mapping tied to the business and able to change as the business changes; at the Run level the framework
   expects the data to capture historical changes, so a reorganisation does not silently rewrite past allocation.
4. Build reports that surface any spend not covered by the allocation metadata.
5. Add completeness and quality checks to ingestion, and record and reconcile any data changes made outside source
   systems back to the source.

## Gotchas
- Allocation strategies change as the practice matures and several versions may be in force at once, so complete
  consistency is hard; aim for the level of allocation that supports good decisions.
- The aim is data that adds value at the current maturity, not the largest dataset possible.

## Verify
- [ ] The share of spend allocated is reported, with the unallocated remainder visible.
- [ ] Mapping tables keep history.

## Checked
Confirmed against the FinOps Data Ingestion and Allocation capability pages (read in full, apart from the long Allocation
KPI lists): data sources including CMDB and service management metadata, Kubernetes usage, business data and tags mapped
to allocation metadata, normalisation and mapping data model, historical changes captured at Run, unallocated spend
reports, completeness checks, reconcile changes back to source, aim of value at current maturity. Removed: named
products (Backstage, ServiceNow, OpenCost, Kubecost), cloud-specific tag names, valid_from and valid_to columns, the
precedence order, the allocation_method column, the HR directory source, the Git storage advice and the single-owner mapping warning.
Method: docs-checked 2026-11-09 against the FinOps Framework Data Ingestion and Allocation pages.
