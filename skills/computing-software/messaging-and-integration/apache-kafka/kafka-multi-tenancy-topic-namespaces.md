---
id: computing-software.messaging-and-integration.apache-kafka.kafka-multi-tenancy-topic-namespaces
name: kafka-multi-tenancy-topic-namespaces
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, multi-tenancy, prefixed-acls, create-topic-policy, auto-create-topics-enable]
level: practitioner
status: docs-checked
description: "Isolate tenants with hierarchical topic names, prefixed ACLs, CreateTopicPolicy, quotas and per-tenant monitoring."
sources:
  - https://kafka.apache.org/42/operations/multi-tenancy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a shared Kafka cluster without noisy neighbours.

Namespaces: topics cannot be renamed (you must create a new topic, copy, delete the old one), so adopt a hierarchical naming scheme up front, for example `<organization>.<team>.<dataset>.<event-name>` or `<project>.<product>.<event-name>`. Avoid putting changeable data (such as the consumer's name) or metadata available elsewhere (partition count) in names.

Enforce naming with: prefix ACLs (KIP-290), a custom CreateTopicPolicy via `create.topic.policy.class.name` (KIP-108), or denying topic creation by ACL and creating topics by automation. Also consider `auto.create.topics.enable=false`, but do not rely on it alone.

Grant a tenant a prefix:
`bin/kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:Alice --producer --resource-pattern-type prefixed --topic acme.infosec.`

Isolation: use client quotas; request-rate quotas often matter more than bandwidth quotas because excess CPU on request handling reduces effective bandwidth. Quotas can also cover topic operations (create, delete, alter). Server quotas cover the connection acceptance rate, maximum connections per broker, and per IP address.

Retention: set `retention.bytes` and `retention.ms` per topic. Monitoring: for example the JMX metric `kafka.log.Log.Size.<TOPIC-NAME>` to alert on tenant storage.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Multi-Tenancy page. Removed: nothing.

Method: documentation only; no commands were run.
