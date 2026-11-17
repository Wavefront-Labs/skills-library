---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-performance-tuning-webhook-and-audit
name: opa-gatekeeper-performance-tuning-webhook-and-audit
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, performance, gomaxprocs, max-serving-threads, audit, memory, tuning]
level: sme
status: docs-checked
description: "Tune Gatekeeper performance with GOMAXPROCS, --max-serving-threads and the audit interval, chunk size and match-kind-only settings."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/performance-tuning.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper performance tuning webhook and audit

Webhook:
- `GOMAXPROCS` defaults to the container CPU limit via automaxprocs; override with the environment variable. Too many threads cause CPU throttling, jitter and higher latency.
- `--max-serving-threads` caps concurrent goroutines calling policy evaluation. Too many starve CPU and time requests out, and each holds RAM until its request ends, risking OOM. Default is `GOMAXPROCS`. Policies that mostly block on `http.send()` or external data are less CPU-bound, though memory still scales. Experiment to maximise webhook throughput.

Audit:
- `--audit-interval` should be long enough that at most one audit runs at once. Overlap causes parallel evaluation (RAM, CPU), more API requests, and a newer run can pre-empt reporting of an older run in constraint status (stdout logs unaffected).
- `--constraint-violations-limit`: memory grows with the limit.
- `--audit-chunk-size`: paginated listing lowers peak memory, helpful for kinds with many or large objects (ConfigMaps). The API continue token is valid only for minutes, so a very small chunk size plus throttling can let it expire mid-listing.
- `--audit-match-kind-only`: cuts runtime and memory if constraints target few kinds; no gain if a constraint matches all kinds.

## Checked

2026-11-04. Confirmed against performance-tuning.md. Removed or corrected: nothing.

Method: documentation only; no commands were run.
