---
id: computing-software.search-and-information-retrieval.apache-solr.docker-solr
name: docker-solr
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [docker, solr-precreate, container, docker-compose, solr-demo]
level: intro
status: docs-checked
description: "Run Solr in Docker: docker run with a /var/solr volume, solr-precreate and solr-demo commands, SolrCloud networking with SOLR_HOST_ADVERTISE, and creating collections."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker-solr

Basic run, persisting data under `/var/solr` in a host directory:
`docker run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 --name my_solr solr solr-precreate gettingstarted`
The Admin UI is at port 8983 of the Docker host.

Entry commands:
- `solr-precreate <name>`: prepares the core, then runs Solr.
- `solr-demo`: starts Solr with demo data, for trying out.
- Plain `docker run -d -p 8983:8983 --name my_solr solr` starts Solr with no core.

Persistence: mount a volume or directory on `/var/solr`. Solr expects some files there; pre-populate your own directory or let the image copy them.

Docker Compose files use the same port map and volumes; named volumes work as well as host directories.

For a cluster, run each container on a shared network, set `SOLR_HOST_ADVERTISE` to a name other containers resolve, and create collections through the API, for example `curl 'http://localhost:8983/solr/admin/collections?action=CREATE&name=gettingstarted4&numShards=1&collection.configName=_default'`, or `docker run ... solr solr create -c gettingstarted3 -p 8983`.

## Checked

Checked 2026-11-09 against the full Solr in Docker page of the Solr Reference Guide: host-mounted run, Compose, solr-demo, /var/solr persistence, solr-precreate, collection creation options and SOLR_HOST_ADVERTISE usage.

Method: docs-checked 2026-11-09 against the Solr in Docker page (raw ref-guide source); no commands were run.
