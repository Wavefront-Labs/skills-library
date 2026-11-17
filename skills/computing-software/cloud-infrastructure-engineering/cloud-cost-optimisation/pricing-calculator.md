---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.pricing-calculator
name: pricing-calculator
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-estimation, pricing-calculator, aws-pricing-calculator, azure-pricing-calculator, google-cloud-pricing-calculator, architecture-cost-estimate, hidden-costs]
level: practitioner
status: draft
description: "Estimate a new architecture's monthly cost with provider calculators: driver assumptions, every billable dimension incl. egress, logs and backups, ranges, review."
sources: ["https://calculator.aws/", "https://azure.microsoft.com/pricing/calculator/", "https://cloud.google.com/products/calculator", "https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Estimating a new architecture

## Steps
1. **Write the drivers first**: requests/day, peak RPS, data stored and growth/month, data
   transferred out, users, batch hours. Every line in the estimate references a driver.
2. Walk the architecture diagram component by component and list **all billable dimensions**:
   - Compute: instance hours × count (peak and average), or requests + GB-seconds for serverless.
   - Storage: GB-month, IOPS/throughput provisioned, snapshots/backups, requests.
   - Network: egress to internet, inter-region, **cross-AZ** (both directions billed on several
     clouds), NAT gateway processing, load balancer units (LCU / capacity units), CDN.
   - Managed services: per-hour + per-request + storage (DBs, queues, API gateways).
   - Observability: log ingestion GB, metrics, traces, retention.
   - Security: WAF rules/requests, key operations, secrets per month.
   - Support plan (% of spend).
3. Enter in the calculator (AWS Pricing Calculator, Azure Pricing Calculator, Google Cloud Pricing
   Calculator); save and share the link; export to CSV.
4. Produce **low / expected / high** using driver ranges, and on-demand vs with commitments.
5. Add non-prod environments (often 30-60% of prod) and DR.
6. Record assumptions and date (prices change); attach to the design doc / ADR.

## Commonly forgotten
Egress and NAT, cross-AZ replication traffic, logs, backup storage, idle non-prod, data
migration one-offs, double-running during migration.

## Verify
- [ ] Estimate reviewed by someone who runs a similar workload.
- [ ] After 3 months in prod, compare actuals vs estimate per line and feed the learning back.
