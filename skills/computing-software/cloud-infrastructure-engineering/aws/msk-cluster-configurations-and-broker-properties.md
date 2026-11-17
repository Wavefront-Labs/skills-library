---
id: computing-software.cloud-infrastructure-engineering.aws.msk-cluster-configurations-and-broker-properties
name: msk-cluster-configurations-and-broker-properties
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, kafka, msk-configuration, broker-properties, server-properties, min-insync-replicas]
level: practitioner
status: docs-checked
description: "Manage MSK cluster configurations: create revisions of server.properties, safe defaults for replication and retention, applying with rolling restarts, and topic-level overrides."
sources: ["https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-default-configuration.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-operations.html", "https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSK cluster configurations and broker properties

## Create and apply
```bash
cat > server.properties <<'EOF'
auto.create.topics.enable=false
default.replication.factor=3
min.insync.replicas=2
num.partitions=6
unclean.leader.election.enable=false
log.retention.hours=168
EOF
aws kafka create-configuration --name prod-kafka --kafka-versions 3.9.x \
  --server-properties fileb://server.properties
aws kafka update-cluster-configuration --cluster-arn "$C" --current-version "$(aws kafka describe-cluster \
  --cluster-arn "$C" --query ClusterInfo.CurrentVersion --output text)" \
  --configuration-info Arn=$CFG_ARN,Revision=1
```
- Configurations are versioned by **revision**; `aws kafka update-configuration --arn ... --server-properties ...`
  adds a new revision.
- Static properties need a broker restart to take effect, dynamic ones do not. With RF 3 and
  `min.insync.replicas=2` producers using `acks=all` should stay available during a rolling restart.
- Watch `aws kafka describe-cluster-operation --cluster-operation-arn ...` until `UPDATE_COMPLETE`.

## Defaults worth changing
| Property | MSK default (non-tiered cluster) | Production choice |
|---|---|---|
| `auto.create.topics.enable` | false | keep false; create topics explicitly |
| `default.replication.factor` | 3 for 3-AZ clusters, 2 for 2-AZ clusters | 3 |
| `min.insync.replicas` | 2 for 3-AZ clusters, 1 for 2-AZ clusters | 2 with RF 3 |
| `unclean.leader.election.enable` | **true** (false on tiered-storage clusters) | set false explicitly |
| `allow.everyone.if.no.acl.found` | true | false once ACLs are defined (define ACLs first or you lose access) |
| `num.partitions` | 1 | sized per topic anyway |

`log.retention.hours` is not in the MSK default table, so the Apache Kafka default for your
version applies; set it (or topic-level `retention.ms`) deliberately.
Properties you do not set take the default-configuration values above, or the Apache Kafka
defaults for your version. A custom configuration can set only the properties on the MSK custom
configuration page.

## Topic-level overrides (no restart)
```bash
kafka-configs.sh --bootstrap-server "$BS" --command-config client.properties \
  --alter --entity-type topics --entity-name orders --add-config retention.ms=1209600000
```
Dynamic broker properties take effect without a restart; static ones need one (see the MSK
broker configuration operations page).

## Gotchas
- A configuration is tied to Kafka versions; after upgrading Kafka, create a revision compatible with the new version.
- Express brokers use their own configuration model (read/write, read-only and non-editable
  properties), and tiered-storage clusters have different defaults.
- If you raise `message.max.bytes` and have consumers older than 0.10.2, raise their fetch size too.
- Store server.properties in git and deploy via IaC (`AWS::MSK::Configuration`).

## Verify
- [ ] `describe-cluster` shows the intended configuration ARN and revision.
- [ ] `kafka-configs.sh --describe --entity-type brokers --entity-name 1 --all` reflects values.
- [ ] Rolling update completed with no `UnderReplicatedPartitions` left > 0.

## Checked

2026-10-27, AWS documentation (current release as read on that date). MSK Developer Guide default configuration, custom configuration, configuration operations and Express broker configuration pages, supported versions table, botocore kafka 2018-11-14 model, CloudFormation AWS::MSK::Configuration page. Fixed: the MSK default for unclean.leader.election.enable is true on non-tiered clusters (the skill said false) and min.insync.replicas defaults to 2 for 3-AZ but 1 for 2-AZ clusters; the example Kafka version 3.6.0 is past end of support so the example uses 3.9.x; the claim that applying always restarts brokers was replaced by the static versus dynamic distinction. Confirmed: auto.create.topics.enable false, default.replication.factor 3 or 2, num.partitions 1, allow.everyone.if.no.acl.found default true, update-configuration and update-cluster-configuration parameters. Removed the log.retention.hours default, the unsourced replica.fetch.max.bytes requirement and the Serverless remark.
Method: documentation only; no commands were run.
