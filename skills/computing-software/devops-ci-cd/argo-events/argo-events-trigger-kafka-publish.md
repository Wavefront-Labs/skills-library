---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-kafka-publish
name: argo-events-trigger-kafka-publish
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, kafka-trigger, topic, partition, payload, minio]
level: practitioner
status: docs-checked
description: "Publish events from a Sensor onto a Kafka topic with the kafka trigger, composing the message body from event fields."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/kafka-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger kafka publish

The Kafka trigger lets a Sensor publish events onto a Kafka topic, sourcing events from the outside world into your messaging queues. Example scenario: a file dropped on a Minio bucket becomes a Kafka message.

```yaml
triggers:
  - template:
      name: kafka-trigger
      kafka:
        url: kafka.argo-events.svc:9092
        topic: minio-events
        partition: 0
        payload:
          - src:
              dependencyName: test-dep
              dataKey: notification.0.s3.object.key
            dest: fileName
          - src:
              dependencyName: test-dep
              dataKey: notification.0.s3.bucket.name
            dest: bucket
```

The message needs a body, so `payload` lists `src` (a dependency plus a `dataKey`) and `dest` (the destination key in the resulting message body). The above produces `{"fileName": "hello.txt", "bucket": "input"}` when `hello.txt` is dropped on the `input` bucket. Set up the Minio EventSource first, but do not create the Minio sensor from that page; create this Kafka sensor instead. In the example `url` is the Kafka URL, `topic` the topic name and `partition` the partition id. The full field list is in the KafkaTrigger API spec.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/kafka-trigger.md. Confirmed: url, topic, partition, payload src/dest, generated message body. Removed or changed: contextKey for Kafka payload, the description of url as an in-cluster broker address and partition semantics beyond 'partition id', and the duplicated EventSource paragraph. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
