---
id: computing-software.messaging-and-integration.apache-kafka.kafka-acls-cli-recipes
name: kafka-acls-cli-recipes
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kafka-acls-sh, producer-acl, consumer-acl, resource-pattern-type]
level: practitioner
status: docs-checked
description: "Add, list and remove ACLs with kafka-acls.sh, using --producer, --consumer, prefixed patterns and deny rules."
sources:
  - https://kafka.apache.org/42/security/authorization-and-acls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage ACLs from the CLI.

Allow reads and writes from specific IPs:
`bin/kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:Bob --allow-principal User:Alice --allow-host 198.51.100.0 --allow-host 198.51.100.1 --operation Read --operation Write --topic Test-topic`

The host options take an IP address. Without an allow ACL, access is denied by default. Deny rules exist for the rare allow-all-except case: allow `User:'*'` from host `'*'` and `--deny-principal User:BadBob --deny-host 198.51.100.3`.

Role shortcuts:
- `--producer` grants WRITE, DESCRIBE and CREATE on the topic (add `--idempotent` with it; idempotence is automatic if the producer is authorized for a transactional id).
- `--consumer` grants READ, DESCRIBE on the topic and READ on the group, so `--group Group-1` is required.

Resource patterns: `--resource-pattern-type` defaults to `literal`. Use `prefixed` to cover names starting with a prefix: `--producer --topic Test- --resource-pattern-type prefixed`. Wildcard: `--topic '*'`.

List: `--list --topic Test-topic` shows only ACLs on that exact pattern. Use `--resource-pattern-type match` to include wildcard and prefixed ACLs that affect the topic. When removing, `match` should be used with care. Remove with `--remove` and the same flags as the add.

Operations: Read, Write, Create, Delete, Alter, Describe, ClusterAction, DescribeConfigs, AlterConfigs, IdempotentWrite, CreateTokens, DescribeTokens, All.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Authorization and ACLs page. Removed: the claim that hosts accept IP addresses only and not hostnames (the page only says the option takes an IP address).

Method: documentation only; no commands were run.
