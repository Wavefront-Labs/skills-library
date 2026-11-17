---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-opensearch-setup
name: jaeger-opensearch-setup
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, opensearch, es-compatible, opensearch-versions, ping-endpoint]
level: practitioner
status: docs-checked
description: "Run Jaeger on OpenSearch 1.x to 3.x, which reuses the Elasticsearch implementation, write modes and poison-pill handling."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/opensearch/
  - https://www.jaegertracing.io/docs/2.22/storage/
  - https://www.jaegertracing.io/docs/2.22/deployment/security/
  - https://www.jaegertracing.io/docs/2.22/architecture/spm/
  - https://www.jaegertracing.io/docs/2.22/architecture/sampling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use OpenSearch as trace storage.

Supported versions: 1.x, 2.x and 3.x. OpenSearch keeps API compatibility between versions, primarily with Elasticsearch v7.10.2; this version is retrieved automatically from the root/ping endpoint, and Jaeger picks compatible index mappings and REST API from it.

OpenSearch needs no initialization other than installing and running it. Then pass correct configuration values to Jaeger using the `opensearch` backend type in the `jaeger_storage` extension.

Jaeger uses the same implementation for OpenSearch as for Elasticsearch, so most of the Elasticsearch page applies, including write modes (`write_mode`), poison-pill handling, index strategies and the rollover tools.

Community resources listed: Docker container, Helm chart and Kubernetes operator.

Security matrix: OpenSearch supports TLS, mTLS, basic auth, bearer token and API key, but not Kerberos.

The storage page recommends OpenSearch over Cassandra for large-scale production. SPM can compute RED metrics directly from OpenSearch by pointing both `storage.traces` and `storage.metrics` of `jaeger_query` at the same backend, and adaptive sampling can use it as `sampling_store`.

## Checked

2026-11-03. Confirmed against the OpenSearch page: supported 1.x to 3.x, compatibility with Elasticsearch v7.10.2 via root/ping, no initialization, shared implementation with Elasticsearch, and the community resources. The security row is from the Securing Jaeger page, the OpenSearch recommendation from the Storage page, SPM from the SPM page and sampling_store from the Sampling page. Nothing removed.
Method: documentation only; no commands were run.
