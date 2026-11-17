---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-cassandra-schema-init
name: jaeger-cassandra-schema-init
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, cassandra, schema-create, trace-ttl, jaeger-cassandra-schema]
level: practitioner
status: docs-checked
description: "Let Jaeger create the Cassandra keyspace on startup (defaults shown) or initialize it manually with create.sh or the schema image."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/cassandra/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: prepare Cassandra 4.x or 5.x for Jaeger.

Since v2.1.0 Jaeger can create the schema on start-up. Defaults are equivalent to:
```
extensions:
  jaeger_storage:
    backends:
      some_storage:
        cassandra:
          schema:
            create: true
            keyspace: jaeger_dc1
            datacenter: dc1
            trace_ttl: 48h
            dependencies_ttl: 48d
            compaction_window: 2h
            replication_factor: 1
```
Customize them, for example for longer retention or higher replication.

If `schema.create` is false, initialize manually with the repository script via cqlsh:
`MODE=test sh ./internal/storage/v1/cassandra/schema/create.sh | cqlsh`
or the container image (provide the right IP):
```
docker run -e CQLSH_HOST={server IP address} -e MODE=prod jaegertracing/jaeger-cassandra-schema:2.22.0
```
For production pass `MODE=prod DATACENTER={datacenter}`, where the datacenter is the name used in the Cassandra configuration or network topology. The script also overrides TTL, keyspace name and replication factor; run it without arguments for the full parameter list.

A sample backend config is config-cassandra.yaml in the repository.

The supported Cassandra versions are 4.x and 5.x. For deploying the cluster itself, the Jaeger docs point to the Apache Cassandra documentation, and they list a Docker container, a Bitnami Helm chart and a DataStax Kubernetes operator as community resources.

## Checked

2026-11-03. Confirmed against the Cassandra page: supported versions 4.x and 5.x, automatic schema creation since v2.1.0 with the listed defaults, create.sh and the schema image commands, MODE=prod and DATACENTER, the sample config and the community resources. Nothing removed.
Method: documentation only; no commands were run.
