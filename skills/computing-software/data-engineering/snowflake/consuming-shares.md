---
id: computing-software.data-engineering.snowflake.consuming-shares
name: consuming-shares
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, secure-data-sharing, imported-privileges, inbound-shares, create-database-from-share, listings, consumer-account]
level: practitioner
status: docs-checked
description: "Consume a Snowflake share or listing as the consumer: create a database from the share, grant IMPORTED PRIVILEGES or imported database roles, and handle limits and changes."
sources:
  - https://docs.snowflake.com/en/user-guide/data-share-consumers
  - https://docs.snowflake.com/en/sql-reference/sql/create-database
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Consuming shares

**Goal:** make a provider's shared data available to the right roles in your account, and build on it safely.

## Find and mount
```sql
show shares;
desc share PROVIDER_ORG.PROVIDER_ACCT.SALES_SHARE;
use role ACCOUNTADMIN;                          -- or a role with the privileges to create the database
create database vendor_sales from share PROVIDER_ORG.PROVIDER_ACCT.SALES_SHARE;
```
Listings (Marketplace or private): "Get" in Snowsight, or `create database ... from listing '<listing_global_name>'`;

## Grant access
Whole share:
```sql
grant imported privileges on database vendor_sales to role ANALYST;
```
`IMPORTED PRIVILEGES` is all-or-nothing on objects the provider shared to the share itself.
If the provider shared **database roles**, grant those selectively:
```sql
show database roles in database vendor_sales;
grant database role vendor_sales.basic_view to role ANALYST;
grant database role vendor_sales.full_view to role DATA_SCIENCE;
```

## What you can and cannot do
- Read-only: no DML, no clone of the shared database, no Time Travel on shared objects.
- You can create views in **your own** database on top of shared objects, and secure views to re-expose subsets internally.
- You can reshare an imported database only when resharing is allowed: run `SHOW DATABASES` and check the `resharing_settings` column.
- Queries run on **your** warehouse.

## Build on it robustly
```sql
create or replace view analytics.vendor.daily_sales as
select * from vendor_sales.public.daily_sales;   -- isolate dbt models from share names
```
Declare shared objects as dbt sources pointing to the imported database.

## Change handling
- Providers can add or remove objects or revoke the share; views over removed objects will fail. Monitor with a freshness/existence check.
- Schema changes upstream break `select *` views; select explicit columns.
- `show shares` and `desc share` show what is currently included.

## Gotchas

## Verify
- [ ] `ANALYST` can select from the imported database; roles without grants cannot.
- [ ] A data test or freshness check alerts if the share disappears or stops updating.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: CREATE DATABASE ... FROM SHARE and FROM LISTING syntax, GRANT IMPORTED PRIVILEGES, granting imported database roles to account roles, no clone or Time Travel on imported databases, resharing only when allowed via resharing_settings (data-share-consumers and create-database pages).

Removed or corrected: the kind = INBOUND comment, IMPORT SHARE privilege wording, who pays storage, one-database-per-share, cross-region and access-history bullets (not on the pages read); corrected the re-share claim.

Method: documentation only; no commands were run.
