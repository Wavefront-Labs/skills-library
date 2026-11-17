---
id: computing-software.messaging-and-integration.strimzi.deploy-mirrormaker2
name: deploy-mirrormaker2
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [mirrormaker2, kafkamirrormaker2, cluster-mirroring]
level: practitioner
status: docs-checked
description: "Deploy MirrorMaker 2 to replicate data between Kafka clusters."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying MirrorMaker 2

**Goal:** mirror topics between a source and a target Kafka cluster.

MirrorMaker 2 consumes messages from a source cluster and republishes them to a target cluster. This supports recovery after failure, consolidation of several clusters, restricting data access to one cluster, and placing data close to consumers. It is based on Kafka Connect and uses its configuration properties.

Example file: `examples/mirror-maker/kafka-mirror-maker-2.yaml`. Edit these fields:

- `spec.target.bootstrapServers` and `spec.mirrors[].source.bootstrapServers`
- `spec.target.alias` and `spec.mirrors[].source.alias`: a unique identifier per cluster
- `spec.target.authentication` and `spec.mirrors[].source.authentication`: `tls`, `scram-sha-256`, `scram-sha-512`, `plain` or `custom`

```bash
kubectl apply -f examples/mirror-maker/kafka-mirror-maker-2.yaml
```

As with Connect, deploy multiple MirrorMaker 2 clusters in separate namespaces. A minimal `KafkaMirrorMaker2` needs `.spec.target` (connection details with a unique alias) and the mirrors list. Optional settings cover TLS, replicated topic naming, consumer group offset sync, ACL sync and Connect worker tuning.

**Checklist**

1. Give every cluster a unique alias.
2. Match authentication types to each cluster's listeners.
3. One MirrorMaker 2 cluster per namespace.

## Checked

2026-11-03. Confirmed in the MirrorMaker 2 deployment section: example file path, target/source bootstrapServers, alias and authentication types, and the one-cluster-per-namespace warning.

Method: documentation only; no commands were run.
