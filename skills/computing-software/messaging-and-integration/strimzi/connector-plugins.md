---
id: computing-software.messaging-and-integration.strimzi.connector-plugins
name: connector-plugins
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [connector-plugins, source-connector, sink-connector]
level: practitioner
status: docs-checked
description: "Add connector plugins to Kafka Connect and choose how to manage connector instances."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connector plugins in Kafka Connect

**Goal:** get connector classes into your Connect cluster.

A connector is an instance of a connector class. A **source** connector fetches data from an external system and feeds it to Kafka as messages. A **sink** connector reads messages from Kafka topics and feeds them to an external system. Plugins carry the implementation artifacts and can include converters and transforms. A Connect deployment can hold several plugins but only one version of each.

Ways to add plugins:

1. Configure Kafka Connect to **build a new container image** with plugins automatically.
2. **Mount plugins as Kubernetes Image volumes.**
3. Create a Docker image from the base Kafka Connect image, manually or through CI.

Once plugins are in the image, manage connector instances in either of two ways:

- Strimzi's `KafkaConnector` custom resource, or
- the Kafka Connect REST API.

You can create new connectors with either option. With the annotation `strimzi.io/use-connector-resources: "true"` on `KafkaConnect`, connectors must be managed through `KafkaConnector` resources; to use the REST API, remove the annotation.

```bash
kubectl get kafkaconnector -n my-namespace
kubectl get kafkaconnect my-connect -o yaml
```

**Checklist**

1. Choose build, image volume or custom image.
2. Keep one version per plugin.
3. Pick KafkaConnector resources or the REST API, not both.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Adding Kafka Connect connectors; Managing Kafka Connect connector instances).
