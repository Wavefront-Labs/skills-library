---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-all-in-one-docker
name: jaeger-all-in-one-docker
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, all-in-one, docker-run, in-memory-storage, port-16686]
level: intro
status: docs-checked
description: "Run Jaeger v2 all-in-one in a container with the documented ports, then load the UI on 16686 and supply a config via --config."
sources:
  - https://www.jaegertracing.io/docs/2.22/getting-started/
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start a throwaway Jaeger with UI and OTLP ingest.

```
docker run --rm --name jaeger \
  -p 16686:16686 -p 4317:4317 -p 4318:4318 -p 5778:5778 -p 9411:9411 \
  cr.jaegertracing.io/jaegertracing/jaeger:2.22.0
```
This is the all-in-one configuration: collector and query in a single process with transient in-memory storage. Open http://localhost:16686 for the UI. Port roles: 16686 UI, 4317 OTLP gRPC, 4318 OTLP HTTP, 5778 remote sampling, 9411 Zipkin.

To run any other role you must supply an explicit configuration file with the `--config` argument. In a container, map the file into the container filesystem:
```
docker run --rm --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 -p 5778:5778 -p 9411:9411 \
  -v /path/to/local/config.yaml:/jaeger/config.yaml \
  cr.jaegertracing.io/jaegertracing/jaeger:2.22.0 --config /jaeger/config.yaml
```
Applications must be instrumented before they send data; the docs recommend OpenTelemetry instrumentation and SDKs. The HotROD demo (run with docker compose from examples/hotrod in the Jaeger repository, then browse http://localhost:8080) generates sample traces.

Failure mode: data is held in memory only and is lost when the process exits, so do not use this for production.

## Checked

2026-11-03. Confirmed against the Getting Started page: the docker run command and ports, the all-in-one description with transient in-memory storage, --config with a mapped file for other roles, the instrumentation advice and the HotROD docker compose steps; port roles are from the APIs page. Nothing removed.
Method: documentation only; no commands were run.
