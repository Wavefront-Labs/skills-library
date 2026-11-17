---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.pricing-models
name: pricing-models
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-billing, pricing-models, on-demand, tiered-pricing, free-tier, pricing-units, pay-per-request, provisioned-capacity, sustained-use-discounts, price-list-api]
level: practitioner
status: draft
description: "Read cloud pricing correctly: on-demand vs provisioned vs per-request units, tiered and regional prices, automatic discounts, free tiers, and pulling prices programmatically."
sources: ["https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html", "https://learn.microsoft.com/rest/api/cost-management/retail-prices/azure-retail-prices", "https://cloud.google.com/billing/docs/reference/rest", "https://focus.finops.org/focus-specification/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud pricing models and units

## Model families
| Model | Examples | Watch for |
|---|---|---|
| On-demand per time unit | VMs per second/hour, managed DB instance-hours | minimum billing increments (per-second with 60 s minimum on many Linux VMs) |
| Provisioned capacity | DynamoDB provisioned RCU/WCU, Cosmos RU/s, provisioned IOPS | paying for peak whether used or not |
| Per request / per operation | Lambda requests + GB-s, S3 PUT/GET, API Gateway calls | small unit prices × huge counts |
| Per GB stored / transferred | object storage GB-month, egress per GB | tiers that drop with volume; cross-AZ and inter-region charges |
| Tiered / volume | storage and egress tiers | which account aggregates the tier (org-level vs account) |
| Automatic discounts | GCP sustained use discounts on some VM families | they disappear when you buy CUDs on the same usage |
| Free tiers | per account/month limits | multiply when you have many accounts? (mostly per payer/org) |

## Read a price correctly
1. Identify the **pricing unit** (FOCUS `PricingUnit`, e.g. `GB-Mo`, `Hrs`, `Requests`) and the
   **consumed quantity** — they differ (a 1 TB disk is 1024 GB-Mo prorated hourly).
2. Region matters: same SKU can vary 10-50% between regions.
3. Include all dimensions: a managed DB = instance + storage + IOPS + backup + I/O requests + egress.

## Programmatic prices
- AWS Price List Query API (`aws pricing get-products --service-code AmazonEC2 --filters ...`, us-east-1 / ap-south-1 endpoints) and bulk files.
- Azure Retail Prices API (`https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Virtual Machines'`), unauthenticated.
- GCP Cloud Billing Catalog API (`services/<id>/skus`).
- Your negotiated prices: from billing data (effective price), not list APIs.

## Verify
- [ ] Every line in an estimate names unit, quantity, unit price and region.
