---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-build-pipelines
name: grafana-alloy-build-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [pipelines, forward-to, fan-out, localfile, component-exports, is-secret]
level: intro
status: docs-checked
description: "Connect Alloy components into pipelines with exports, references and forward_to, including fan-out and chained loki.process stages."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/components/build-pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Building Alloy pipelines

A pipeline forms when one component references another component's exports. Referencing `local.file.api_key.content` in an argument creates a dependency, and when the file changes Alloy updates the consumer automatically.

```alloy
local.file "api_key" {
  filename  = "/etc/secrets/api-key"
  is_secret = true
}
prometheus.remote_write "production" {
  endpoint {
    url = "https://prometheus.example.com/api/v1/write"
    basic_auth {
      username = "metrics"
      password = local.file.api_key.content
    }
  }
}
```

`forward_to` is the attribute that creates data-flow connections. It takes a list of receivers, for example `[prometheus.remote_write.production.receiver]`.

## Patterns
- **Fan-out**: list several receivers in one `forward_to` (for example production and staging remote_write) to test changes, split datasets or keep redundant copies.
- **Chain**: `loki.source.file` forwards to `loki.process "parse"` (stage.json), then to `loki.process "filter"` (stage.match with selector `{level="error"}`, action `keep`), then `loki.write`.

## Guidance
- Give components descriptive labels (`api_metrics`, not `scraper1`) and keep each one single-purpose.
- Set `is_secret = true` on `local.file` so the value is hidden in the UI.
- Debug in the UI: unhealthy components show red, inspect exports, check `forward_to` targets are receiver exports, and remember components cannot reference themselves directly or indirectly.

## Checked

2026-11-08. Read the Build data pipelines page in full. Confirmed: pipelines from references and automatic reevaluation, the local.file to remote_write example, `forward_to` semantics, fan-out and chain patterns with the stage.match selector and keep action, labelling and single-purpose guidance, `is_secret = true`, and the debugging steps.

Method: documentation only; no commands were run.
