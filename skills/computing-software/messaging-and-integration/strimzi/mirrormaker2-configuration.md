---
id: computing-software.messaging-and-integration.strimzi.mirrormaker2-configuration
name: mirrormaker2-configuration
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [mirrormaker2-config, mirror-aliases, offset-sync]
level: advanced
status: docs-checked
description: "Configure MirrorMaker 2 beyond the minimal resource."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MirrorMaker 2 configuration

**Goal:** build a production-grade `KafkaMirrorMaker2` resource.

Start with the minimal configuration. A minimal resource needs `.spec.target` (connection details for the target cluster, with a unique alias), `.spec.mirrors` (the replication flow), `.spec.mirrors[].source` (source cluster details, also with a unique alias) and `.spec.replicas` (Kafka Connect worker pods). MirrorMaker 2 runs on the Kafka Connect framework, so its configuration and status are stored in Kafka topics on the target cluster.

By default MirrorMaker 2 replicates all topics and consumer groups. Use `topicsPattern` and `groupsPattern` (regexes) to limit what is replicated and synchronised.

Extend it for:

- securing connections (TLS and authentication),
- managing replicated topic names,
- synchronising consumer group offsets,
- synchronising ACL rules,
- tuning Kafka Connect worker settings,
- common settings: resource requests and limits (recommended), JVM tuning, metrics,
- logging.

Settings such as security and resource allocation are optional but recommended for production.

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaMirrorMaker2
metadata:
  name: my-mirror-maker2
spec:
  replicas: 3
  target:
    alias: my-cluster-target
    bootstrapServers: my-cluster-target-kafka-bootstrap:9092
    groupId: my-mirror-maker2-group
    configStorageTopic: my-mirror-maker2-config
    offsetStorageTopic: my-mirror-maker2-offset
    statusStorageTopic: my-mirror-maker2-status
  mirrors:
    - source:
        alias: my-cluster-source
        bootstrapServers: my-cluster-source-kafka-bootstrap:9092
      sourceConnector: {}
      topicsPattern: "topic1.*|topic2.*"
      groupsPattern: "group1.*|group2-[0-9]{2}"
```

For a Strimzi-managed cluster the bootstrap address can be the bootstrap service name, `<cluster_name>-kafka-bootstrap:<port>`. The Kafka clusters need not be managed by Strimzi or run on Kubernetes.

Each cluster can use its own authentication type, set in `spec.target.authentication` and `spec.mirrors[].source.authentication`: `tls`, `scram-sha-256`, `scram-sha-512`, `plain` or `custom`. Securing connections needs separate `KafkaUser` credentials for the source and target clusters, and the security options must be compatible with those on the clusters.

**Checklist**

1. Unique alias per cluster.
2. Add TLS and authentication per cluster.
3. Set resources and metrics before production.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (single page; MirrorMaker 2 sections 11.9.1 and 11.9.2 and the deployment section on authentication types read); minimal example replaced by the documented one, port 9093 example dropped.
