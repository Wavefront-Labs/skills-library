---
id: computing-software.cloud-infrastructure-engineering.cortex.cortex-architecture-overview
name: cortex-architecture-overview
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [architecture, microservices, multi-tenancy, remote-write, blocks-storage]
level: intro
status: docs-checked
description: "Orient on Cortex's microservice layout, the tenant ID header, Prometheus remote write, and which services are stateless or semi-stateful."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex is a set of horizontally scalable microservices. Most are stateless and can serve any tenant; the ingesters are semi-stateful and depend on consistent hashing. A single-process mode runs every component in one process, handy for local testing and development.

Services: distributor, ingester, querier, compactor, store gateway (required), plus optional alertmanager, configs API, overrides exporter, query frontend, query scheduler and ruler.

Prometheus servers scrape targets and push samples to Cortex over the remote write API (batched, Snappy-compressed protobuf). Writes are handled by the distributor, reads (PromQL) by the querier or optionally the query frontend.

Every HTTP request must carry a header with the tenant ID. Cortex does no authentication itself; an external reverse proxy handles authentication and authorization and sets the tenant header.

Blocks storage is based on Prometheus TSDB: each tenant's series go into their own TSDB, written as on-disk blocks with a default 2h range. It needs no dedicated index store, only an object store for the blocks: Amazon S3, Google Cloud Storage, Azure Storage, OpenStack Swift, or the local filesystem (single node only).

Statefulness summary: distributor, querier, compactor, query frontend, query scheduler and configs API are stateless; ingester, store gateway, ruler and alertmanager are semi-stateful.

## Checked

Method: docs-checked 2026-11-09 against the full Cortex architecture.md (raw markdown, master). Corrected the object-store list to match the page (local filesystem, single node only, rather than "any S3-compatible store").
