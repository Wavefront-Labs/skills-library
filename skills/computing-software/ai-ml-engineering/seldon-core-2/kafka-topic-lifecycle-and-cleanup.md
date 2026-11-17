---
id: computing-software.ai-ml-engineering.seldon-core-2.kafka-topic-lifecycle-and-cleanup
name: kafka-topic-lifecycle-and-cleanup
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, kafka-topics, cleantopicsondelete, topic-cleanup, topic-naming, kafka-busybox, errors-topic]
level: practitioner
status: docs-checked
description: "Seldon Core 2 creates input and output Kafka topics per model and pipeline; set dataflow.cleanTopicsOnDelete to remove them on delete, and list topics with a temporary kafka pod."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/managing-kafka-topics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kafka topic lifecycle and cleanup

If Kafka is installed, Seldon creates dedicated input and output topics for each Model as it is loaded, and for each Pipeline when deployed. They enable asynchronous messaging: send inputs and read outputs later.

## Names
```
seldon.seldon-mesh.model.iris.inputs
seldon.seldon-mesh.model.iris.outputs
seldon.seldon-mesh.pipeline.iris-pipeline.inputs
seldon.seldon-mesh.pipeline.iris-pipeline.outputs
seldon.seldon-mesh.errors.errors
```

## Retention versus cleanup
By default topics are kept when a model or pipeline is unloaded (useful for auditing, but it costs Kafka resources). Set `dataflow.cleanTopicsOnDelete: true` in the Model or Pipeline spec to remove the input and output topics on delete:

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: iris
spec:
  dataflow:
    cleanTopicsOnDelete: true
  storageUri: "gs://seldon-models/scv2/samples/mlserver_1.5.0/iris-sklearn"
  requirements:
    - sklearn
  memory: 100Ki
```

Topics of models inside a pipeline are not deleted unless those models are unloaded and have `cleanTopicsOnDelete` set to true.

## Listing topics
Run a temporary Pod with image `apache/kafka:latest` and `command: ["sleep", "3600"]`, then inside it run:

```bash
./kafka-topics.sh --list --bootstrap-server $SELDON_KAFKA_BOOTSTRAP_PORT_9092_TCP
```

Apply and delete manifests with `kubectl apply -f model.yaml -n seldon-mesh` and `kubectl delete -f model.yaml -n seldon-mesh`, then list again to verify.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/managing-kafka-topics.md (read in full).
