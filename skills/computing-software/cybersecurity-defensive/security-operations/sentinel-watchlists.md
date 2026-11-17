---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-watchlists
name: sentinel-watchlists
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-watchlists, kql, allowlist, vip-users, enrichment, getwatchlist, detection-tuning]
level: practitioner
status: docs-checked
description: "Use Microsoft Sentinel watchlists for allowlists, VIP and asset context in KQL rules: the _GetWatchlist and _GetWatchlistAlias functions, templates and documented limits."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/watchlists", "https://learn.microsoft.com/en-us/azure/sentinel/watchlists-queries", "https://learn.microsoft.com/en-us/azure/sentinel/watchlist-schemas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel watchlists

**Goal:** keep reference data (allowlisted IPs, VIP users, service accounts, critical
assets, terminated employees) outside the rule KQL so tuning is a data change.

## Create
Create a watchlist by uploading a CSV (local file or Azure Storage) or by downloading a
Sentinel template, adding your data and uploading it. When you create a watchlist you define
the **SearchKey**: the column you expect to join on or search often.
Built-in templates (preview): High Value Assets, VIP Users, Network Addresses, Terminated
Employees, Identity Correlation, Service Accounts; the schema page lists each template's fields.
Create from Azure Storage (preview) for files up to 500 MB: upload the file to your storage
account and create a SAS URL so Sentinel can read it.

## Limits (as documented)
- Name and alias: 3 to 64 characters; first and last character alphanumeric, spaces, hyphens and underscores allowed between.
- Maximum 10 million active watchlist items across all watchlists in a workspace; deleted items do not count.
- Local file upload up to 3.8 MB; Azure Storage upload up to 500 MB.
- Reference data only, not large data volumes. Cross-workspace management with Azure Lighthouse is not supported.
- Column and table names must follow KQL entity naming restrictions.
- The `Watchlist` table keeps data 28 days, but watchlists refresh every 12 days (updating `TimeGenerated`), so a list stays queryable until you delete it.

## Use in KQL
Built-in functions: `_GetWatchlistAlias` (aliases of all watchlists) and
`_GetWatchlist('<alias>')` (name-value pairs of one watchlist). Use SearchKey for joins.
Watchlist as a variable (from the docs):
```
let watchlist = (_GetWatchlist('ipwatchlist') | project IPAddress);
Heartbeat
| where ComputerIP in (watchlist)
```
Inline, using SearchKey (the docs say this gives the best performance):
```
Heartbeat
| where ComputerIP in (
    (_GetWatchlist('ipwatchlist')
    | project SearchKey)
)
```
Enrichment with `lookup`:
```
Heartbeat
| lookup kind=leftouter _GetWatchlist('mywatchlist')
  on $left.RemoteIPCountry == $right.SearchKey
```
The query timestamp is ignored for watchlist queries in the query UI and scheduled alerts.

## Maintain
- Treat allowlists as data with an owner: add team-chosen columns such as `Owner` and `Expires` and review expired entries on a schedule (a convention, not a Sentinel feature).
- Do not delete and recreate a watchlist while Sentinel shows 5XX errors or a blank Watchlists page; first check whether `_GetWatchlistAlias` still returns rows and check Azure Service Health.

## Gotchas
- Empty or partial `_GetWatchlist` results can come from a narrow query time range or restrictive filters; widen the scope and retry.
- Zero rows right after creation: confirm the workspace and alias, then check the Log Analytics daily cap.
- After March 31, 2027 Sentinel is available only in the Defender portal (per the queries page).

## Verify
`_GetWatchlistAlias` lists the alias, and `_GetWatchlist('<alias>') | take 10` returns rows.

## Checked
Date: 2026-11-07. Read in full: the Watchlists overview page (limitations table, creation methods, query functions, troubleshooting sections), "Build queries or detection rules with watchlists" (SearchKey, lookup and in examples, alias listing) and the built-in template schemas page (template names). Trimmed as unconfirmed: the template name "Network Mapping" (page says Network Addresses), `ipv4_lookup` CIDR matching, the Watchlist Items API PUT path, the "updates take a minute" delay, "latest version" and "indexed" wording, the invented VIP `Title` enrichment and the "up to around 500 MB" imprecision (now: 500 MB Storage, 3.8 MB local). Create/Manage watchlist pages were not read.
Method: documentation only; no commands were run.
