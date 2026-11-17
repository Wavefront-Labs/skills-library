---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-loki-source-file-and-process-stages
name: alloy-loki-source-file-and-process-stages
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-process, alloy, loki.source.file, loki.write, stage-regex, stage-json, stage-labels, stage-drop]
level: practitioner
status: draft
description: "Collect files with Alloy and shape logs using loki.process stages (json, regex, labels, drop, timestamp) before loki.write."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: parse, label and filter logs at the edge.

```
local.file_match "app" {
  path_targets = [{"__path__" = "/var/log/app/*.log", "job" = "app"}]
}

loki.source.file "app" {
  targets    = local.file_match.app.targets
  forward_to = [loki.process.app.receiver]
}

loki.process "app" {
  stage.json {
    expressions = { level = "level", ts = "time", msg = "message", trace_id = "trace_id" }
  }
  stage.timestamp {
    source = "ts"
    format = "RFC3339"
  }
  stage.labels {
    values = { level = "" }
  }
  stage.structured_metadata {
    values = { trace_id = "" }
  }
  stage.drop {
    expression = "healthcheck"
  }
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```
Other stages: `stage.regex`, `stage.multiline`, `stage.match`, `stage.replace`, `stage.static_labels`, `stage.limit`, `stage.template`, `stage.output`.

Gotchas
- Only promote low-cardinality fields (level, not user id) to labels.
- `stage.multiline` must come first to join stack traces.
- Positions are stored under the data path; deleting it re-reads files from the start.
- Alloy needs read access to the files and the container's data dir for positions.

## Verify
Open the Alloy UI component page for `loki.process.app` to see stage processed counts, and query `{job="app"} | level="error"` in Loki.
