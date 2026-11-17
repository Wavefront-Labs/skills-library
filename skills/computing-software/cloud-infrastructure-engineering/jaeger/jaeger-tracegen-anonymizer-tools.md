---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-tracegen-anonymizer-tools
name: jaeger-tracegen-anonymizer-tools
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, tracegen, anonymizer, firehose-mode, stress-test]
level: practitioner
status: docs-checked
description: "Generate load with jaeger-tracegen and share anonymized traces with jaeger-anonymizer."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/tools/
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
  - https://www.jaegertracing.io/docs/2.22/storage/cassandra/
  - https://www.jaegertracing.io/docs/2.22/storage/clickhouse/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stress test a deployment or share a trace safely.

Tracegen generates a continuous stream of simple spans, useful for stress testing. Flags control the number of workers and traces per worker, and it can emit spans in firehose mode, a flag set on spans to skip indexing.
`docker run --rm jaegertracing/jaeger-tracegen:2.22.0`
From source, the ClickHouse quick start uses: `go run ./cmd/tracegen -duration 10s -workers 3 -pause 250ms`.

Anonymizer takes a trace ID and outputs an anonymized JSON version, removing or hashing environment-specific details so you can share it for debugging:
```
docker run --rm --volume /tmp:/tmp jaegertracing/jaeger-anonymizer:2.22.0 \
  --trace-id <TRACE_ID> --query-host-port <JAEGER_QUERY_HOST_PORT>
```
Other utilities: `jaeger-es-rollover` and `jaeger-es-index-cleaner` for Elasticsearch/OpenSearch indices; `jaeger-cassandra-schema` for Cassandra schema; `jaeger-remote-storage` for sharing single-node stores.

## Checked

2026-11-03. Confirmed against the Tools page: tracegen purpose, worker and trace flags and firehose mode, the anonymizer command and what it removes or hashes, and the remote storage component. The tracegen source command matches the ClickHouse page quick start; rollover, index cleaner and Cassandra schema images match the Elasticsearch and Cassandra pages. Removed: the claim that backups and lifecycle are handled outside Jaeger (no fetched page states it) and a closing paragraph restating the commands with unverified detail.
Method: documentation only; no commands were run.
