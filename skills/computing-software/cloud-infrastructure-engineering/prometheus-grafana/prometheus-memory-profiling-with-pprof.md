---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-memory-profiling-with-pprof
name: prometheus-memory-profiling-with-pprof
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-pprof, heap-profile, go-pprof, prometheus-memory, gomemlimit, oomkilled]
level: advanced
status: docs-checked
description: "Profile Prometheus memory with /debug/pprof: capture heap profiles, read them with go tool pprof, map hotspots to series, queries or remote write, set GOMEMLIMIT."
sources: ["https://pkg.go.dev/net/http/pprof", "https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling Prometheus memory

## 1. Capture
The `/debug/pprof/` paths are the standard Go `net/http/pprof` handlers:
```bash
curl -s http://prom:9090/debug/pprof/heap > heap.pb.gz
curl -s 'http://prom:9090/debug/pprof/profile?seconds=30' > cpu.pb.gz
# or promtool, which fetches profiling debug information:
promtool debug pprof http://prom:9090
```
Take heap profiles at steady state and during the spike you're investigating.

## 2. Read
```bash
go tool pprof heap.pb.gz
```
Attribute the hottest frames to head series (cardinality and churn), PromQL evaluation (big queries), remote write buffers or scrape parsing. Take two heap profiles and compare them to see what grew.

## 3. Rough sizing
Memory scales with active head series plus query and remote-write overhead. Compare the head `numSeries` from
`/api/v1/status/tsdb` with the process memory; a large gap points at queries or remote write rather than series.

## 4. GOMEMLIMIT
`--auto-gomemlimit` (default true) sets GOMEMLIMIT to match the container or system memory limit, and
`--auto-gomemlimit.ratio` (default 0.9) is the share of that limit used. If the flag is unavailable, set the
`GOMEMLIMIT` env var yourself. It reduces spikes; it doesn't fix cardinality.

## Checked
2026-10-31. Confirmed: `/debug/pprof/heap`, `profile?seconds=30` and the `go tool pprof` usage (Go net/http/pprof docs), `promtool debug pprof <server>` (promtool page), `--auto-gomemlimit` default true and `--auto-gomemlimit.ratio` default 0.9 (command-line page), `/api/v1/status/tsdb` `headStats.numSeries`. Removed: per-series KiB sizing, Go frame names, pprof flags, metric names and the goroutine debug URL (not in the fetched docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Top heap consumers are attributed (series, queries, remote write, scrape).
- [ ] After the fix, heap steady state is lower in a before/after comparison.
- [ ] No OOMKilled restarts.
