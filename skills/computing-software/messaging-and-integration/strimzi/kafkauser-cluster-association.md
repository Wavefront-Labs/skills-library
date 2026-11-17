---
id: computing-software.messaging-and-integration.strimzi.kafkauser-cluster-association
name: kafkauser-cluster-association
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafkauser-label, strimzi-cluster-label, user-secret]
level: practitioner
status: docs-checked
description: "Tie a KafkaUser to its cluster and find its generated secret."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Associating users with clusters

**Goal:** make sure the User Operator creates the user and its credentials.

A `KafkaUser` carries the label `strimzi.io/cluster` with the name of the `Kafka` resource:

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaUser
metadata:
  name: my-user
  labels:
    strimzi.io/cluster: my-cluster
```

If the label does not match, the User Operator cannot identify the resource and the user is not created. If the status of the `KafkaUser` stays empty, check this label.

Clients are represented as users. `KafkaUser` configures authentication, authorization and access rights; authentication permits access, authorization constrains actions. Mechanisms must match the specification of the listener the client uses.

The User Operator stores credentials in a **user secret** that holds a private key and certificate (for mTLS) or the SCRAM password; see the generated secrets skill for names.

```bash
kubectl get kafkauser my-user -o yaml
kubectl get secret my-user -o yaml
```

**Checklist**

1. Check `strimzi.io/cluster` matches `metadata.name` of the Kafka.
2. Check `status` has conditions.
3. Mount the user secret in client pods.

## Checked

2026-11-03. Confirmed in Managing Kafka users: the strimzi.io/cluster label requirement and the behaviour when it does not match.

Method: documentation only; no commands were run.
