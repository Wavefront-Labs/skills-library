---
id: computing-software.database-administration.elasticsearch.running-elasticsearch-in-docker
name: running-elasticsearch-in-docker
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-docker, docker-compose, elasticsearch-setup, containers]
level: practitioner
status: docs-checked
description: "Run Elasticsearch in Docker for dev or small production: official image, single-node vs multi-node compose, memory limits, vm.max_map_count, volumes and security bootstrap."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Elasticsearch in Docker

## Single node (development)
```bash
docker network create elastic
docker run -d --name es01 --net elastic -p 9200:9200 -m 1GB \
  -v esdata01:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:<version>
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
curl --cacert http_ca.crt -u elastic https://localhost:9200
```
Elasticsearch generates TLS certs and the `elastic` password on first start (shown in the container output, so run without `-d` the first time or read `docker logs`), along with an enrollment token for Kibana (valid 30 minutes). The `-m` flag sets the container memory limit, and Elasticsearch sizes its heap from it, so no manual JVM sizing is needed; ML features such as ELSER need a larger container (the docs use 6GB). On Docker Desktop allocate at least 4GB.

## Host prerequisites
```bash
sudo sysctl -w vm.max_map_count=1048576     # persist in /etc/sysctl.conf
```
On Docker Desktop set it in the VM; with the WSL 2 backend set it in the `docker-desktop` WSL instance (`wsl -d docker-desktop -u root`). The setting must be `1048576` for Docker production use.

## Multi-node compose essentials
- Each node: unique `node.name`, same `cluster.name`, `discovery.seed_hosts=es01,es02,es03`, `cluster.initial_master_nodes=es01,es02,es03` (first bootstrap only; remove afterwards).
- Docker's `--ulimit nofile=65535:65535` (and `memlock=-1:-1` with `bootstrap.memory_lock=true`) for production.
- Heap is sized automatically from the container memory limit; to override in production bind mount a file under `/usr/share/elasticsearch/config/jvm.options.d`. `ES_JAVA_OPTS` overrides all other JVM options and is not recommended in production.

## Volumes
The container runs Elasticsearch as user `elasticsearch` with uid:gid `1000:0`; bind-mounted directories and files must be accessible to it and the data and log directories writable. Always bind a volume to `/usr/share/elasticsearch/data`. Back up with snapshots, not by copying a live volume.

## Production cautions
- Use an explicit version tag (the docs use `<SPECIFIC.VERSION.NUMBER>`).
- One node per host for real HA; several ES containers on one VM share its failure.
- For orchestration at scale prefer ECK on Kubernetes.

## Verify
`curl --cacert http_ca.crt -u elastic https://localhost:9200/_cluster/health?pretty` shows expected `number_of_nodes` and `green`/`yellow` (single-node with replicas configured stays yellow).

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x docs). Confirmed: image name, `docker network create elastic`, `-m` memory limit and automatic heap sizing, `elasticsearch-reset-password`, `docker cp ... http_ca.crt` path, 30-minute enrollment tokens, vm.max_map_count 1048576 and the WSL 2 note, uid:gid 1000:0, `--ulimit nofile=65535:65535`, `memlock`, `ES_JAVA_OPTS` caveat, bind data volume. Removed the stale pinned 8.15.3 tag, the `discovery.type=single-node` flag, the 2x-heap rule, the certutil setup-container advice and the "never latest" claim (not in the docs). The compose-file node settings (`discovery.seed_hosts`, `cluster.initial_master_nodes`) follow the discovery skill; the exact compose file was not re-read.

Method: documentation only; no commands were run.
