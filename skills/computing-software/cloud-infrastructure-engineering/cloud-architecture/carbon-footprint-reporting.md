---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.carbon-footprint-reporting
name: carbon-footprint-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-sustainability, carbon-footprint-reporting, customer-carbon-footprint-tool, emissions-impact-dashboard, scope-3]
level: practitioner
status: draft
description: "Report cloud carbon footprint from provider tools: AWS, Azure and Google carbon data, scopes and methodologies, exports, allocation to teams and caveats."
sources: ["https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html", "https://learn.microsoft.com/industry/sustainability/api-overview", "https://cloud.google.com/carbon-footprint/docs/methodology", "https://www.cloudcarbonfootprint.org/docs/methodology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carbon footprint reporting from provider tools

## Sources
- **AWS Customer Carbon Footprint Tool** (Billing console; data export available via Data
  Exports): monthly estimates by service and region, market-based; data lag of weeks.
- **Microsoft Emissions Impact Dashboard** / Azure carbon optimization: scope 1, 2 and 3 by
  subscription and service; export via API/Power BI.
- **Google Cloud Carbon Footprint**: location- and market-based, by project, region and
  service; export to BigQuery.
- **Cloud Carbon Footprint** (open source) estimates from billing data using published
  coefficients when native data is insufficient.

## Steps
1. **Enable exports** to the cost data platform so carbon joins billing and tags.
2. **Understand methodology**: scope 2 location-based vs market-based; whether scope 3
   (embodied hardware, upstream) is included; allocation methods differ by provider, so
   multi-cloud totals are not perfectly comparable.
3. **Allocate** to teams via the same account/project mapping used for cost.
4. **Report** monthly: total emissions, emissions per unit of business output (per order,
   per 1,000 requests), trend, top contributors; feed corporate sustainability (CSRD/GHG
   Protocol scope 3 category 1 for purchased services).
5. **Set targets** on intensity metrics, not only absolute numbers.

## Gotchas
- Provider data lags (up to 3 months for some) and is restated; label periods as provisional.
- Market-based numbers near zero can hide efficiency work; also track usage-based proxies.

## Verify
- [ ] Carbon data in the same reporting platform as cost, allocated to owners.
- [ ] Methodology and scopes stated on every report.
