---
id: computing-software.data-engineering.apache-kafka.kafka-acls
name: kafka-acls
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, kafka-acls, authorizer, standardauthorizer, prefixed-acls, super-users, allow-everyone-if-no-acl-found, least-privilege, kafka-authorization]
level: advanced
status: docs-checked
description: "Authorize Kafka with ACLs: StandardAuthorizer, least-privilege ACL sets for producers, consumers, Streams and Connect, prefixed patterns, super.users and auditing denials."
sources:
  - https://kafka.apache.org/documentation/#security_authz
  - https://kafka.apache.org/documentation/#security_authz_cli
  - https://github.com/apache/kafka/blob/trunk/docs/security/security-model.md
  - https://github.com/apache/kafka/blob/trunk/docs/streams/developer-guide/security.md
  - https://github.com/apache/kafka/blob/trunk/docs/security/security-model-connect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka ACLs

**Goal:** each service can do exactly what it needs on exactly its topics and groups.

## Enable
```properties
authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer   # KRaft: set on brokers and controllers
super.users=User:admin;User:broker              # brokers/controllers' own principals
allow.everyone.if.no.acl.found=false            # default false: deny when no ACL matches
```
Turning on an authorizer with no ACLs locks out every non-super user: create ACLs first (or start with `allow.everyone.if.no.acl.found=true` during migration and audit denials).

## Standard ACL sets
```bash
K="kafka-acls.sh --bootstrap-server $B --command-config admin.properties"
# Producer (idempotent producers also need IdempotentWrite on the cluster: add --idempotent)
$K --add --allow-principal User:checkout-svc --producer --idempotent --topic orders.checkout.order-placed.v1
# Consumer
$K --add --allow-principal User:billing-svc --consumer --topic orders.checkout.order-placed.v1 --group billing-projector
# Transactional producer also needs
$K --add --allow-principal User:enricher --operation Write --operation Describe --transactional-id enricher- --resource-pattern-type prefixed
# Prefixed: a team owns a namespace
$K --add --allow-principal User:payments-team --operation All --topic payments. --resource-pattern-type prefixed
$K --list --topic orders.checkout.order-placed.v1
```
`--producer` = Write, Describe, Create on topic; `--consumer` = Read, Describe on topic + Read on group.

## Kafka Streams app
Needs Read on input topics and Write on output topics. The principal must also be allowed to create, read and write the internal topics (named `<application.id>-<operatorName>-<suffix>`, a convention the Streams docs say is not guaranteed for future releases), so grant on the prefixed `<application.id>` rather than naming them; plus a transactional-id ACL if exactly-once is on. Check the Streams security page for the exact operations.

## Kafka Connect
The worker authenticates as one principal, so ACLs cannot distinguish connectors: grant that principal Read/Write on the `config.storage.topic`, `offset.storage.topic` and `status.storage.topic` and the worker group, plus access to the topics its connectors use (partition by topic prefix). A sink connector consumes with group `connect-<connector-name>`. Per-connector credentials via `producer.override.sasl.jaas.config` / `consumer.override.sasl.jaas.config` work under `connector.client.config.override.policy=All` (the default); use `Allowlist` or `None` unless only trusted users can reach the REST API, because overriding JAAS settings is a code-execution vector.

## Deny rules
`--deny-principal` with `--deny-host` carves an exception out of a broader allow (for example allow `User:*` to read a topic but deny `User:BadBob` from one IP). `--allow-host` and `--deny-host` take IP addresses only, not hostnames. Use sparingly.

## Audit
Authorizer decisions go to the `kafka.authorizer.logger` log4j logger: `INFO` records denied requests, `DEBUG` also records allowed requests (very noisy). There is no built-in tamper-evident audit trail, so ship the log off-broker and alert on spikes of denials.

## Verify
- [ ] Each service principal can only touch its listed topics/groups (try reading another team's topic: `TopicAuthorizationException`).
- [ ] ACL definitions are kept in version control and applied from there, with no manual drift.
- [ ] `allow.everyone.if.no.acl.found=false` in production.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: StandardAuthorizer class name and KRaft placement, `allow.everyone.if.no.acl.found` default false, `--producer` (Write, Describe, Create on topic), `--consumer` (Read, Describe on topic plus Read on group), `--idempotent` and the IdempotentWrite cluster operation (the earlier claim that Write alone suffices was wrong), `--allow-host`/`--deny-host` IP-only, `kafka.authorizer.logger` INFO/DEBUG behaviour, Streams internal-topic naming and ACL requirement, Connect `connector.client.config.override.policy` default `All` (WorkerConfig source) and the single-principal model. Sink consumer group naming `connect-<connector-name>` confirmed in the SinkUtils source. Removed: the unsourced Streams "All on prefixed" ACL, the ZooKeeper authorizer note and the Terraform and Strimzi names.

Method: documentation only; no commands were run.
