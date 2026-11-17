---
id: computing-software.data-engineering.apache-kafka.topic-naming-and-config-as-code
name: topic-naming-and-config-as-code
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, topic-naming, topic-config-management, kafka-configs, kafka-topics, terraform-kafka, julie-ops, auto-create-topics, topic-governance]
level: practitioner
status: docs-checked
description: "Govern Kafka topics: a naming convention, disabling auto-create, managing topic configs as code (Terraform/GitOps), and altering/describing configs safely with kafka-configs."
sources:
  - https://kafka.apache.org/39/configuration/topic-level-configs/
  - https://kafka.apache.org/39/operations/basic-kafka-operations/
  - https://github.com/Mongey/terraform-provider-kafka/blob/master/docs/resources/topic.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topic naming and configuration as code

**Goal:** every topic has a predictable name, an owner, and its config in version control, so the cluster can be rebuilt and audited.

## Naming convention (pick one, enforce it)
`<domain>.<dataset>.<event-or-entity>.<version>` with optional visibility prefix:
- `orders.checkout.order-placed.v1` (event stream)
- `crm.customer.state.v2` (compacted entity state)
- `private.payments.fraud-scores.v1` (team-internal)
Rules: lowercase, dots/hyphens only (don't mix `.` and `_`), version suffix bumps only on breaking change (new topic, migrate consumers), no environment in the name if clusters are per-environment.

## Disable auto-create
`auto.create.topics.enable=false` on brokers. Otherwise a typo in a producer creates a topic with the broker defaults and data goes nowhere useful.

## Inspect and change configs
```bash
kafka-topics.sh --bootstrap-server $B --describe --topic orders.checkout.order-placed.v1
kafka-configs.sh --bootstrap-server $B --entity-type topics --entity-name orders.checkout.order-placed.v1 --describe --all
kafka-configs.sh --bootstrap-server $B --entity-type topics --entity-name orders.checkout.order-placed.v1 \
  --alter --add-config retention.ms=1209600000,max.message.bytes=2097152
kafka-configs.sh ... --alter --delete-config retention.ms        # revert to broker default
kafka-topics.sh --bootstrap-server $B --alter --topic X --partitions 24   # increase only
```
Partition count can only grow (Kafka does not support reducing it), and adding partitions does not repartition existing data, which can disturb consumers that rely on key placement.

## Config as code (Terraform)
```hcl
resource "kafka_topic" "order_placed" {
  name               = "orders.checkout.order-placed.v1"
  partitions         = 12
  replication_factor = 3
  config = {
    "cleanup.policy"      = "delete"
    "retention.ms"        = "604800000"
    "min.insync.replicas" = "2"
  }
}
```
Confluent Cloud: the Confluent Terraform provider's `confluent_kafka_topic`; MSK: same OSS provider via IAM/SASL; Strimzi on Kubernetes: `KafkaTopic` custom resources reconciled by the Topic Operator. Pair with ACLs in the same repo.

## Ownership metadata
Kafka has no topic description field: keep owner, schema subject, retention rationale and consumers in the IaC repo or a catalog (DataHub, Confluent Stream Catalog tags).

## Gotchas
- Before changing `replication_factor` in Terraform, read the provider's `kafka_topic` page; the Kafka docs change replication factor with a partition reassignment plan.
- Deleting a topic requires `delete.topic.enable=true` (default true) and is asynchronous; recreating the same name immediately can race.

## Checked
2026-10-28. Confirmed: kafka-configs `--add-config`/`--delete-config` and `--partitions` usage, partitions cannot be reduced and adding them does not repartition existing data (Kafka 3.9 basic operations page); `delete.topic.enable` default true and `auto.create.topics.enable` (Strimzi deployment docs); `kafka_topic` resource with `partitions`, `replication_factor`, `config` (Mongey provider docs); `confluent_kafka_topic` (Confluent provider docs). Removed: metric-name collision claim, default-partition claim, restart-free config claim, destroy-on-replication-change claim. The naming convention is an opinion, not a documented rule.
Method: documentation only; no commands were run.

## Verify
- [ ] `terraform plan` shows no drift against the live cluster.
- [ ] Producing to a non-existent topic fails (auto-create off).
- [ ] All topic names match the convention regex in a CI check.
