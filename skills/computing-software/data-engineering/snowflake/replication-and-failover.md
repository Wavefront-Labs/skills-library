---
id: computing-software.data-engineering.snowflake.replication-and-failover
name: replication-and-failover
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-replication, failover-group, replication-group, business-continuity, client-redirect, connection-object, cross-region, disaster-recovery]
level: advanced
status: docs-checked
description: "Protect Snowflake against region outages: failover groups for databases, roles and warehouses, refresh schedules, client redirect connections, and failover drills."
sources:
  - https://docs.snowflake.com/en/user-guide/account-replication-intro
  - https://docs.snowflake.com/en/user-guide/account-replication-config
  - https://docs.snowflake.com/en/user-guide/client-redirect
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Replication and failover

**Goal:** a secondary account in another region/cloud holds a recent copy of data and account objects, and clients can be redirected to it during an outage.

## Concepts
- **Replication group**: read-only replicas of selected objects in target accounts (also used to share data across regions).
- **Failover group** (Business Critical Edition or higher): same, plus the target can be **promoted** to primary.
- Object types are set with `OBJECT_TYPES` (for example users, roles, warehouses, resource monitors, databases, integrations, network policies); see the replication config page for the full list.
- Accounts must be in the same organization; an organization administrator enables replication for each source and target account (`ENABLE_ACCOUNT_DATABASE_REPLICATION`).

## Configure
```sql
-- on primary (org: acme, accounts: prod_eu, dr_us)
create failover group prod_fg
  object_types = users, roles, warehouses, resource monitors, databases, integrations, network policies
  allowed_databases = analytics, raw
  allowed_integration_types = storage integrations, notification integrations
  allowed_accounts = acme.dr_us
  replication_schedule = '10 MINUTE';

-- on secondary
create failover group prod_fg as replica of acme.prod_eu.prod_fg;
alter failover group prod_fg refresh;          -- initial refresh (can take long for big DBs)
```
`replication_schedule` sets how often the secondary refreshes.

## Client redirect
```sql
create connection prod_conn;                                    -- on primary
alter connection prod_conn enable failover to accounts acme.dr_us;
create connection prod_conn as replica of acme.prod_eu.prod_conn;   -- on secondary
```
Clients connect to the connection URL `<organization_name>-<connection_name>.snowflakecomputing.com`; the account is chosen by whichever connection is primary.

## Failover
```sql
-- on secondary, during an outage or drill
alter failover group prod_fg primary;
alter connection prod_conn primary;
```
Check the replication pages for objects that are not replicated or need planning (for example integration replication requires Business Critical Edition or higher).

## Monitor
The `REPLICATION_GROUP_REFRESH_PROGRESS` table function (Information Schema); alert when the last successful refresh is much older than the schedule.

## Verify
- [ ] Drill: promote secondary, run a BI query through the connection URL, fail back.
- [ ] Measured RPO (refresh lag) and RTO recorded vs targets.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the replication intro, replication config, CREATE/ALTER FAILOVER GROUP, CREATE CONNECTION and client redirect pages: failover and replication groups, Business Critical requirement, same-organization accounts, ENABLE_ACCOUNT_DATABASE_REPLICATION, OBJECT_TYPES, ALLOWED_DATABASES, ALLOWED_INTEGRATION_TYPES, ALLOWED_ACCOUNTS, REPLICATION_SCHEDULE, AS REPLICA OF, promotion of a secondary failover group to primary, CREATE CONNECTION, ENABLE FAILOVER TO ACCOUNTS, ALTER CONNECTION ... PRIMARY, REPLICATION_GROUP_REFRESH_PROGRESS, integration replication needs Business Critical.

Removed: refresh-cost sentence and the task replication note (not on the pages read).

Method: documentation only; no commands were run.
