---
id: computing-software.cloud-infrastructure-engineering.google-cloud.region-cfe-percentage-and-low-carbon-region-selection
name: region-cfe-percentage-and-low-carbon-region-selection
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, carbon-free-energy, cfe, region-selection, low-co2]
level: practitioner
status: docs-checked
description: "Choose Google Cloud regions by carbon: hourly carbon-free energy percentage (CFE%) and grid intensity data, the low-CO2 indicator, and trading off latency, price and residency."
sources: ["https://cloud.google.com/sustainability/region-carbon", "https://github.com/GoogleCloudPlatform/region-carbon-info", "https://cloud.google.com/architecture/framework/sustainability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Region CFE% and low-carbon region selection

## Data
- **Google CFE%**: calculated for every hour, the percentage of energy consumed in that hour in the region
  that is carbon-free; the published figure is the yearly average of the hourly values. Higher is better.
  Google's goal is to match consumption with carbon-free energy every hour in every region by 2030.
- **Grid carbon intensity** (gCO2eq/kWh): average operational gross emissions per unit of energy from the
  local grid. Use it to compare regions with similar CFE%, as it shows emissions while your workload is not
  running on carbon-free energy.
- Published per region yearly on the "Carbon free energy for Google Cloud regions" page, which marks some
  regions **Low CO2**, and as yearly CSV files in `GoogleCloudPlatform/region-carbon-info`
  (CSV header: `Google Cloud Region,Location,Google CFE,Grid carbon intensity (gCO2eq / kWh)`).
  The Low CO2 threshold is defined on that page; read it there.

## Decision framework
1. Hard constraints first: data residency, latency to users, service availability (for example GPU types), price.
2. Among acceptable regions, prefer higher CFE%, then lower grid intensity as the tie-breaker.
3. For latency-insensitive batch or ML training, use the lowest-carbon region allowed.
4. Encode as policy where useful (an allowed-locations organization policy) and record carbon data in
   architecture decision records.

## Gotchas
- CFE% is a yearly average of hourly values; hourly variation matters for carbon-aware scheduling.
- Moving data across regions adds egress cost and its own emissions; process large data where it lives.
- Figures are republished each year; re-check rather than hard-coding.

## Verify
- [ ] Region choice record lists CFE% and intensity with the source year.

## Checked
2026-10-28. Confirmed on the region-carbon page and the region-carbon-info CSV: hourly CFE% definition and yearly
aggregation, 2030 goal, grid intensity definition and use, Low CO2 label, CSV header. Removed: the wrong lowercase
column names (`cloud_region`, `google_cfe`), the sort one-liner, the "leaf icon in region pickers" claim, the
regional hydro/nuclear/coal generalisation, and the Carbon Footprint report verification step.
Method: documentation only; no commands were run.
