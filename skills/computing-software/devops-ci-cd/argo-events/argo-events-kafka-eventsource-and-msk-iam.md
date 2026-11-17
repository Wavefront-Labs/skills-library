---
id: computing-software.devops-ci-cd.argo-events.argo-events-kafka-eventsource-and-msk-iam
name: argo-events-kafka-eventsource-and-msk-iam
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, kafka-eventsource, amazon-msk, iam, irsa, awsmskiamauth, consumergroup]
level: advanced
status: docs-checked
description: "Consume Kafka topics with the Kafka EventSource, including Amazon MSK IAM authentication through IRSA with the minimum IAM policy."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/kafka.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events kafka eventsource and msk iam

The Kafka EventSource listens on topics. The CloudEvent `data` has `topic`, `partition`, `body` and `timestamp`. Create the EventSource (`examples/event-sources/kafka.yaml`, update fields), the sensor `examples/sensors/kafka.yaml`, publish a message with a Kafka client and look for the workflow with `argo list`.

Amazon MSK with IAM access control: use `awsMskIamAuth` instead of `sasl` or `tls` (TLS is enabled automatically). It uses the AWS SDK v2 default credential chain, so IRSA on EKS is simplest, but EC2 instance profiles and static `AWS_*` env credentials also work.

```yaml
spec:
  kafka:
    msk-source:
      url: b-1.my-cluster.abc123.c2.kafka.us-east-1.amazonaws.com:9098  # 9098 for IAM
      topic: my-topic
      consumerGroup:
        groupName: my-consumer-group
      awsMskIamAuth:
        region: us-east-1
```

Annotate the service account (`argo-events-sa`) with `eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/<role-name>`.

The role's policy needs at minimum: `kafka-cluster:Connect` on the cluster ARN; `kafka-cluster:DescribeTopic` and `kafka-cluster:ReadData` on the topic ARN; `kafka-cluster:AlterGroup` on the consumer-group ARN. Use port 9098 and not 9092 for IAM authentication.

## Checked

2026-11-04. Confirmed against the Kafka EventSource page: the `data` fields, setup steps, `awsMskIamAuth` instead of `sasl` or `tls` with TLS automatic, the AWS SDK v2 default credential chain (IRSA, EC2 instance profiles, static `AWS_*` variables), the EventSource and ServiceAccount YAML, the IAM actions and resources, and port 9098. Nothing removed.
Method: documentation only; no commands were run.
