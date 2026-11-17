---
id: computing-software.messaging-and-integration.strimzi.storage-types
name: storage-types
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafka-storage, jbod, persistent-storage, ephemeral-storage]
level: advanced
status: docs-checked
description: "Choose ephemeral, persistent or JBOD storage for node pools."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kafka storage types

**Goal:** select a storage type that cannot be regretted later.

Basic types:

- **Ephemeral:** lasts only while the pod runs. Recommended only for development and testing.
- **Persistent:** survives pod restarts; suited to production.
- **JBOD:** multiple disks or volumes, each either ephemeral or persistent.
- **Tiered storage (advanced):** offloads older data to remote storage such as object storage; configured at cluster level and enabled per topic with `remote.storage.enable`.

Persistent, ephemeral and JBOD **cannot be changed after the cluster is deployed**. You can add or remove volumes within JBOD, or create and migrate to node pools with new storage. The docs recommend JBOD even for one volume, so you can add volumes later.

Storage is configured in `KafkaNodePool.spec.storage`:

```yaml
storage:
  type: jbod
  volumes:
    - id: 0
      type: persistent-claim
      size: 100Gi
      deleteClaim: false
```

**Checklist**

1. Use persistent or JBOD for real data.
2. Prefer JBOD so volumes can be added later.
3. Plan a node pool migration if you need a different base type.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Configuring Kafka storage, storage types section).
