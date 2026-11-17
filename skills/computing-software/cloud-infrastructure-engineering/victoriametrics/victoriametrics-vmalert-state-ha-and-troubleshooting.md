---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmalert-state-ha-and-troubleshooting
name: victoriametrics-vmalert-state-ha-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmalert, state-restore, high-availability, replay, multitenant, troubleshooting]
level: advanced
status: docs-checked
description: "Restore vmalert alert state, run it highly available, replay rules and troubleshoot empty or late alerts."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmalert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmalert state ha and troubleshooting

State restoration needs both `-remoteWrite.url` and `-remoteRead.url`. It happens once at startup (hot reload does not restore), uses `-remoteRead.lookback` (default 1h), and restored alerts get a `restored` label in the UI. It can fail if series are missing, older than the lookback, or do not match the current rules.

High availability: run several identically configured vmalert instances; each notifies all listed Alertmanagers. On VictoriaMetrics set `-dedup.minScrapeInterval` equal to `-evaluationInterval` (or a common multiple when groups differ).

Replay mode back-fills recording rules with `-replay.timeFrom`, `-replay.timeTo`, `-replay.maxDatapointsPerQuery`, `-replay.rulesDelay` and `-replay.ruleEvaluationConcurrency`.

Multi-tenancy: run one instance per tenant with the tenant ID in the datasource and remote write URL paths, or use the multitenant endpoint with `extra_label` params `vm_account_id` and optionally `vm_project_id` (restrict access to trusted sources). Enterprise `-clusterMode` allows a `tenant` per group. Run vmalert behind VictoriaMetrics with `-vmalert.proxyURL` to expose its UI and API.

Troubleshooting:
- Keep group intervals at or above series resolution and lookbehind windows at least 2x resolution; with 5m or coarser resolution set `-datasource.queryStep` to at least 2x.
- Use explicit lookbehind windows in rollups and subqueries.
- Empty results are often data delay: check `-search.latencyOffset` and `-rule.evalDelay`.
- Set `debug: true` on a rule or group with `-loggerLevel=INFO`, and use the rule Details page (last N updates, cURL samples).
- For rule chaining keep the dependent rule interval under 5 minutes.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
