---
id: computing-software.cloud-infrastructure-engineering.docker.elasticsearch-and-opensearch-containers
name: elasticsearch-and-opensearch-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, database-container, elasticsearch-container, vm-max-map-count, opensearch, memlock, jvm-heap]
level: advanced
status: docs-checked
description: "Run Elasticsearch or OpenSearch in Docker: host vm.max_map_count, heap sizing, memlock/nofile ulimits, single-node vs cluster discovery, security, data ownership."
sources: ["https://www.elastic.co/docs/deploy-manage/deploy/self-managed/vm-max-map-count", "https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elasticsearch and OpenSearch containers

## Host prerequisite: vm.max_map_count
```bash
sudo sysctl -w vm.max_map_count=1048576   # Elasticsearch; OpenSearch docs use 262144
```
Elastic's current docs: if the OS default is already 1048576 or higher, change nothing;
otherwise set 1048576, and persist it in `/etc/sysctl.conf`. The OpenSearch Docker guide sets
`vm.max_map_count=262144` (also in the Docker Desktop WSL distribution).

## Single node for dev/test (Elasticsearch 8.x)
```yaml
services:
  es:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.3
    environment:
      discovery.type: single-node
      ELASTIC_PASSWORD: ${ELASTIC_PASSWORD:?}
      xpack.security.http.ssl.enabled: "false"     # dev only
      ES_JAVA_OPTS: "-Xms2g -Xmx2g"
      bootstrap.memory_lock: "true"
    ulimits:
      memlock: { soft: -1, hard: -1 }
      nofile: { soft: 65536, hard: 65536 }
    mem_limit: 4g
    volumes: [esdata:/usr/share/elasticsearch/data]
    ports: ["127.0.0.1:9200:9200"]
    healthcheck:
      test: ["CMD-SHELL", "curl -fs -u elastic:$$ELASTIC_PASSWORD http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s"]
      interval: 10s
      retries: 30
volumes: { esdata: {} }
```
- Size the heap with `ES_JAVA_OPTS` and keep `mem_limit` comfortably above it.

## OpenSearch
```yaml
  os:
    image: opensearchproject/opensearch:2.17.1
    environment:
      discovery.type: single-node
      OPENSEARCH_INITIAL_ADMIN_PASSWORD: ${OS_ADMIN_PASSWORD:?}   # required since 2.12
      OPENSEARCH_JAVA_OPTS: "-Xms2g -Xmx2g"
```
The OpenSearch guide sets `memlock` unlimited and `nofile` 65536 (at least) in compose, and
from 2.12 a custom admin password is required (`OPENSEARCH_INITIAL_ADMIN_PASSWORD`).

## Multi-node on one host or Swarm
Set `node.name`, `cluster.name`, `discovery.seed_hosts=es01,es02,es03` and
`cluster.initial_master_nodes` (first bootstrap only, remove afterwards).

## Gotchas
- Swap kills performance; `memory_lock` prevents heap swapping but needs unlimited memlock.
- Do not publish 9200 on all interfaces without auth.

## Checked
2026-10-31. Confirmed: Elastic Install Elasticsearch > Increase virtual memory page (1048576 threshold, persist in `/etc/sysctl.conf`); OpenSearch Docker guide (262144, WSL distribution, 2.12 admin password, memlock -1, nofile 65536). Corrected the old 262144 figure for Elasticsearch. Removed (Elastic Docker pages read were index stubs): heap percentages and 31 GB, default-security and UID 1000 notes, disk watermark percentages, the bootstrap-check message, `--sysctl` remark.
Method: documentation only; no commands were run.
