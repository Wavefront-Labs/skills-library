---
id: computing-software.ai-ml-engineering.kserve.kserve-kafka-event-pipeline
name: kserve-kafka-event-pipeline
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [kafka, kafkasource, knative-eventing, minio, bootstrapservers, consumergroup, inferenceservice-addressable-resolver, event-driven]
level: advanced
status: docs-checked
description: "Event-driven inference: Minio bucket notifications to Kafka, a Knative KafkaSource sinking to an InferenceService with a transformer, plus the addressable-resolver ClusterRole."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/kafka/kafka.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kafka event-driven inference pipeline

Flow: image uploaded to Minio bucket `mnist` -> Minio notification to Kafka topic `mnist` -> Knative `KafkaSource` -> InferenceService transformer (preprocess downloads the image and builds tensors; postprocess writes it into bucket `digits`) -> TensorFlow predictor.

Setup:
- Kafka and Zookeeper via Bitnami Helm charts (kafka chart 21.0.0, zookeeper 11.0.0) or an existing cluster.
- Knative Eventing core >= 1.2 and the Kafka event source (`source.yaml`).
- RBAC so the source can resolve InferenceServices:

```yaml
kind: ClusterRole
metadata:
  name: inferenceservice-addressable-resolver
  labels: {duck.knative.dev/addressable: "true"}
rules:
  - apiGroups: [serving.kserve.io]
    resources: [inferenceservices, inferenceservices/status]
    verbs: [get, watch]
```
- Minio: `mc admin config set myminio notify_kafka:1 ...`, `mc event add myminio/mnist arn:minio:sqs::1:kafka -p --event put --suffix .png`, plus an S3 Secret attached to the service account.

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: mnist}
spec:
  predictor: {minReplicas: 1, model: {modelFormat: {name: tensorflow}, storageUri: 's3://mnist'}}
  transformer:
    minReplicas: 1
    containers: [{name: kserve-container, image: '${USERNAME}/mnist-transformer:latest'}]
---
apiVersion: sources.knative.dev/v1beta1
kind: KafkaSource
metadata: {name: kafka-source}
spec:
  consumerGroup: knative-group
  bootstrapServers: [kafka-headless.default.svc.cluster.local:9092]
  topics: [mnist]
  sink:
    ref: {apiVersion: serving.kserve.io/v1beta1, kind: InferenceService, name: mnist}
    uri: /v1/models/mnist:predict
```

## Checked
Confirmed against KServe's Kafka event pipeline page: Bitnami chart versions, Knative Eventing core 1.2 or later, Kafka source install, the `inferenceservice-addressable-resolver` ClusterRole, Minio bucket notification commands, the InferenceService with transformer and the `KafkaSource` sink.
Method: docs-only read of cited pages, 2026-11-08
