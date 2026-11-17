---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-remote-storage-component
name: jaeger-remote-storage-component
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-remote-storage, port-17271, badger-shared, single-node-storage]
level: advanced
status: docs-checked
description: "Use the jaeger-remote-storage service to share Badger or memory storage between separate collector and query processes."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/tools/
  - https://www.jaegertracing.io/docs/2.22/storage/badger/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run split collector and query services on a single-node storage.

Single-node backends (memory store, Badger) cannot be shared between multiple processes, so without help they only work in all-in-one. `jaeger-remote-storage` implements the Remote Storage gRPC API and proxies it into one of the regular Jaeger backends. Run a full deployment of separate collector and query services, point them at it via the `grpc` storage type, and keep the single-node store behind it.

Default ports of the service:
- 17271 gRPC: Remote Storage API
- 17270 HTTP: admin port; health check at `/` and metrics at `/metrics`

Why it is needed: the Badger page says that if Badger is enabled in a collector it cannot be accessed from jaeger-query, and vice versa, so Badger can be used only in all-in-one or with the remote storage component.

Badger itself is an embeddable persistent key-value database similar to RocksDB, embedded in the Jaeger binary. Pros: data in the local filesystem survives restarts, and a single node sustains high throughput. Con: only suitable for single-node deployments; it cannot scale horizontally.

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 tools and Badger pages (read in full).
