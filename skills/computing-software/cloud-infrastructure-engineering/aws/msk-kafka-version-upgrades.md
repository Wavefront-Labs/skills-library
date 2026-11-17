---
id: computing-software.cloud-infrastructure-engineering.aws.msk-kafka-version-upgrades
name: msk-kafka-version-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, kafka, kafka-version-upgrade, rolling-upgrade, kraft, get-compatible-kafka-versions]
level: practitioner
status: docs-checked
description: "Upgrade Apache Kafka on MSK safely: check compatible versions, client compatibility, RF and min ISR for availability, rolling upgrade monitoring, and ZooKeeper to KRaft migration."
sources: ["https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html", "https://docs.aws.amazon.com/msk/latest/developerguide/version-support.html", "https://docs.aws.amazon.com/msk/latest/developerguide/version-upgrades.html", "https://docs.aws.amazon.com/msk/latest/developerguide/version-upgrades-best-practices.html", "https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSK Kafka version upgrades

## Plan
```bash
aws kafka get-compatible-kafka-versions --cluster-arn "$C"
aws kafka describe-cluster --cluster-arn "$C" \
  --query 'ClusterInfo.[CurrentBrokerSoftwareInfo.KafkaVersion,CurrentVersion]'
```
- Upgrades are one-way; downgrades are not supported. Test in a staging cluster with production-like clients.
- Read the Kafka release notes between versions for removed configs and client protocol changes.
  Server-side upgrades do not update client applications; Kafka's client compatibility policy lets
  older clients talk to newer clusters and vice versa, and client upgrades are not tied to the cluster's EOL date.
- Check the MSK supported-versions table. A cluster still on a version after its end-of-support
  date is auto-upgraded to the recommended version at any time, with no notice. On the page as read,
  3.6.0 ended support on 2026-06-01 and 3.7.x on 2026-09-01; 3.9.x was the recommended version.

## Availability prerequisites
- Topic replication factor at least 3 for 3-AZ clusters and at least 2 for 2-AZ clusters (an RF of 2 can
  cause offline partitions during patching), and `min.insync.replicas` at most RF - 1, so one broker down keeps writes going.
- Clients configured with several broker addresses in the bootstrap string.
- Producers with `acks=all` and retries (the default in 3.x clients); consumers tolerant of rebalances.
```bash
kafka-topics.sh --describe --bootstrap-server "$BS" --command-config c.properties | grep -E 'ReplicationFactor: 1'
```

## Run
```bash
aws kafka update-cluster-kafka-version --cluster-arn "$C" \
  --current-version "$V" --target-kafka-version 3.9.x \
  --configuration-info Arn=$CFG_ARN,Revision=2     # a configuration valid for the target version
aws kafka list-cluster-operations --cluster-arn "$C" --max-results 1
```
- MSK performs an in-place rolling update and orchestrates broker restarts to keep the cluster
  available. `describe-cluster-operation` shows the steps (`INITIALIZE_UPDATE`,
  `UPDATE_APACHE_KAFKA_BINARIES`, `FINALIZE_UPDATE`).
- Watch `UnderReplicatedPartitions`, `OfflinePartitionsCount`, `ActiveControllerCount` (exactly 1),
  client error rates and consumer lag (`MaxOffsetLag`).

## ZooKeeper and KRaft
- New KRaft clusters use a `.kraft` version (for example `3.7.x.kraft` in the API; the console has a
  KRaft checkbox on 3.7.x or later).
- An existing ZooKeeper-based cluster can be migrated in place by choosing a KRaft-based target version
  (a `.kraft` suffix) in the upgrade (`UpdateClusterKafkaVersion`). Read the "Migrate from ZooKeeper to
  KRaft mode" page first; migrated clusters have no controller DNS endpoints.
- Kafka 3.9 is the last version to support both ZooKeeper and KRaft; Kafka 4.0 deprecates ZooKeeper.
  Kafka 4.2.x was available on Express brokers only when the page was read.

## Gotchas
- A custom configuration is tied to Kafka versions; the console offers an option to apply configuration
  updates compatible with the new version, and `--configuration-info` on the CLI does the same.

## Verify
- [ ] Staging upgrade done with production client versions, no errors.
- [ ] Post-upgrade `KafkaVersion` correct, `UnderReplicatedPartitions` = 0, lag recovered.

## Checked

2026-10-27, AWS documentation (current release as read on that date). MSK Developer Guide supported versions table, version support policy, upgrade procedure, upgrade best practices and metadata management pages; botocore kafka 2018-11-14 model. Fixed: an in-place ZooKeeper to KRaft migration is now supported by choosing a .kraft target version (the skill said it was not); the example target version 3.6.0 and 3.7.x are past end of support (2026-06-01 and 2026-09-01), so the example uses 3.9.x, the recommended version; Kafka 4.x does not simply drop ZooKeeper (3.9 is the last version supporting both, 4.0 deprecates it); RF minimums are 3 for 3-AZ and 2 for 2-AZ clusters. Confirmed: downgrades unsupported, auto-upgrade after end of support, minISR at most RF-1, get-compatible-kafka-versions and update-cluster-kafka-version parameters. Removed unsourced claims on CPU headroom, upgrade duration, concurrent operations and bootstrap strings.
Method: documentation only; no commands were run.
