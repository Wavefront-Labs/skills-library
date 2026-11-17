---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.ocb-containerize-distribution
name: ocb-containerize-distribution
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, ocb, docker, dockerfile, kubernetes, custom-distribution]
level: advanced
status: docs-checked
description: "Build a custom Collector image by running ocb inside a Dockerfile so the binary matches the container architecture."
sources:
  - https://opentelemetry.io/docs/collector/extend/ocb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To deploy a custom Collector on Kubernetes or another orchestrator, build it inside a `Dockerfile`, which keeps the binary matched to the target architecture such as `linux/arm64` or `linux/amd64`. Add `Dockerfile` and `collector-config.yaml` next to `builder-config.yaml`.

The Dockerfile has three stages:

- `FROM alpine:3.19 AS certs` installs `ca-certificates`.
- `FROM golang:1.25.0 AS build-stage` copies the manifest, runs `go install go.opentelemetry.io/collector/cmd/builder@<version>`, then `builder --config builder-config.yaml`.
- `FROM gcr.io/distroless/base:latest` sets `USER` to 10001, copies `collector-config.yaml`, the certificates and the built binary with `COPY --chmod=755 --from=build-stage /build/otelcol-dev /otelcol`, and sets `ENTRYPOINT ["/otelcol/otelcol-dev"]`, `CMD ["--config", "/otelcol/collector-config.yaml"]` and `EXPOSE 4317 4318 12001`.

If you change `name` or `output_path` in `dist`, update the `COPY` and `ENTRYPOINT` lines to the new distribution name.

The test `collector-config.yaml` has an `otlp` receiver on `0.0.0.0:4317` and `0.0.0.0:4318`, a `debug` exporter with `verbosity: detailed`, and pipelines for traces, metrics and logs.

Multi-architecture build:

```sh
docker run --rm --privileged tonistiigi/binfmt --install all
docker buildx create --name mybuilder --use
docker buildx build --load -t <image>:<version> --platform=linux/amd64,linux/arm64 .
docker run -it --rm -p 4317:4317 -p 4318:4318 --name otelcol <image>:<version>
```

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/extend/ocb/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
