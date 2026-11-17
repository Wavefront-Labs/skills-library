---
id: computing-software.data-engineering.snowflake.private-listings
name: private-listings
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, private-listing, listings, data-sharing, cross-region-sharing]
level: advanced
status: docs-checked
description: "Share Snowflake data products with specific accounts via private listings: creating them, cross-region auto-fulfillment, organization listings, and consumer access."
sources:
  - https://docs.snowflake.com/en/collaboration/provider-listings-creating-publishing
  - https://docs.snowflake.com/en/collaboration/provider-listings-auto-fulfillment
  - https://docs.snowflake.com/en/user-guide/collaboration/listings/organizational/org-listing-about
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private listings

**Goal:** share curated data (or a Native App) with chosen consumers across regions and clouds, with metadata, without per-region manual replication.

## Listing vs direct share
- **Direct share**: a secure share; it can be converted to a free (or paid off-platform) private listing, and existing consumers keep access.
- **Listing**: wraps a share or app; supports **cross-region auto-fulfillment**; private listings are auto-fulfilled after the specified consumers get them; Marketplace listings are public.

## Create
Snowsight: Marketplace > Provider Studio > Create Listing > Specified Consumers. The share SQL below is the usual starting point:
```sql
CREATE SHARE sales_share;
GRANT USAGE ON DATABASE sales TO SHARE sales_share;
GRANT USAGE ON SCHEMA sales.public TO SHARE sales_share;
GRANT SELECT ON VIEW sales.public.orders_v TO SHARE sales_share;

CREATE EXTERNAL LISTING sales_listing SHARE sales_share AS
$$
<YAML manifest: keys are in the Listing manifest reference>
$$ PUBLISH = FALSE REVIEW = FALSE;   -- saves a draft, no review requested, not published
```
Auto-fulfillment can be configured with `SUB_DATABASE` or `SUB_DATABASE_WITH_REFERENCE_USAGE` (see the auto-fulfillment page).

## Organization listings (internal)
See the organizational listings page for sharing across your own organization.

## Gotchas
- Share only secure views/secure UDFs over base tables you control; never share raw tables with PII unless intended.
- Refresh schedule controls staleness and cost in remote regions.
- Revoking an account from targets removes access immediately; communicate changes.

## Verify
In a consumer test account in another region, the listing appears, Get creates the database, and data refreshes per schedule.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the CREATE LISTING, listing creation/publishing, auto-fulfillment and organizational listing pages: Snowsight path Marketplace > Provider Studio > Create Listing > Specified Consumers, CREATE EXTERNAL LISTING ... SHARE ... AS manifest with PUBLISH and REVIEW options (FALSE/FALSE saves a draft), SUB_DATABASE and SUB_DATABASE_WITH_REFERENCE_USAGE, direct share conversion.

Removed: the manifest keys and sample values (not on the pages read; see the Listing manifest reference), the Data Products menu path, same-region claim.

Method: documentation only; no commands were run.
