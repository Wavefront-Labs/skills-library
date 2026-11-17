---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pushgateway-grouping-keys-and-admin-api
name: pushgateway-grouping-keys-and-admin-api
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, pushgateway, pushgateway-admin-api, pushgateway-grouping-keys, grouping-key, admin-api, wipe, persistence-file, push-failure-time-seconds, delete-group, base64-labels, pushgateway-metrics, pca]
level: practitioner
status: verified
description: "Operate a Pushgateway: design grouping keys so jobs don't overwrite each other, delete stale groups, use the admin API (wipe, list), persistence flags and self metrics."
sources: ["https://github.com/prometheus/pushgateway/blob/master/README.md", "https://github.com/prometheus/pushgateway/blob/master/README.md#api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pushgateway grouping keys and admin API

**Goal:** keep a Pushgateway tidy: every group belongs to a live job, pushes never clobber
each other, and you can inspect or wipe state without a restart.

## 1. Grouping keys
A group is identified by the labels in the URL path: `/metrics/job/<job>/<label>/<value>…`.
Everything pushed to the same path is one unit — `PUT` replaces the whole group.
- Always include `job`; it is mandatory and first.
- Put `instance` in the path **only** if runs on different hosts must be distinguished.
  Omitting it means the gateway stores `instance=""` (seen in its `/metrics`), and a `honor_labels: true` scrape then yields series with no `instance` label at all, which is what you want for
  service-level jobs.
- Two jobs that share a path overwrite each other. Parallel shards of a job need a shard
  label in the path: `/metrics/job/export/shard/3`.
- Label values containing `/` (paths, URLs): `/metrics/job/export/path@base64/L3Zhci9sb2c=` (stored `path="/var/log"`, run).
  An empty value is `@base64/=` (stored `path=""`, run).

## 2. Inspect
```bash
curl -s localhost:9091/api/v1/metrics   # then, per element of .data: .labels, .last_push_successful, .push_time_seconds.metrics[0].value (fields read with Python; jq is not needed)
```
This lists every group with its labels, `push_time_seconds`, `push_failure_time_seconds`
and the metrics it holds (run: each element has the keys `labels`, `last_push_successful`, `push_failure_time_seconds`, `push_time_seconds` plus one key per pushed metric name) — the quickest way to find a group nobody pushes to anymore.

## 3. Delete and wipe
```bash
curl -X DELETE localhost:9091/metrics/job/export/shard/3   # one group (HTTP 202)
curl -X PUT    localhost:9091/api/v1/admin/wipe             # everything (needs --web.enable-admin-api; HTTP 202 in the run, GET gives 405)
```
`DELETE` removes exactly the group matching the path; a parent path does not cascade
(run: `DELETE /metrics/job/b64` left the `path=...` and `region=eu` groups in place, and only `DELETE /metrics/job/b64/region/eu` removed that group). Build job teardown so
each shard deletes its own group when it finishes if its metrics are per-run.

## 4. Flags that matter
| Flag | Why |
|---|---|
| `--persistence.file=/data/pg.data` | survive restarts (default: in-memory only; run: groups survived a restart) |
| `--persistence.interval=5m` | minimum interval between writes of the file (default 5m) |
| `--web.enable-admin-api` | enables `/api/v1/admin/wipe` |
| `--push.disable-consistency-check` | `--help` says "Do not check consistency of pushed metrics. DANGEROUS."; don't, unless migrating |
| `--web.enable-lifecycle` | `/-/quit` (used in the run) and `/-/reload` endpoints |

A push that is inconsistent with existing metrics (here a metric `ma` pushed as a counter while gauges named `ma` existed in other groups) returns `400 pushed metrics are invalid or inconsistent with existing metrics: ... is not a COUNTER` and sets `push_failure_time_seconds` for the group (a new group `verbs3` appeared with only the failure time, run). In a second run an existing group `lastcheck2` (with `y_m 5`) kept `y_m` after a rejected push, and its `push_failure_time_seconds` (1.7926394231e9) was newer than its `push_time_seconds` (1.7926394230e9), which is what the alert `push_failure_time_seconds > push_time_seconds` detects. A malformed body (`bad`) also returned 400 (`text format parsing error`) but left `push_failure_time_seconds` at 0 and the stored data unchanged, so alert on the 400 counter too. The README adds that `--push.disable-consistency-check` only moves the check to scrape time, where one inconsistent push can then fail every scrape.

## 5. Self metrics
`pushgateway_http_requests_total{handler="push",code="400"}` rising → clients sending bad
exposition (run: the series appeared as `{code="400",handler="push",method="put"} 1` after the bad push). `pushgateway_build_info` and `process_start_time_seconds` are present on `/metrics`, and `/-/healthy` and `/-/ready` return 200 (run). Scrape the gateway with
`honor_labels: true` or its own pushed metrics become `exported_*` (run: pushed `job` became `exported_job` without it); the gateway's own metrics are unaffected.

## Gotchas
- Push to the exact path the gateway serves. Run with `--web.route-prefix=/pg`: a push to `/metrics/job/rp` returned 404, a push to `/pg/metrics/job/rp` returned 200 and was stored, and `/metrics` itself was 404 (so a mis-prefixed push fails loudly here rather than silently; behaviour behind a path-rewriting reverse proxy depends on the proxy). On Git Bash for Windows pass `/pg` with `MSYS_NO_PATHCONV=1`, otherwise the shell rewrites it into a Windows path and the gateway panics at startup.
- Grouping-key labels override labels inside the pushed body with the same name (run: body `job="inbody"` pushed to `/metrics/job/real` was stored as `job="real"`, the other body label kept).
- Clients that push on every event create one HTTP request per event; batch in the job.

## Verify
- [ ] `/api/v1/metrics` shows no group older than its job's interval.
- [ ] Deleting a group removes its series from Prometheus queries after the next scrape (run: after `PUT /api/v1/admin/wipe`, an instant query for a wiped series was empty within about 90 s).
- [ ] Restarting the gateway with persistence keeps all groups.

## Checked
Pushgateway 1.11.4 (windows-amd64) run locally with `--web.enable-admin-api --web.enable-lifecycle --persistence.file`, scraped by Prometheus 3.15.1: group keys and `@base64` values, DELETE (parent versus child path), `PUT /api/v1/admin/wipe` (and GET 405), `/api/v1/metrics` element keys, an inconsistent push (400 with message, `push_failure_time_seconds`, `pushgateway_http_requests_total{code="400"}`), body-label override, persistence and no-persistence restarts, `--help` text for the flags.
