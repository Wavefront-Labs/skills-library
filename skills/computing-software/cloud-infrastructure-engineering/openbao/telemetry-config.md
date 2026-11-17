---
id: computing-software.cloud-infrastructure-engineering.openbao.telemetry-config
name: telemetry-config
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, telemetry, prometheus, statsd, metrics]
level: practitioner
status: docs-checked
description: "OpenBao telemetry stanza: Prometheus retention, statsd and dogstatsd, hostname labels, prefix filters and sys/metrics caveats."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/telemetry.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Telemetry stanza

## Defaults

- `usage_gauge_period` `"10m"` (`"none"` disables); `maximum_gauge_cardinality` 500
- `disable_hostname` false; `enable_hostname_label` false
- `metrics_prefix` `"vault"`
- `lease_metrics_epsilon` `"1h"`; `num_lease_metrics_buckets` 168; `add_lease_metrics_namespace_labels` false
- `filter_default` true; `prefix_filter` empty (`+` allows, `-` blocks a prefix)
- `prometheus_retention_time` `"24h"`; `0` disables Prometheus telemetry
- `statsd_address`, `dogstatsd_addr` default empty; `dogstatsd_tags` list of `"name:value"`

## Fetching Prometheus metrics

`/v1/sys/metrics` needs a token with read and list capabilities. Pass the format as a parameter; `?format=prometheus` in the path will not work.

## Gotchas

- `/v1/sys/metrics` works only on the active node and is disabled on standbys; unauthenticated metrics access can expose it on standbys.
- With `filter_default` false and no filters, nothing is sent.
- `add_lease_metrics_namespace_labels` can create a very large-cardinality metric.
- Docs recommend `disable_hostname` for Prometheus or Stackdriver, and `enable_hostname_label` for Stackdriver.

## Checked

2026-11-04. Read the OpenBao telemetry stanza page in full. Confirmed: all listed defaults, the `prefix_filter` format, `filter_default` behaviour, Prometheus retention, the `/v1/sys/metrics` active-node limitation, token capabilities and parameter-based format, the cardinality warning and the hostname recommendations. Removed: nothing.
Method: documentation only; no commands were run.
