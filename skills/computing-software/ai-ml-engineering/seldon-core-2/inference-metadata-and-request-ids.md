---
id: computing-software.ai-ml-engineering.seldon-core-2.inference-metadata-and-request-ids
name: inference-metadata-and-request-ids
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference, request-id, x-request-id, x-pipeline-version, pipeline-inspect, metadata-headers, tracing]
level: practitioner
status: docs-checked
description: "Pass X- metadata headers through a pipeline, read x-pipeline-version, and use x-request-id with seldon pipeline inspect to debug a single request."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline metadata and request IDs

## Metadata
Metadata can travel with an inference through the graph.
- Kafka: attach Kafka headers to the request.
- REST to a pipeline: add HTTP headers prefixed with `X-`.
- gRPC to a pipeline: add metadata keys that start with `X-`.
- CLI: `--header X-foo=bar`, and `--show-headers` to print response headers.

```bash
seldon pipeline infer --show-headers --header X-foo=bar tfsimples \
    "{\"inputs\":[{\"name\":\"INPUT0\",\"data\":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],\"datatype\":\"INT32\",\"shape\":[1,16]},{\"name\":\"INPUT1\",\"data\":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],\"datatype\":\"INT32\",\"shape\":[1,16]}]}"
```

A pipeline response also includes `x-pipeline-version`, the version of the pipeline that served the request.

## Request IDs
Every model and pipeline response carries an `x-request-id` header. If the caller supplies one it is used, and the caller must keep it unique. Generated ids are XIDs. The id also appears in tracing spans.

For pipelines, use it to inspect each step:

```bash
seldon pipeline inspect tfsimples --request-id carjjolvqj3j2pfbut10 --offset 10
```

`--offset` is how many messages back from the latest to search; without it the last request is shown.

## Checked

Confirmed against the Inference page (Pipeline Metadata and Request IDs sections): X- prefixed headers and metadata, CLI --header and --show-headers, x-pipeline-version, x-request-id behaviour and XIDs, and seldon pipeline inspect with --request-id and --offset.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb inference.md page (raw markdown).
