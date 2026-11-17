---
id: computing-software.data-engineering.metabase.query-result-caching
name: query-result-caching
category: computing-software
field: data-engineering
product: metabase
tags: [caching, cache-policy, adaptive-caching, duration, schedule, cache-refresh]
level: practitioner
status: docs-checked
description: "Configure Metabase query result caching: Adaptive, Duration, Schedule and no-cache policies, precedence by level, auto-refresh limits, clearing caches and storage location."
sources:
  - https://www.metabase.com/docs/latest/configuring-metabase/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies:
- **Duration**: clears after a set number of seconds, minutes, hours or days (Pro/Enterprise).
- **Schedule**: clears hourly, daily, weekly or monthly; results are stored only when someone runs the query (Pro/Enterprise).
- **Adaptive**: lifetime is average query runtime times a multiplier, with a minimum query duration. For example 10 s x 100 = 1,000 s.
- **Don't cache results**: every view queries the database.

Precedence, highest first: question, dashboard, database, site default.

Where: Admin, Performance, Database caching sets the default and per-database policy ("Use default" inherits). Dashboards and questions use three dots, Edit settings, Caching, and need curate access on the collection. Per-database, dashboard and question overrides are Pro/Enterprise.

Refresh automatically (Duration and Schedule only): without it, the first viewer after expiry waits. It is unavailable with row and column security, impersonation or database routing. Refreshes use default parameter values plus up to ten of the most frequent parameter combinations from the last period. Find them in the query log by filtering Query source `cache-refresh`.

Clearing: Info, Caching policy, Clear cache on a question or dashboard; or Admin, Performance, pick the database, Clear cache.

Storage: self-hosted keeps the cache in the application database; Cloud uses Metabase servers in the United States.

Not documented on the page: caching env vars, default policy, size limits.

## Checked
2026-11-03. Confirmed against the Metabase docs page Configuring Metabase, Caching query results: the four policies and their plan limits, adaptive multiplier example, precedence order, Admin Performance path, refresh-automatically limits and the ten-parameter-combination rule, cache-refresh query source, clearing steps, caching location. Nothing removed.
Method: documentation only; no commands were run.
