---
id: computing-software.messaging-and-integration.apache-kafka.kafka-authorizer-standard-authorizer
name: kafka-authorizer-standard-authorizer
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, acl, standard-authorizer, authorizer-class-name, allow-everyone-if-no-acl-found]
level: practitioner
status: docs-checked
description: "Enable StandardAuthorizer on all KRaft nodes, understand default deny, super.users and allow.everyone.if.no.acl.found."
sources:
  - https://kafka.apache.org/42/security/authorization-and-acls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on ACL-based authorization.

Config on every broker, controller or combined node:
`authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer`
ACLs are stored in the KRaft metadata log. Format: Principal P is Allowed or Denied Operation O from Host H on any Resource R matching ResourcePattern RP (KIP-11, KIP-290).

Defaults: a resource with no matching ACL is restricted to super users. To open such resources to everyone set `allow.everyone.if.no.acl.found=true`; resources that do have ACLs are still enforced as written.

Super users: `super.users=User:Bob;User:Alice`. The delimiter is a semicolon because SSL user names may contain commas, and the principal type `User` is case sensitive.

KRaft forwarding: CreateTopics and DeleteTopics go to a broker listener, which forwards them to the active controller via the first listener in `controller.listener.names`. Authorization happens on the controller using an Envelope request carrying the client principal. Custom `principal.builder.class` implementations therefore must implement `org.apache.kafka.common.security.auth.KafkaPrincipalSerde`.

Failure codes you will see: TOPIC_AUTHORIZATION_FAILED (29), GROUP_AUTHORIZATION_FAILED (30), CLUSTER_AUTHORIZATION_FAILED (31), TRANSACTIONAL_ID_AUTHORIZATION_FAILED (53).

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Authorization and ACLs page. Removed: nothing.

Method: documentation only; no commands were run.
