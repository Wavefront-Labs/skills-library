---
id: computing-software.web-development.appwrite.appwrite-network-regions-endpoints
name: appwrite-network-regions-endpoints
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, network, regions, endpoints, cdn, edges]
level: intro
status: docs-checked
description: "Pick an Appwrite Cloud region and endpoint and understand how edges and the CDN serve traffic."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/regions/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/endpoints/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/edges/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/network/cdn/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect to the right Cloud endpoint.

Regions available: Frankfurt (FRA), New York (NYC), Sydney (SYD), San Francisco (SFO), Singapore (SGP) and Toronto (TOR). A project lives in one region, and its endpoint looks like `https://fra.cloud.appwrite.io/v1`, where the prefix is the region code.

Endpoint styles: `appwrite.network` is geo-balanced across locations, while `<region>.cloud.appwrite.io` pins you to one region.

Edges: Appwrite has 6 edge locations (FRA, NYC, SYD, SFO, SGP, TOR) that handle routing, caching and lightweight compute close to users. The CDN spans over 120 points of presence for static and cacheable content.

Caching works at the region, edge and CDN layers.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/network/regions, products/network/endpoints, products/network/edges, products/network/cdn. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed "cached privately", the mixing-regions gotcha, the CLI/predictable-latency advice and Verify; edge description corrected to routing, caching and lightweight compute in 6 locations.

Method: documentation only; no commands were run.
