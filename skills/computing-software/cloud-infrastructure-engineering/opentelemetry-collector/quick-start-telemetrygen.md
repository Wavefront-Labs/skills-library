---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.quick-start-telemetrygen
name: quick-start-telemetrygen
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, quick-start, telemetrygen, otlp, debug-exporter]
level: intro
status: docs-checked
description: "Send test traces to a local Collector with telemetrygen and see them printed by the debug exporter."
sources:
  - https://opentelemetry.io/docs/collector/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The quick start runs a local Collector from the core distribution image and sends it generated traces. It needs Docker (or a compatible runtime), Go (one of the latest two minor versions) and `GOBIN` set, for example `export GOBIN=${GOBIN:-$(go env GOPATH)/bin}`.

1. Pull the image: `docker pull otel/opentelemetry-collector:<version>`.
2. Install the generator: `go install github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest`.
3. Start the Collector, saving its output:

```sh
docker run \
  -p 127.0.0.1:4317:4317 \
  -p 127.0.0.1:4318:4318 \
  -p 127.0.0.1:55679:55679 \
  otel/opentelemetry-collector:<version> \
  2>&1 | tee collector-output.txt
```

Port 4317 is OTLP over gRPC, 4318 is OTLP over HTTP, and 55679 is zPages, a debug UI.

4. In another terminal, generate traces:

```sh
$GOBIN/telemetrygen traces --otlp-insecure --traces 3
```

You see lines such as `traces generated {"worker": 0, "traces": 3}`.

5. Check the Collector output with `grep -E '^Span|(ID|Name|Kind|time|Status \w+)\s+:' ./collector-output.txt`. The page's sample shows spans named `okey-dokey` and `lets-go`, each with Trace ID, Parent ID, ID, Kind, times and status.
6. Press Control-C to stop the Collector.

The page says this demo shows how the Collector works and is not a production setup. It points next to configuration, deployment patterns, installation options and the component registry.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/quick-start page (docs repo raw markdown).
