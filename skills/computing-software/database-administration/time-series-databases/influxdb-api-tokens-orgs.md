---
id: computing-software.database-administration.time-series-databases.influxdb-api-tokens-orgs
name: influxdb-api-tokens-orgs
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-auth, influxdb-api-tokens-orgs, influxdb, flux]
level: practitioner
status: docs-checked
description: "Issue least-privilege API tokens scoped to organisations and buckets."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/create-token/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/auth/create/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API tokens and organisations

**Goal:** Issue least-privilege API tokens scoped to organisations and buckets.

## Steps
- An operator token (`influx auth create --operator`, OSS only) grants all permissions in all organizations; creating one after setup needs an existing operator token. Store it safely and keep it for administration, not day-to-day writes.
- Scoped token: `influx auth create -o myorg --read-bucket <id> --write-bucket <id> -d "grafana read"`.
- List and revoke: `influx auth list`, `influx auth delete -i <id>`; inactivate with `influx auth inactive -i <id>`.
- Use one token per writer (Telegraf host group, app) so a leak is revocable alone.
- Pass tokens via `INFLUX_TOKEN` environment variable or a secrets manager, never in config repos.

**Gotcha:** From InfluxDB OSS 2.9.0, tokens are stored hashed by default and the original strings cannot be recovered afterwards, so capture plaintext tokens you still need before upgrading and create a new token if one is lost.

## Verify
- A read-only token is rejected on a test write.
- `influx auth list` shows no unused all-access tokens.

## Checked

2026-11-03. Confirmed in the InfluxDB v2 pages for tokens, create-token and `influx auth create`, `auth delete`, `auth inactive`: the flags `--read-bucket`, `--write-bucket`, `-d/--description`, `-o/--org`, `-i/--id`, `--operator` (OSS only), the `INFLUX_TOKEN` variable, `influx auth list`, and the 2.9.0 token-hashing note. Removed: the claim that orgs separate users, buckets, tasks and dashboards, and the specific HTTP status codes (not stated on these pages).
Method: documentation only; no commands were run.

