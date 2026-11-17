---
id: computing-software.cloud-infrastructure-engineering.azure.resource-graph-paging-skip-tokens-and-throttling
name: resource-graph-paging-skip-tokens-and-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-graph, arg-paging, skip-token, arg-throttling, query-limits, automation]
level: practitioner
status: docs-checked
description: "Get complete results from Azure Resource Graph: --first/--skip-token paging, quota headers and throttling, query limits and batching across many subscriptions."
sources: ["https://learn.microsoft.com/azure/governance/resource-graph/concepts/work-with-data", "https://learn.microsoft.com/azure/governance/resource-graph/concepts/guidance-for-throttled-requests", "https://learn.microsoft.com/azure/governance/resource-graph/concepts/query-language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource Graph paging and throttling

**Goal:** scripts that return every row (not the first 100) and don't get throttled at scale.

## Paging
- A query returns at most **1,000** records per response; page with a skip token for the rest.
```bash
token=""
while :; do
  if [ -z "$token" ]; then
    out=$(az graph query -q "resources | project id, type | order by id asc" --first 1000 -o json)
  else
    out=$(az graph query -q "resources | project id, type | order by id asc" --first 1000 --skip-token "$token" -o json)
  fi
  echo "$out" | jq -r '.data[].id'
  token=$(echo "$out" | jq -r '.skip_token // empty')
  [ -z "$token" ] && break
done
```
PowerShell: `Search-AzGraph -Query $q -First 1000 -SkipToken $token`. REST: `options.$top`, `options.$skipToken`.
Include `id` in the projection and a stable `order by` - paging needs it.

## Throttling
- Each user gets a quota per time window (the docs example: at most 15 queries per 5-second window; the value varies and can change). Responses carry headers
  `x-ms-user-quota-remaining` (query count left) and `x-ms-user-quota-resets-after` (hh:mm:ss until reset).
- Respect `resets-after`; stagger parallel jobs; one service principal per automation so they don't share a quota.

## Make queries cheaper
- Filter early (`where type == ...`) and `project` only needed columns.
- `summarize` server-side instead of pulling all rows.
- Query limits: at most three `join`/`union` operations combined and three `mv-expand` per query; `mv-expand` `RowLimit` max 2,000 (default 128). Split complex reports.

## Many subscriptions
- Scope with `--management-groups` (whole hierarchy) rather than passing thousands of subscription IDs.
- Results include only subscriptions where the caller has read access - missing data is often RBAC, not paging.

## Gotchas
- A single query response never exceeds 1,000 records; `limit` in KQL doesn't remove the need for paging.

## Verify
- [ ] Script row count equals `resources | count` for the same scope.

## Checked

Date: 2026-10-28.

Confirmed against Learn (Resource Graph work-with-data, guidance-for-throttled-requests, query-language): 1,000 records per response, skip-token paging, the quota headers and the 15-queries-per-5-seconds example, join/union/mv-expand limits and mv-expand RowLimit. CLI flags verified with check_commands.py.
Removed: CLI default of 100 rows, HTTP 429 wording, the 1,000-subscription batching claim, the eventual-consistency claim and the `--first` rejection claim (not on the fetched pages).

Method: documentation only; no commands were run.
