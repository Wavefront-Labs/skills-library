---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pricing-lookups-with-billing-catalog-api-and-calculator
name: pricing-lookups-with-billing-catalog-api-and-calculator
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, billing-catalog-sku-lookup, pricing-calculator-estimates, cloud-billing-catalog-api, pricing-api, cost-estimation]
level: practitioner
status: docs-checked
description: "Look up Google Cloud SKU prices with the Cloud Billing Catalog API and the preview Pricing API, including contract prices for a billing account, and the Pricing Calculator."
sources: ["https://cloud.google.com/billing/docs/how-to/get-pricing-information-api", "https://cloud.google.com/billing/v1/how-tos/catalog-api", "https://cloud.google.com/products/calculator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pricing lookups with the Catalog API and the Pricing Calculator

## 1. Catalog API v1 (public prices, API key)
Enable the Cloud Billing API (needs `serviceusage.services.enable`, e.g. Service Usage Admin) and
create an API key; every Catalog call needs the key.
```text
GET https://cloudbilling.googleapis.com/v1/services?key=API_KEY
GET https://cloudbilling.googleapis.com/v1/services/SERVICE_ID/skus?key=API_KEY
```
Services return `name`, `serviceId`, `displayName`. SKUs return `name`
(`services/{SERVICE_ID}/skus/{SKU_ID}`), `skuId`, `description`, `category` (`resourceFamily`,
`resourceGroup`, `usageType` such as OnDemand, Preemptible, Commit1Mo, Commit1Yr),
`serviceRegions`, `pricingInfo` and `geoTaxonomy` (type GLOBAL, REGIONAL or MULTI_REGIONAL; the
regions list is empty for global SKUs).

- Pages hold up to 5000 items; follow `nextPageToken` with `pageToken=`, shrink with `pageSize=`;
  no token means the end.
- Price: `pricingInfo[].pricingExpression.tieredRates[]` has `startUsageAmount` (the rate applies only
  after that much usage) and `unitPrice` (`currencyCode`, `units`, `nanos`). Cost is units + nanos,
  e.g. $1.75 is units=1, nanos=750000000, per `usageUnit` (for example GiBy). `baseUnit` is the unit
  used in usage exports and `baseUnitConversionFactor` converts between them.
- `displayQuantity` is for display only; it does not change the price formula.
- `aggregationInfo` gives the level (ACCOUNT, PROJECT) and interval (DAILY, MONTHLY) at which usage is
  aggregated to compute cost.
- The same data is in the pricing table report and the Cloud Billing pricing export to BigQuery.

## 2. Pricing API (preview, v1beta and v2beta)
Pre-GA "as is" and may have limited support. Public calls (no IAM permission, API key needed):
```text
GET https://cloudbilling.googleapis.com/v2beta/services?key=API_KEY&pageSize=N&pageToken=T
GET https://cloudbilling.googleapis.com/v2beta/skus?key=API_KEY&filter=service="services/6F81-5844-456A"
GET https://cloudbilling.googleapis.com/v1beta/skus/SKU_ID/prices?key=API_KEY      # SKU_ID "-" = all
GET https://cloudbilling.googleapis.com/v1beta/skus/SKU_ID/price?key=API_KEY&currencyCode=CUR
```
Default page size is 50 (SKUs maximum 5000). Without `currencyCode` the price uses your Cloud Billing
account's currency.

## 3. Prices specific to your billing account (contract pricing)
Endpoints sit under `v1beta/billingAccounts/BILLING_ACCOUNT_ID/` (for example `skuGroups`,
`skuGroups/SKU_GROUP_ID/skus`, `skus/SKU_ID/prices`). Permissions needed on the billing account:

| Resource | Permissions |
|---|---|
| `billingAccounts.services` | `billing.billingAccountServices.get`, `.list` |
| `billingAccounts.skus` | `billing.billingAccountSkus.get`, `.list` |
| `billingAccounts.skugroups` | `billing.billingAccountSkuGroups.get`, `.list` |
| `billingAccounts.skugroups.skus` | `billing.billingAccountSkuGroupSkus.get`, `.list` |
| `billingAccounts.skus.price` | `billing.billingAccountPrice.get` |

Billing Account Administrator and Billing Account Viewer have them. A service account caller needs
them too. SKU groups matter if your Google Cloud contract refers to them.

## 4. Pricing Calculator
Builds estimates from assumptions you give; Google says they may not match the final bill. The page
has a currency selector, monthly cost and an annual cost (a simple x12), and buttons for
"Download .csv" and "New from duplicate". "Sign in to view billing account pricing" shows prices for
your account.

## Gotchas
- Public Catalog and Pricing calls show public prices; custom contract prices need section 3.
- Match SKUs on `skuId` rather than `description` text.

## Verify
- [ ] The tiered rate you picked starts at the `startUsageAmount` that fits your volume.
- [ ] A contract-price call succeeds only with the billingAccount permissions above.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands or API calls were run.
Read in full: the Catalog API how-to (v1 endpoints, response fields, pagination, nanos). The Pricing API page was read lines 1-120 and then searched for endpoints, price and permissions (the middle response examples and lines after about line 545 were not read). The Pricing Calculator page is a JavaScript shell; only its few lines of visible text (currency list, monthly and annual cost, CSV download, duplicate) were available.
Corrections: removed the `curl | jq` example with a GBP `currencyCode` on the v1 Catalog (the page does not show that parameter for v1), the claim that the Pricing API needs only Billing Account Viewer and `billing.billingAccountPrice.get` for all calls, the "730 hours", sustained use and CUD selection claims, the list of commonly missed costs, "share the estimate URL", the "~10%" reconciliation and the claim that discounts appear in billing export.
