---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-status-and-debug-endpoints
name: prometheus-status-and-debug-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, debug-endpoints, runtime-info, status-api, tsdb-status-api, buildinfo, targets-api, promtool-debug]
level: practitioner
status: gated
description: "Use the Prometheus status/debug HTTP endpoints (runtimeinfo, buildinfo, config, flags, tsdb, walreplay, targets, rules, pprof) to triage a sick server from the CLI."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/#status", "https://prometheus.io/docs/prometheus/latest/management_api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Status and debug endpoints

```bash
P=http://prom:9090
curl -s $P/-/healthy; curl -s $P/-/ready                                  # 200 when up / when TSDB loaded
# every response is JSON {"status":"success","data":...}; pipe to jq or python -m json.tool to filter (jq itself was not run here)
curl -s $P/api/v1/status/buildinfo      # data: version, revision, branch, buildUser, buildDate, goVersion
curl -s $P/api/v1/status/runtimeinfo    # data: startTime, CWD, hostname, serverTime, reloadConfigSuccess, lastConfigTime, corruptionCount, goroutineCount, GOMAXPROCS, GOMEMLIMIT, GOGC, GODEBUG, storageRetention
curl -s $P/api/v1/status/flags          # effective command-line flags, every flag incl. defaults
curl -s $P/api/v1/status/config         # data.yaml: loaded config, secrets shown as <secret>
curl -s $P/api/v1/status/tsdb           # data.headStats (numSeries, numLabelPairs, chunkCount, minTime, maxTime), seriesCountByMetricName, labelValueCountByLabelName, memoryInBytesByLabelName, ...
curl -s $P/api/v1/status/walreplay      # data: {min, max, current} progress during startup replay
curl -s "$P/api/v1/targets?state=active"    # data.activeTargets[]: .health, .scrapeUrl, .lastError, .labels.job
curl -s "$P/api/v1/targets/metadata?match_target={job=%22api%22}"
curl -s "$P/api/v1/rules?type=alert"    # data.groups[].rules[]: .health, .lastError
curl -s $P/api/v1/alertmanagers         # activeAlertmanagers / droppedAlertmanagers
```

## Triage order
1. `ready` false -> `walreplay` progress; logs.
2. `runtimeinfo.reloadConfigSuccess=false` -> config error since last good load (old config still active).
3. `tsdb` headStats numSeries jump -> cardinality incident; `seriesCountByMetricName`, `labelValueCountByLabelName`.
4. Failing targets list from `targets`; failing rules from `rules`.
5. Memory/CPU -> `/debug/pprof/*` or `promtool debug all $P` (run: writes `debug.tar.gz` holding cpu.pb, heap.pb, block.pb, goroutine.pb, mutex.pb, threadcreate.pb, trace.pb and metrics.txt; it takes about 30 s because it collects a 30 s trace).

## Gotchas
- `/api/v1/status/tsdb` accepts `?limit=N`: default 10 items per statistic, maximum 10000 (docs; `limit=2` returned two, run).
- These endpoints are unauthenticated unless a web config file is set (see the basic-auth skill); the config YAML can reveal internal hostnames and `/debug/pprof/` is served too (run).

## Verify
- [ ] A one-liner script with the above gives a health summary in under 5 s (not timed; gated: unconfirmed, source is paywalled or blocked).
- [ ] Runbooks link to these commands for "Prometheus not ready" and "cardinality spike" alerts.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally: every endpoint in the block (buildinfo, runtimeinfo fields, flags, config with a `basic_auth` password shown as `<secret>`, tsdb with `limit=2`, walreplay `{min,max,current}`, targets, targets/metadata, rules, alertmanagers), `/debug/pprof/`, and `promtool debug all` (tarball listing read). Docs read: querying/api.md at tag v3.15.1 (tsdb limit). Not run: `jq`, a cardinality incident, `ready` false during a large WAL replay.
