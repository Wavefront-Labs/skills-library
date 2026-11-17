---
id: computing-software.messaging-and-integration.strimzi.private-registry-images
name: private-registry-images
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [container-registry, mirror-images, quay-io]
level: practitioner
status: docs-checked
description: "Mirror Strimzi images into your own registry and update the install YAML."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using your own container registry

**Goal:** run Strimzi without pulling from the public registry.

Strimzi images are published to the Container Registry (quay.io), and the installation YAML pulls them directly. If you cannot reach it, or want your own repository:

1. Pull all container images listed in the docs.
2. Push them into your own registry.
3. Update the image names in the YAML files used in deployment.

Each Kafka version supported by the release has a separate image, for example:

```text
quay.io/strimzi/kafka:1.3.0-kafka-4.3.1
quay.io/strimzi/operator:1.3.0
```

The Kafka image runs the broker, Kafka Connect, MirrorMaker 2 and Cruise Control. The operator image runs the Cluster Operator, Topic Operator, User Operator and Kafka Initializer. HTTP Bridge has its own image.

The Cluster Operator maps Kafka versions to images through per-component variables such as `STRIMZI_KAFKA_IMAGES` and `STRIMZI_KAFKA_CONNECT_IMAGES`, as whitespace or comma-separated `<version> = <image>` pairs, for example `4.3.1=quay.io/strimzi/kafka:1.3.0-kafka-4.3.1`. An `image` property in a component's resource overrides these defaults.

**Checklist**

1. Mirror every image for every Kafka version you run.
2. Update the operator Deployment and the `STRIMZI_KAFKA_IMAGES` style mappings.
3. Use `spec.image` only for deliberate overrides.

## Checked

2026-11-03. Confirmed in the Container images section: quay.io registry, the pull/push/update steps, per-Kafka-version images (kafka:1.3.0-kafka-4.3.1, operator:1.3.0), which components each image runs, the version=image pair format, and that a component image property overrides the defaults. Reworded the generic STRIMZI_<COMPONENT_NAME>_IMAGES placeholder to the documented STRIMZI_KAFKA_IMAGES and STRIMZI_KAFKA_CONNECT_IMAGES names.

Method: documentation only; no commands were run.
