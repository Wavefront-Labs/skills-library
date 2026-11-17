---
id: computing-software.cloud-infrastructure-engineering.fluentd.docker-compose-efk-stack
name: docker-compose-efk-stack
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, docker-compose, efk, elasticsearch, kibana, dockerfile]
level: practitioner
status: docs-checked
description: "Compose an EFK stack: httpd with the Fluentd logging driver, a custom Fluentd image with the Elasticsearch plugin, and forward to elasticsearch output."
sources:
  - https://docs.fluentd.org/container-deployment/docker-compose
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd in Docker Compose (EFK)
Four services: `httpd`, `fluentd`, `elasticsearch`, `kibana`. The web service logs through Fluentd:
```
logging:
  driver: "fluentd"
  options:
    fluentd-address: localhost:24224
    tag: httpd.access
```
Fluentd publishes `24224` on TCP and UDP, mounts `./fluentd/conf` at `/fluentd/etc`, and `depends_on` Elasticsearch with `condition: service_healthy` (a healthcheck calling `/_cluster/health`). The page's Elasticsearch is single-node with security disabled for testing.

Custom image (`fluentd/Dockerfile`):
```
FROM fluent/fluentd:edge-debian
USER root
RUN ["gem", "install", "elasticsearch", "--no-document", "--version", "8.19.0"]
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.4.3"]
USER fluent
```
Elasticsearch 8 requires the matching `elasticsearch` gem.

`fluentd/conf/fluent.conf`: `forward` source on 24224, and a `copy` match with an `elasticsearch` store (`host elasticsearch`, `port 9200`, `logstash_format true`, `logstash_prefix fluentd`, `include_tag_key true`, `<buffer> flush_interval 1s`) plus a `stdout` store.

Start with `docker compose up --detach`, generate a request with curl to port 8080, then create a Kibana data view with pattern `fluentd-*`. Note the page says Elasticsearch and Kibana are under non-open-source licences since v7.11.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/container-deployment/docker-compose and confirmed: compose services, logging options, Dockerfile gem versions, fluent.conf parameters, licence note. Removed or reworded: nothing.

Method: documentation only; no commands were run.
