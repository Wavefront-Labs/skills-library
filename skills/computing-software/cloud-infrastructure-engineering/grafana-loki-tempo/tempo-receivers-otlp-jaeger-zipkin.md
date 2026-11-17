---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-receivers-otlp-jaeger-zipkin
name: tempo-receivers-otlp-jaeger-zipkin
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-receivers, tempo, otlp-grpc, otlp-http, jaeger-receiver, zipkin-receiver, distributor]
level: practitioner
status: docs-checked
description: "Enable Tempo distributor receivers for OTLP gRPC and HTTP, Jaeger and Zipkin, bind external addresses, push a test span and debug ingestion."
sources: ["https://grafana.com/docs/tempo/latest/configuration/#distributor", "https://grafana.com/docs/tempo/latest/api_docs/pushing-spans-with-http/", "https://grafana.com/docs/tempo/latest/troubleshooting/querying/unable-to-see-trace/", "https://grafana.com/docs/tempo/latest/set-up-for-tracing/setup-tempo/deploy/kubernetes/tanka/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: accept spans from SDKs and collectors on the right protocols.

Receivers are configured under `distributor.receivers` and passed to OpenTelemetry receivers. The configuration reference lists these (enable only what you need in production):
```yaml
distributor:
  receivers:
    otlp:
      protocols:
        grpc:    # default localhost:4317
        http:    # default localhost:4318
    jaeger:
      protocols:
        thrift_http:
        grpc:
        thrift_binary:
        thrift_compact:
    zipkin:
    kafka:
```
By default receivers listen on localhost, so set an IP to accept external traffic, for example `grpc: { endpoint: 0.0.0.0:4317 }`. The Tanka guide's example exposes OTLP gRPC on 4317 and Jaeger gRPC on 14250 (`endpoint: '0.0.0.0:14250'`). Check the receiver README linked from the configuration page for other protocol defaults.

Push a test span over OTLP/HTTP (set `startTimeUnixNano` and `endTimeUnixNano` to current nanosecond times, e.g. `date +%s%N` on Linux):
```
curl -X POST -H 'Content-Type: application/json' http://localhost:4318/v1/traces -d '{"resourceSpans": [ ... ]}'
```

Distributor behaviour depends on mode: in microservices mode it writes to Kafka; in monolithic mode (`target: all`) it pushes in-process to the live-store and metrics-generator.

Debug options (not for production): `distributor.log_received_spans.enabled`, `log_discarded_spans`, `metric_received_spans`. `retry_after_on_resource_exhausted` defaults to 5s; the per-tenant `ingestion.retry_info_enabled` override can disable it.

Gotchas
- Wrong protocol/port pairing is the first cause of zero received spans; some SDKs default to e.g. Thrift Compact over UDP (Jaeger Go client).
- SDK probabilistic samplers may drop most spans before they leave the app.
- In Docker, send to `tempo:<receiver-port>`.

## Verify
`tempo_distributor_spans_received_total` and `tempo_live_store_traces_created_total` should be above 0 within minutes; `tempo_receiver_accepted_spans` has a receiver label (e.g. `jaeger-thrift`).

## Checked
2026-11-03. Confirmed against the Tempo configuration reference (distributor block), the push-spans guide, the unable-to-see-trace troubleshooting page and the Tanka deployment page. Removed: unconfirmed default ports for Jaeger thrift_http, Zipkin and Jaeger agent protocols, `tls: {cert_file, key_file}` snippet, SDK env var export, "gRPC through L7 needs HTTP/2" and the curl metrics grep.
Method: documentation only; no commands were run.
