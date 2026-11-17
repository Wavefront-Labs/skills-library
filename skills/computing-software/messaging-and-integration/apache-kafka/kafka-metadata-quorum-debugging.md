---
id: computing-software.messaging-and-integration.apache-kafka.kafka-metadata-quorum-debugging
name: kafka-metadata-quorum-debugging
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, kafka-dump-log-sh, kafka-metadata-shell-sh, describe-status]
level: practitioner
status: docs-checked
description: "Inspect KRaft metadata state with kafka-metadata-quorum.sh describe, kafka-dump-log.sh and kafka-metadata-shell.sh."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: debug the cluster metadata partition.

Quorum summary:
`bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status`
It prints ClusterId, LeaderId, LeaderEpoch, HighWatermark, MaxFollowerLag, MaxFollowerLagTimeMs, CurrentVoters and CurrentObservers. Use `describe --replication` to watch followers catch up.

Decode metadata log segments or snapshots:
```
bin/kafka-dump-log.sh --cluster-metadata-decoder --files metadata_log_dir/__cluster_metadata-0/00000000000000000000.log
bin/kafka-dump-log.sh --cluster-metadata-decoder --files metadata_log_dir/__cluster_metadata-0/00000000000000000100-0000000001.checkpoint
```

Browse a snapshot interactively:
`bin/kafka-metadata-shell.sh --snapshot metadata_log_dir/__cluster_metadata-0/00000000000000007228-0000000001.checkpoint`
Inside the shell, `ls /` shows brokers, local, metadataQuorum, topicIds and topics; `cat /topics/foo/0/data` prints a partition's leader, ISR and epochs; `exit` leaves.

Failure mode: the snapshot `00000000000000000000-0000000000.checkpoint` contains no cluster metadata, so do not examine it with kafka-metadata-shell.sh; use a valid later snapshot.

Replace `metadata_log_dir` with the directory set by `metadata.log.dir` on your node.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 KRaft operations page (Debugging). Removed: closing paragraph interpreting CurrentVoters and MaxFollowerLag.

Method: documentation only; no commands were run.
