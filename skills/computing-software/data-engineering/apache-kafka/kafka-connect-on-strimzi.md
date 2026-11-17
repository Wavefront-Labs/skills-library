---
id: computing-software.data-engineering.apache-kafka.kafka-connect-on-strimzi
name: kafka-connect-on-strimzi
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, strimzi-kafka-connect, strimzi, kubernetes, kafkaconnector, gitops]
level: practitioner
status: docs-checked
description: "Run Kafka Connect on Kubernetes with Strimzi: KafkaConnect resources, building plugin images, declarative KafkaConnector resources, secrets, and scaling."
sources:
  - https://strimzi.io/docs/operators/latest/deploying
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Connect on Kubernetes with Strimzi

## KafkaConnect cluster with a built image
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: cdc
  annotations:
    strimzi.io/use-connector-resources: "true"     # manage connectors via KafkaConnector CRs, not REST
spec:
  version: <KAFKA_VERSION>
  replicas: 3
  bootstrapServers: prod-kafka-bootstrap:9093
  tls: {trustedCertificates: [{secretName: prod-cluster-ca-cert, certificate: ca.crt}]}
  authentication: {type: tls, certificateAndKey: {secretName: cdc-user, certificate: user.crt, key: user.key}}
  config:
    group.id: cdc-connect
    config.storage.topic: cdc-connect-configs
    offset.storage.topic: cdc-connect-offsets
    status.storage.topic: cdc-connect-status
    config.providers: secrets
    config.providers.secrets.class: io.strimzi.kafka.KubernetesSecretConfigProvider
  build:
    output: {type: docker, image: registry.example.com/kafka/cdc-connect:1.0, pushSecret: regcred}
    plugins:
      - name: debezium-postgres
        artifacts:
          - type: tgz
            url: <URL_OF_CONNECTOR_PLUGIN_ARCHIVE>
            sha512sum: <sha512>
  resources: {requests: {cpu: "1", memory: 4Gi}, limits: {memory: 4Gi}}
  jvmOptions: {"-Xmx": "3g"}
```
- With `build`, Strimzi downloads the plugins into a new container image, pushes it to the registry in `.spec.build.output` and uses it in the deployment. A new image is built when `.spec.image` or `.spec.build.plugins` changes. `sha512sum` is the artifact checksum.
- Alternatively build your own image from the Kafka Connect base image with plugins in `/opt/kafka/plugins/` and set `KafkaConnect.spec.image` (per cluster; the `STRIMZI_KAFKA_CONNECT_IMAGES` variable on the Cluster Operator applies globally).

## KafkaConnector (declarative)
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: orders-cdc
  labels: {strimzi.io/cluster: cdc}
spec:
  class: <CONNECTOR_CLASS>
  tasksMax: 1
  state: stopped            # optional; set to stop a connector
  config:
    # connector-specific keys; see the connector's own docs
    some.password: ${secrets:<NAMESPACE>/<SECRET>:password}   # config provider reference
```
- With the annotation enabled, manage connectors through KafkaConnector resources: manual changes made directly through the Kafka Connect REST API are reverted by the Cluster Operator. To use the REST API instead, remove the annotation.
- To restart a connector or task manually, annotate the KafkaConnector resource with `strimzi.io/restart` (see the Strimzi deployment guide for the exact annotation forms).
- `spec.autoRestart.enabled` restarts failed connectors and tasks; by default restarts are attempted indefinitely and `maxRestarts` limits them.
- `spec.tasksMax` is the maximum number of tasks the connector can create.

## Checked
2026-11-01. Confirmed in the Strimzi deployment guide (Kafka Connect build, custom image, KafkaConnector, autoRestart sections): the use-connector-resources annotation and its REST-revert note, build.output and plugins fields, pushSecret, sha512sum, rebuild triggers, /opt/kafka/plugins, spec.image, tasksMax, autoRestart. Removed: pinned Kafka and Debezium versions and the Maven URL (now placeholders), Kaniko and OpenShift Builds detail, restart-task, running/paused state values, Role/RoleBinding detail for the secret provider, status jsonpath, the 0.33 version note and the kubectl verify commands, none of which could be confirmed.
Method: documentation only; no commands were run.
