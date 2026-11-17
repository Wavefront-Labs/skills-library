---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-tracing-block
name: grafana-alloy-tracing-block
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [tracing-block, sampling-fraction, send-traceparent, jaeger-remote, tracing-write-to, self-tracing]
level: practitioner
status: docs-checked
description: "Configure Alloy self-tracing with the tracing block: sampling_fraction, write_to otelcol consumers, send_traceparent and the jaeger_remote sampler."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/tracing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The tracing block

Optional, unlabeled, once per file. It controls traces Alloy produces about itself.

```alloy
tracing {
  sampling_fraction = 0.1
  send_traceparent  = true
  write_to          = [otelcol.exporter.otlp.tempo.input]
}
otelcol.exporter.otlp "tempo" {
  client {
    endpoint = sys.env("TEMPO_OTLP_ENDPOINT")
    tls {
      insecure = true
    }
  }
}
```

## Arguments
- `sampling_fraction` (default `0.1`): `1` or more keeps everything, `0` or less keeps nothing.
- `write_to` (default `[]`): any `otelcol` component accepting traces, including processors and exporters. An empty array drops all traces.
- `send_traceparent` (default `false`): send the `traceparent` header on outgoing requests.

Traces generated before the block is evaluated (early process start) are dropped.

## sampler > jaeger_remote
At most one sampler may be defined. `jaeger_remote` fetches sampling strategies by HTTP GET from `url` (default `http://127.0.0.1:5778/sampling`), always adding `service=alloy`; the response is JSON in the Jaeger `strategies.json` schema. `refresh_interval` defaults to `1m`; `max_operations` defaults to `256`, and beyond that the default sampler decides.

## Checked
2026-11-04: confirmed against the tracing block reference. Removed: nothing.
Method: documentation only; no commands were run.
