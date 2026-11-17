---
id: computing-software.messaging-and-integration.strimzi.access-operator
name: access-operator
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [access-operator, kafkaaccess, service-binding-secret]
level: advanced
status: docs-checked
description: "Share Kafka connection details across namespaces with the Access Operator."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Access Operator and KafkaAccess

**Goal:** give applications in other namespaces connection details and credentials.

The Strimzi Access Operator is optional and deployed separately. It distributes Kafka connection information and credentials, stored as a `Secret`, which applications in different namespaces can reference. A `KafkaAccess` resource configures the connection information; when you create, modify or delete it, the operator updates a service binding secret holding the details in multiple formats.

Requirements and defaults:

- It cannot be used with a Kafka cluster that is not managed by the Cluster Operator.
- Installation files come from the release archive (`strimzi-1.3.0.*`) on GitHub; files are in `./install`.
- The Cluster Operator must be deployed first.
- By default it is deployed in the `strimzi-access-operator` namespace; to use another namespace, update the namespace in the install files.

```bash
kubectl create -f ./install/access-operator
kubectl get deployments
```

**Checklist**

1. Deploy the Cluster Operator and Kafka first.
2. Adjust namespaces in the install files if needed.
3. Reference the generated secret from consuming applications.

## Checked

2026-11-03. Confirmed in Using the Access Operator: optional and separate, release archive ./install files, Cluster Operator required, default strimzi-access-operator namespace, unsupported with unmanaged clusters. Corrected the install command to kubectl create -f ./install/access-operator as documented.

Method: documentation only; no commands were run.
