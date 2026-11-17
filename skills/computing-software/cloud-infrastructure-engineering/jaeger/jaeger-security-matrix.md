---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-security-matrix
name: jaeger-security-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, tls-mtls, bearer-token, security-matrix, jaeger-ui-auth]
level: practitioner
status: docs-checked
description: "See which TLS, mTLS and authentication mechanisms Jaeger supports per connection, including storage backends."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: secure each Jaeger hop.

- SDK to collector: OTLP over HTTP or gRPC, TLS with mTLS (client certificate authentication) supported. Covers span export and sampling configuration queries.
- Collector/ingester/query to storage:
  - Cassandra: TLS, mTLS, basic
  - Elasticsearch: TLS, mTLS, basic, bearer token, API key (bearer token propagation)
  - OpenSearch: TLS, mTLS, basic, bearer token, API key
  - Kafka: TLS, mTLS, basic, Kerberos (plaintext also possible)
  - Prometheus (for SPM): TLS, mTLS, basic, given a correctly configured Prometheus
  No Kerberos for Cassandra, Elasticsearch, OpenSearch or Prometheus; no bearer or API key for Cassandra, Kafka or Prometheus.
- Browser to UI: HTTP with TLS and bearer token authentication (pass-through to storage).
- Consumers to query: HTTP and gRPC, TLS with mTLS supported.

UI authentication: the page links blog posts on protecting the UI with an OAuth sidecar proxy and on an Apache httpd reverse proxy on OpenShift.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Securing Jaeger Installation page, read in full (connection list and storage support table). Removed the claims about the UI having no accounts, HAProxy/NGINX/Keycloak proxies, and the Prometheus token_file_path settings, none of which that page states.

Method: documentation only; no commands were run.
