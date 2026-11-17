---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.install-docker-and-compose
name: install-docker-and-compose
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, install, docker, compose, ports, otlp]
level: intro
status: docs-checked
description: "Run the Collector in Docker or Compose, mount config at /etc/otelcol/config.yaml and publish the standard ports."
sources:
  - https://opentelemetry.io/docs/collector/install/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pull and run the Collector image from Docker Hub or ghcr.io:

```sh
docker pull otel/opentelemetry-collector:<version>
docker run otel/opentelemetry-collector:<version>
docker pull ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector:<version>
```

Replace `<version>` with the Collector version you want. To load a custom configuration from your working directory, mount it as a volume:

```sh
docker run -v $(pwd)/config.yaml:/etc/otelcol/config.yaml otel/opentelemetry-collector:<version>
```

To add the Collector to an existing `docker-compose.yaml`:

```yaml
otel-collector:
  image: otel/opentelemetry-collector
  volumes:
    - ./otel-collector-config.yaml:/etc/otelcol/config.yaml
  ports:
    - 1888:1888 # pprof extension
    - 8888:8888 # Prometheus metrics exposed by the Collector
    - 8889:8889 # Prometheus exporter metrics
    - 13133:13133 # health_check extension
    - 4317:4317 # OTLP gRPC receiver
    - 4318:4318 # OTLP http receiver
    - 55679:55679 # zpages extension
```

The `otel-collector-config.yaml` file is required for the Collector to start. The page's minimal configuration has an `otlp` receiver with gRPC on `0.0.0.0:4317` and HTTP on `0.0.0.0:4318`, a `debug` exporter with `verbosity: detailed`, and traces, metrics and logs pipelines wiring one to the other.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/install/docker/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
