---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-elasticsearch-setup
name: jaeger-elasticsearch-setup
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, elasticsearch, shards-replicas, es-version, config-elasticsearch-yaml]
level: practitioner
status: docs-checked
description: "Point Jaeger at Elasticsearch 7.x or 8.x, understand version autodetection and decide shards and replicas before indices exist."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
  - https://www.jaegertracing.io/docs/2.22/deployment/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use Elasticsearch as trace storage.

Supported versions: 7.x and 8.x. The version is retrieved automatically from the root/ping endpoint, and Jaeger uses compatible index mappings and REST API for it. You can force a version with the `version:` config property.

Elasticsearch needs no initialization other than installing and running it; then pass the configuration values to Jaeger. A sample is config-elasticsearch.yaml in the repository; config.go is the authoritative property list.

Shards and replicas deserve attention because they are decided when an index is created. The docs link an article on choosing shard counts.

Index defaults: Jaeger creates daily indices unless you use aliases (rollover); see the index strategy skills. Useful settings: `date_layout` (default 2006-01-02; use 2006-01-02-15 for hourly indices), `use_aliases` (false), `use_ilm` (false), `create_mappings` (true).

The security matrix shows Elasticsearch with TLS, mTLS, basic auth, bearer token and API key support, but no Kerberos.

Community resources mentioned: Docker container and Helm chart from Elastic, Kubernetes operator from RedHat.

## Checked

2026-11-03. Confirmed against the Elasticsearch page: supported versions 7.x and 8.x, version autodetection from root/ping and the version: property, no initialization needed, sample config and config.go, shards and replicas set at creation, date_layout and the other defaults, and the community resources. The security matrix row is from the Securing Jaeger page. Nothing removed.
Method: documentation only; no commands were run.
