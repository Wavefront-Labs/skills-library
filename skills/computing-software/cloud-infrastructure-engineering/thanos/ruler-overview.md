---
id: computing-software.cloud-infrastructure-engineering.thanos.ruler-overview
name: ruler-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-rule, ruler, recording-rules, alerting-rules]
level: practitioner
status: docs-checked
description: "Decide whether to use Thanos Ruler and run it against Query API endpoints."
sources: ["https://thanos.io/tip/components/rule.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ruler overview

The docs recommend keeping rules inside the relevant Prometheus servers; use `thanos rule` only for specific cases and not to avoid proper rule deployment in configuration management.

`thanos rule` evaluates Prometheus recording and alerting rules against the chosen query API given by repeated `--query` (or file SD via `--query.sd-files`). With more than one query, it round-robins. Results are written locally as TSDB blocks and can be uploaded.

**Risk.** Prometheus evaluates rules locally, so failure is unlikely; Ruler depends on a distributed read path through the Querier and remote stores, so query failures are likelier. Have a plan for alerts during query unavailability.

Key defaults: `--eval-interval=1m`, `--rule-file=rules/` (glob, repeatable; rules are not auto-detected, so use SIGHUP or POST `/-/reload`), `--data-dir=data/`, `--tsdb.block-duration=2h`, `--tsdb.retention=48h`, `--resend-delay=1m`, `--query.http-method=POST`, `--rule-concurrent-evaluation=1`.

Restore of alert `for` state uses `--for-outage-tolerance=1h` and `--for-grace-period=10m`.

**Performance.** Ruler does little work itself; split rules over HA pairs for functional sharding.

Each alert in the Ruler UI links to the query it runs, using `--alert.query-url`.

## Checked

2026-11-03. Confirmed against the Thanos Ruler page (components/rule.md) and the Thanos tools page (rules-check): defaults, HA external labels and alert.label-drop, mon1/eu1 label example, partial_response_strategy default abort, stateless mode via remote write, rules-check behaviour and exit codes. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
