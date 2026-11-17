---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-clickhouse-experimental
name: jaeger-clickhouse-experimental
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, clickhouse, storage-clickhouse-feature-gate, create-schema, feature-gates]
level: advanced
status: docs-checked
description: "Try the experimental ClickHouse backend by enabling the storage.clickhouse feature gate and create_schema."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/clickhouse/
  - https://www.jaegertracing.io/docs/2.22/deployment/delivery-guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: evaluate ClickHouse 26.x for Jaeger.

ClickHouse storage is experimental and must be explicitly enabled via the `storage.clickhouse` feature gate. The schema is subject to breaking changes in future releases. Supported ClickHouse versions: 26.x.

Quick start from the Jaeger repository root:
1. `docker compose -f docker-compose/clickhouse/docker-compose.yml up -d` starts ClickHouse on ports 9000 (native) and 8123 (HTTP) with database `jaeger`.
2. `go run ./cmd/jaeger --config cmd/jaeger/config-clickhouse.yaml --feature-gates=storage.clickhouse`
3. Generate data: `go run ./cmd/tracegen -duration 10s -workers 3 -pause 250ms`, then open http://localhost:16686.

The sample config sets `create_schema: true`, so all tables are created at startup; auxiliary tables are populated by materialized views that transform and insert data as spans arrive. All SQL definitions are in the sql/ directory of the repository. config.go is the authoritative configuration source, and the sample is config-clickhouse.yaml.

ClickHouse writes are synchronous and return errors on failure, which matters for delivery guarantees. The delivery guarantees page lists ClickHouse with Cassandra as storages that always report failures.

## Checked

2026-11-03. Confirmed against the ClickHouse page: experimental status, storage.clickhouse feature gate, schema breaking-change warning, supported 26.x, the three quick start commands and ports, create_schema with materialized views, the sql/ directory and sample config. The delivery-guarantee remark is from the Delivery Guarantees page. Nothing removed.
Method: documentation only; no commands were run.
