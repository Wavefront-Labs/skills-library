---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.composite-sla
name: composite-sla
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-ecosystem, composite-sla, sla, service-credits, availability-math]
level: practitioner
status: docs-checked
description: "Derive a composite SLO from dependency SLAs by multiplying serial components, adjust for SLA scope, and treat service credits as enforcement, not a guarantee."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite SLO from dependency SLAs

Based on the Azure Well-Architected Framework reliability metrics guidance.

## Calculation
- A composite SLO is a product of the contributing factors. The page's example: 99.95% x 99.99999% = ~99.95%.
  Worked the same way, serial 99.95% x 99.99% x 99.9% = 99.84% (arithmetic, not from the page).
- Redundancy (a secondary region for failover) can improve the SLO when properly designed. Under a bulkhead pattern
  (customers restricted to regional stamps), measure each stamp's health separately; if you can fail over between
  stamps, the overall SLO is higher. The page notes Microsoft guarantees higher Cosmos DB SLAs for multiregion than
  single-region deployments.
- Noncompliance time per month (page table): 99% = 7.20 hours, 99.90% = 43.20 minutes, 99.95% = 21.60 minutes,
  99.99% = 4.32 minutes, 99.999% = 25.90 seconds. Per year: 3.65 days, 8.76 hours, 4.38 hours, 52.56 minutes,
  5.26 minutes.

## Steps
1. Choose the scope for the SLO (application, workload, or a specific flow) and list the components on that flow.
2. Include external services and shared platform components when they directly affect the customer experience or
   critical flows. Components whose brief unavailability does not affect the experience can be omitted, with an
   explicit, consensus-based justification.
3. Use the provider's published SLA as input, not as the answer. Adjust each value for what the SLA covers and for
   your own risks. In the page's example the team keeps some SLA values as is and lowers SQL Managed Instance to
   99.80% to allow for schema changes and backups, then multiplies the adjusted values (99.72% composite).
4. Components with no published SLA (virtual networks, NSGs in the example) still need an assumed value; the
   example assumes 99.99% each.

## Gotchas
- SLAs do not guarantee an offering as a whole. App Service is available when it returns 200 OK in a given use
  case; features such as Easy Auth or slot switching fall outside financially backed coverage, so deriving the SLO
  solely from the App Service SLA is problematic.
- The Front Door 99.99% SLA applies only under the criteria in the agreement (a storage back end, a GET of a file
  of at least 50 KB, agents in at least five geographically diverse locations); caching, routing rules and WAF fall
  outside it.
- A service credit procedure acts as an enforcement policy; it does not make the workload available.
- Workloads not thoroughly tested against recovery metrics should not have guaranteed SLAs.

## Verify
- [ ] Composite figure documented beside the SLO with the assumptions and adjustments behind each component.
- [ ] Each SLA's coverage conditions were read, not just its percentage.

## Checked
2026-11-09. Confirmed against the Azure Well-Architected reliability metrics page (downloaded HTML; SLO, composite
SLO, SLA impact, multiregion and example sections read). Removed unconfirmed claims and sources: the AWS SLA and
Google SRE availability-table sources (not read), the credit claim deadline and exclusions, the single-instance SKU
remark, the shared control-plane independence caveat, and the earlier 43.8 minute figure (page gives 43.20).
Method: docs-checked 2026-11-09 against learn.microsoft.com/azure/well-architected/reliability/metrics downloaded HTML; documentation only, no commands run.
