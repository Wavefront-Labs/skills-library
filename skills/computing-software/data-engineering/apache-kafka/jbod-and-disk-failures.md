---
id: computing-software.data-engineering.apache-kafka.jbod-and-disk-failures
name: jbod-and-disk-failures
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, jbod, log-dirs, disk-failure, kafka-operations, kraft, replica-movement]
level: advanced
status: docs-checked
description: "Run Kafka with JBOD (multiple log.dirs): placement, handling a failed disk, moving replicas between disks with kafka-reassign-partitions, and KRaft JBOD support."
sources:
  - https://kafka.apache.org/documentation/#brokerconfigs_log.dirs
  - https://kafka.apache.org/documentation/#basicops
  - https://github.com/apache/kafka/blob/trunk/storage/src/main/java/org/apache/kafka/storage/internals/log/LogManager.java
  - https://github.com/apache/kafka/blob/trunk/server-common/src/main/java/org/apache/kafka/server/config/ServerLogConfigs.java
  - https://github.com/apache/kafka/blob/trunk/docs/operations/hardware-and-os.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JBOD log directories and disk failure handling

```properties
log.dirs=/data1/kafka,/data2/kafka,/data3/kafka,/data4/kafka
```
Each partition replica lives in exactly one dir. The log manager creates new logs in the data directory with the fewest logs and makes no attempt to move partitions afterwards or balance by size or I/O rate, so dirs can fill unevenly when partition sizes differ.

## Disk failure behaviour
- KRaft: the 3.9 documentation lists JBOD with multiple storage directories as not fully implemented, with an Early Access release in 3.7 (KIP-858) that is not recommended for production; the current documentation no longer lists it as missing, so check the release notes of your version.
- If a broker cannot tell the controller that a log directory failed for longer than `log.dir.failure.timeout.ms` (default 30000 ms), the broker fails and shuts down.

Detect: broker metric `kafka.log:type=LogManager,name=OfflineLogDirectoryCount` (should be 0), and `kafka-log-dirs.sh --describe --bootstrap-server $BS --broker-list 3` (options: `--describe`, `--topic-list`, `--broker-list`).

## Replace a failed disk
1. To retire a directory on purpose, cordon it: `kafka-configs.sh --bootstrap-server $BS --alter --add-config cordoned.log.dirs=/data4/kafka --entity-type brokers --entity-name <id>`, reassign its partitions to other directories or brokers (the tool cannot generate this plan), shut the broker down, uncordon with `--bootstrap-controller ... --alter --delete-config cordoned.log.dirs`, remove the path from `log.dirs` and restart.
2. After replacing hardware, confirm re-replication through the `UnderReplicatedPartitions` metric returning to 0, and throttle the copy if needed (`leader.replication.throttled.rate` and `follower.replication.throttled.rate` via `kafka-configs.sh`).

## Move replicas between disks on one broker
```json
{"version":1,"partitions":[{"topic":"orders","partition":3,"replicas":[1,2,3],"log_dirs":["/data4/kafka","any","any"]}]}
```
```bash
kafka-reassign-partitions.sh --bootstrap-server $BS --reassignment-json-file move.json --execute \
  --replica-alter-log-dirs-throttle 50000000
kafka-reassign-partitions.sh --bootstrap-server $BS --reassignment-json-file move.json --verify
```
`log_dirs` entries align with `replicas`; `any` means no particular directory. The throttle for moves between disks is `replica.alter.log.dirs.io.max.bytes.per.second`, set by `--replica-alter-log-dirs-throttle`.

## JBOD vs RAID
The Kafka hardware guidance says RAID costs write throughput and available disk space; its benefit is tolerating disk failures, but rebuilding a RAID array is so I/O intensive that it can effectively disable the server, so it gives little real availability gain. Follow the hardware and OS section when choosing.

## Verify
- [ ] `OfflineLogDirectoryCount` alert wired.
- [ ] `kafka-log-dirs.sh --describe` shows reasonably even sizes across dirs on each broker (placement is by log count, not size).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: new logs go to the directory with the fewest logs and are not rebalanced (LogManager source), `log.dir.failure.timeout.ms` default and behaviour (ServerLogConfigs source), `OfflineLogDirectoryCount` metric, `kafka-log-dirs.sh` options, the `log_dirs` and `any` plan syntax and `--replica-alter-log-dirs-throttle`, the cordoned.log.dirs decommissioning procedure, KRaft JBOD Early Access status in 3.7 (3.9 kraft.md), and the RAID guidance. Removed: the KIP-112 offline-directory behaviour, the `KafkaStorageException` output claim, the `metadata.log.dir` default, replacement-disk restart details, the `.future` directory claim, Cruise Control, and the JBOD-versus-RAID10 capacity comparison and 20% figure.

Method: documentation only; no commands were run.
