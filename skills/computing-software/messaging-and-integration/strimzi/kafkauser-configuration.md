---
id: computing-software.messaging-and-integration.strimzi.kafkauser-configuration
name: kafkauser-configuration
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafkauser, user-operator, acl-rules]
level: practitioner
status: docs-checked
description: "Create Kafka users with the User Operator, including authentication and ACLs."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring KafkaUser

**Goal:** declare a client identity with its authentication and authorization.

The User Operator reflects `KafkaUser` changes in Kafka. Use `kubectl apply` to create or modify and `kubectl delete KafkaUser <name>` to remove.

Prerequisites: a Kafka listener using mTLS authentication with TLS encryption, and a running User Operator (typically deployed with the Entity Operator).

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaUser
metadata:
  name: my-user-1
  labels:
    strimzi.io/cluster: my-cluster
spec:
  authentication:
    type: tls
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: my-topic
          patternType: literal
        operations: [Describe, Read]
```

The mechanism must match the equivalent Kafka listener configuration. The label `strimzi.io/cluster` ties the user to a cluster; without a match the User Operator cannot identify the user and it is not created.

A user certificate's validity can be tuned with `validityDays` and `renewalDays`, which must be set together: `validityDays` greater than 0 and greater than `renewalDays`; `renewalDays` greater than 0 and less than `validityDays`.

**Checklist**

1. Label the user with the cluster name.
2. Match authentication type to the listener.
3. Set `validityDays` and `renewalDays` together.

## Checked

2026-11-03. Confirmed in Configuring Kafka users: kubectl apply/delete usage, prerequisites (mTLS listener with TLS, running User Operator), mechanism matching, and validityDays/renewalDays rules.

Method: documentation only; no commands were run.
