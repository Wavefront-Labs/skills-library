---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.alerting-monitors-triggers
name: alerting-monitors-triggers
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, alerting-monitors-triggers, os-alerting]
level: practitioner
status: docs-checked
description: "Create per-query or bucket-level monitors with triggers and notification channels in OpenSearch."
sources:
  - https://docs.opensearch.org/latest/observing-your-data/alerting/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alerting monitors, triggers and destinations

**Goal:** notify on conditions in data (OpenSearch Alerting plugin).
- `POST _plugins/_alerting/monitors` with `"monitor_type": "query_level_monitor"` (or `bucket_level_monitor`), a `schedule` (for example `"period": {"interval": 1, "unit": "MINUTES"}`), `inputs[].search` (`indices` and `query`), and `triggers[]` whose `condition.script` is a Painless `source` such as `ctx.results[0].hits.total.value > 0`.
- Query-level monitors can trigger only one alert at a time; bucket-level monitors use a `bucket_level_trigger`.
- Trigger `actions` carry a `message_template`, optional `subject_template` and `throttle`. Destinations were deprecated in OpenSearch 2.0 and replaced by notification channels; configure delivery with the Notifications API.
- Test: `POST _plugins/_alerting/monitors/<id>/_execute?dryrun=true` shows the run's results without actions sending any message.

## Verify
- [ ] The dry run response shows `trigger_results.<trigger-id>.triggered` as `true` for a known matching dataset.

## Checked
Date: 2026-11-07
- OpenSearch Alerting API page: read the create query-level monitor section (request body, trigger condition script, action fields, destinations-deprecated note), the monitor options area by search, and the Run monitor section including the `dryrun=true` sentence and example response (`trigger_results`, `triggered`). The page is long; the bucket-level, document-level, update, delete, acknowledge and comment sections were located by search and not read in full.
- Removed: the list of Slack/email/webhook channel types, the advice on webhook secrets, and the claim that wide time ranges every minute add load (none on the page).
- The only page cited is the OpenSearch Alerting API; the skill covers the OpenSearch plugin only.
Method: documentation only; no commands were run.
