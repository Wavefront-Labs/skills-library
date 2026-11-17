---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmalert-rules-and-templating
name: victoriametrics-vmalert-rules-and-templating
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmalert, alerting-rules, recording-rules, rule-groups, templating, notifier]
level: practitioner
status: docs-checked
description: "Run vmalert rule groups with the right datasource, notifier and remote write flags, group fields and templates."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmalert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmalert rules and templating

Core flags: `-rule` (files, wildcards, HTTP URLs), `-datasource.url` (query endpoint), `-notifier.url` (repeat for several Alertmanagers), `-remoteWrite.url` (required for recording rules and alert state), `-remoteRead.url` (state restore), `-external.label`, `-external.url`, `-dryRun` with `-rule` to validate syntax, `-rule.templates`.

Group fields: `name` (required, unique per file), `interval` (defaults to `-evaluationInterval`), `eval_offset` (cannot combine with `eval_delay`), `eval_delay`, `limit` (0 means none), `concurrency` (default 1), `type` (`prometheus`, `graphite`, `vlogs`), `eval_alignment` (default true), `params` (such as `nocache`, `denyPartialResponse`, `extra_label`), `headers`, `notifier_headers`, `labels`, `debug`, `rules`.

Alerting rule fields: `alert`, `expr`, `for` (default 0s), `keep_firing_for`, `labels`, `annotations`, `debug`, `update_entries_limit`. Recording rules: `record`, `expr`, `labels` (no templating), `debug`.

Templating variables: `$value`, `$labels`, `$activeAt`, `$expr`, `$for`, `$type`, `$alertID`, `$groupID`, `$externalLabels`, `$externalURL`, `$isPartial`, `$interval`; functions include `query`, `first`, `label`, `humanize`, `humanizeDuration`, `humanizeTimestamp`, `queryEscape`. Do not put `$value` in labels: a changing value creates a new alert and resets the `for` timer.

Defaults: `-rule.evalDelay` 30s, `-datasource.queryStep` 5m, `-rule.defaultRuleType` prometheus. Endpoints: `/api/v1/rules`, `/api/v1/alerts`, `/api/v1/notifiers`, `/-/reload`, metrics on port 8880.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
