---
id: computing-software.messaging-and-integration.dapr.logging-json-format-and-schema
name: logging-json-format-and-schema
category: computing-software
field: messaging-and-integration
product: dapr
tags: [logging, json, log-as-json, helm, annotations, log-schema, fluentd, observability]
level: practitioner
status: docs-checked
description: "Dapr structured logs: field schema (time, level, type, msg, scope, instance, app_id, ver), plain versus JSON, --log-as-json, global.logAsJson and dapr.io/log-as-json."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/observability/logging/logs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All Dapr processes (sidecar and control plane services) write structured logs to stdout. The default is plain text; JSON is recommended whenever a collector or search engine such as Elasticsearch or Azure Monitor will parse them.

Schema fields: `time` (ISO8601), `level` (info/warn/debug/error), `type` (`log`), `msg`, `scope` (for example `dapr.runtime`), `instance` (container name), `app_id`, `ver` (runtime version). API logging may add more structured fields.

Plain text looks like `time="2022-11-01T17:08:48.303776-07:00" level=info msg="starting Dapr Runtime -- version 1.9.0 ..." instance=dapr-pod-xxxx scope=dapr.runtime type=log ver=1.9.0`; JSON carries the same keys as `{"instance":"dapr-pod-xxxx","level":"info","msg":"...","scope":"dapr.runtime","time":"...","type":"log","ver":"1.9.0"}`.

Enable JSON:

```sh
dapr run \
  --app-id orderprocessing \
  --resources-path ./components/ \
  --log-as-json \
    -- python3 OrderProcessingService.py
```

Kubernetes control plane (every control plane service supports `--log-as-json`; with Helm):

```bash
helm upgrade --install dapr \
  dapr/dapr \
  --namespace dapr-system \
  --set global.logAsJson=true
```

Sidecars: annotate the Deployment pod template with `dapr.io/log-as-json: "true"`.

Collectors: Fluentd with its JSON parser plugin is the popular choice on Kubernetes, paired with Elasticsearch and Kibana; on AKS the built-in agent with Azure Monitor works without Fluentd. Log level and API logging are covered by the logs and API logs troubleshooting pages.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
