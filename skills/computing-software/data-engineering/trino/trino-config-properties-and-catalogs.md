---
id: computing-software.data-engineering.trino.trino-config-properties-and-catalogs
name: trino-config-properties-and-catalogs
category: computing-software
field: data-engineering
product: trino
tags: [config-properties, coordinator, discovery-uri, catalog-properties, node-scheduler-include-coordinator]
level: practitioner
status: docs-checked
description: "Minimal Trino coordinator and worker config.properties, what coordinator, discovery.uri and include-coordinator mean, and how catalog files mount connectors."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/installation/deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino config properties and catalogs

Every Trino server can act as coordinator and worker, but a cluster needs exactly one coordinator, and dedicating a machine to coordination performs best on larger clusters.

Coordinator `etc/config.properties`:

```text
coordinator=true
node-scheduler.include-coordinator=false
http-server.http.port=8080
discovery.uri=http://example.net:8080
```

Worker: `coordinator=false`, the same port and `discovery.uri`, no include-coordinator line. Single-machine test: `coordinator=true` with `node-scheduler.include-coordinator=true`.

- `coordinator`: accept client queries and manage execution.
- `node-scheduler.include-coordinator`: allow work on the coordinator; on larger clusters it competes with scheduling and monitoring.
- `http-server.http.port`: Trino uses HTTP for all internal and external traffic.
- `discovery.uri`: the coordinator's built-in discovery service, sharing the HTTP server port. Every node registers and heartbeats to it. If HTTP is disabled on the coordinator, the scheme must be `https`.

This is a minimal set; resource groups, fault-tolerant execution, logging, tracing, JMX and metrics are optional extras.

Catalogs: a connector reaches a data source through a catalog, which provides its schemas and tables. The Hive connector maps each Hive database to a schema, so table `clicks` in database `web` in catalog `example` is `example.web.clicks`. Register catalogs with files in `etc/catalog`; `etc/catalog/jmx.properties` containing `connector.name=jmx` mounts the JMX connector as catalog `jmx`.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
