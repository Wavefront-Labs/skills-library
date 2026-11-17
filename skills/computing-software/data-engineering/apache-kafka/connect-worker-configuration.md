---
id: computing-software.data-engineering.apache-kafka.connect-worker-configuration
name: connect-worker-configuration
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, connect-worker-config, plugin-path, internal-topics, distributed-mode, connect-rest-api]
level: practitioner
status: docs-checked
description: "Configure Kafka Connect distributed workers: group.id, config/offset/status topics, plugin.path isolation, converters, REST listener, and producer/consumer overrides."
sources:
  - https://kafka.apache.org/documentation/#connectconfigs
  - https://kafka.apache.org/documentation/#connect_running
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/user-guide.md
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedConfig.java
  - https://github.com/apache/kafka/blob/trunk/docs/security/security-model-connect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Connect worker configuration

`connect-distributed.properties` (same file on every worker of one Connect cluster):
```properties
bootstrap.servers=b1:9092,b2:9092,b3:9092
group.id=connect-prod-a                       # unique per Connect cluster; workers sharing it form the cluster
config.storage.topic=connect-prod-a-configs   # always 1 partition, replicated, compacted
offset.storage.topic=connect-prod-a-offsets   # many partitions (offset.storage.partitions default 25), compacted
status.storage.topic=connect-prod-a-status    # can have several partitions (default 5), compacted
config.storage.replication.factor=3
offset.storage.replication.factor=3
status.storage.replication.factor=3
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
value.converter.schemas.enable=false
plugin.path=/opt/connect/plugins              # paths that contain Connect plugins (default null)
listeners=http://0.0.0.0:8083
rest.advertised.host.name=${HOSTNAME}         # what other workers use to forward REST calls
connector.client.config.override.policy=All   # allow per-connector producer./consumer.override.*
exactly.once.source.support=enabled           # exactly-once source connectors (3.3.0+); existing clusters go preparing first
```

## Rules
- **`group.id` names the Connect cluster and must not conflict with consumer group ids**; two Connect clusters should not share it or the internal topics, since sharing the offsets topic would mix source offsets.
- Create the internal topics yourself (compacted, replicated, `config` topic **1 partition**: the framework ignores a `config.storage.partitions` setting) so they are not auto-created with surprising settings. `config.storage.replication.factor` defaults to 3.
- `plugin.path` lists the paths that contain Connect plugins. `plugin.discovery` (3.6+) defaults to `hybrid_warn`; `service_load` is the fastest and only safe if all plugins are compatible: check the startup WARN logs, try `hybrid_fail` in a test environment, or use `connect-plugin-path.sh list` and `sync-manifests --dry-run` to inspect and migrate plugins.
- Worker-level converters are defaults; connectors can override (`value.converter` in the connector config).
- Producer/consumer settings for tasks: `producer.*` / `consumer.*` in the worker config (all connectors), or `producer.override.*` in a connector config (needs the override policy).
- Secrets: use `config.providers` rather than plain text.
- Security: on a secured cluster the client settings must be given up to three times in the worker config: for management access, for Kafka sources (`producer.` prefix) and for Kafka sinks (`consumer.` prefix).
- REST: any caller allowed onto the API can act on every connector and read its configuration, and a connector can read any data the worker can reach, so restrict network access and use HTTPS and extensions (`rest.extension.classes`) as the security model describes.
- `scheduled.rebalance.max.delay.ms` (default 300000 ms, five minutes): when a worker leaves, Connect waits this long before triggering a rebalance. `connect.protocol=eager` restores the old rebalance behaviour; incremental cooperative rebalancing has been the default since 2.3.0.

## Verify
- [ ] `GET /` returns the worker version, commit and `kafka_cluster_id`; `GET /connector-plugins` lists expected plugins (it only checks the worker that serves the request).
- [ ] Internal topics exist with `cleanup.policy=compact` and the expected replication factor.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: the three internal-topic settings and their roles, `offset.storage.partitions` default 25, status partitions default 5, `config.storage.replication.factor` default 3, config topic partitions always 1 (DistributedConfig source), `connector.client.config.override.policy` default `All`, `plugin.path`, `plugin.discovery` modes and `connect-plugin-path.sh`, `listeners` and `rest.advertised.host.name`, `exactly.once.source.support` (3.3.0), `scheduled.rebalance.max.delay.ms` default, `connect.protocol`, root endpoint contents, and the security model. Removed: the Confluent Avro converter lines, the unconfirmed "workers refuse a config topic with more than one partition", the named library clashes and the one-subdirectory-per-plugin rule.

Method: documentation only; no commands were run.
