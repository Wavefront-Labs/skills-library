---
id: computing-software.data-engineering.apache-kafka.strimzi-kafka-on-kubernetes
name: strimzi-kafka-on-kubernetes
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-operations, strimzi-kafka-operator, kubernetes, kafkanodepool, kafkatopic, kafkauser, kraft, operator]
level: advanced
status: docs-checked
description: "Run Kafka on Kubernetes with the Strimzi operator: Kafka and KafkaNodePool CRs in KRaft mode, listeners, storage, topic/user operators, upgrades and rolling restarts."
sources:
  - https://strimzi.io/docs/operators/latest/deploying
  - https://strimzi.io/docs/operators/latest/configuring
  - https://github.com/strimzi/strimzi-kafka-operator/tree/main/packaging/examples
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Strimzi: Kafka on Kubernetes

**Goal:** declarative Kafka clusters on k8s where the operator handles rolling restarts, certificates, and topic/user management.

## Install
```bash
helm install strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator
```
This is the Helm install shown in the Strimzi deployment docs; the docs also cover YAML-file installs and
setting chart values such as `--set replicas=2` and `--version`.

## Cluster (KRaft, node pools)
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata: {name: controllers, namespace: kafka, labels: {strimzi.io/cluster: prod}}
spec:
  replicas: 3
  roles: [controller]
  storage: {type: jbod, volumes: [{id: 0, type: persistent-claim, size: 20Gi, kraftMetadata: shared}]}
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata: {name: brokers, namespace: kafka, labels: {strimzi.io/cluster: prod}}
spec:
  replicas: 3
  roles: [broker]
  storage: {type: jbod, volumes: [{id: 0, type: persistent-claim, size: 1Ti, class: gp3, deleteClaim: false}]}
  resources: {requests: {cpu: "4", memory: 16Gi}, limits: {memory: 16Gi}}
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: prod
  namespace: kafka
spec:
  kafka:
    version: <Kafka version supported by your Strimzi release>
    listeners:
      - {name: tls, port: 9093, type: internal, tls: true, authentication: {type: tls}}
      - {name: external, port: 9094, type: loadbalancer, tls: true, authentication: {type: scram-sha-512}}
    authorization: {type: simple}
    rack: {topologyKey: topology.kubernetes.io/zone}
    config:
      default.replication.factor: 3
      min.insync.replicas: 2
      offsets.topic.replication.factor: 3
  entityOperator: {topicOperator: {}, userOperator: {}}
  cruiseControl: {}
```
Field names and API versions change between Strimzi releases: the current docs use `apiVersion: kafka.strimzi.io/v1` and ZooKeeper-based clusters must be migrated before upgrading to 0.46 or later. The `v1beta2` and node-pool annotations above are for older releases; check the docs for your version.

## Topics and users as CRs
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata: {name: orders, namespace: kafka, labels: {strimzi.io/cluster: prod}}
spec: {partitions: 24, replicas: 3, config: {retention.ms: 604800000, min.insync.replicas: 2}}
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata: {name: billing-app, namespace: kafka, labels: {strimzi.io/cluster: prod}}
spec:
  authentication: {type: tls}
  authorization:
    type: simple
    acls:
      - {resource: {type: topic, name: orders}, operations: [Read, Describe]}
      - {resource: {type: group, name: billing}, operations: [Read]}
```
The User Operator creates a Secret `billing-app` with the client cert/key.

## Day-2
- Rolling restart: annotate the pod with `strimzi.io/manual-rolling-update="true"` using `kubectl annotate pod <pod-name>` (the docs show this for a Kafka pod; find the pod name with `kubectl get pods`).
- Upgrade: bump operator first, then `spec.kafka.version`; operator rolls brokers one by one, waiting for partitions to be in sync.
- Scale brokers: change `KafkaNodePool.spec.replicas`; then rebalance with a `KafkaRebalance` CR (`mode: add-brokers`). Before scaling down, `mode: remove-brokers`.
- Status: `kubectl get kafka prod -o jsonpath='{.status.conditions}'`.

## Gotchas
- Set memory limit = request and size the JVM heap via `jvmOptions` (`-Xms/-Xmx`) well below it: Kafka relies on the OS page cache, which counts against the pod's memory cgroup.
- `deleteClaim: false` to keep the persistent volume claims if the node pool is deleted.
- Treat `KafkaTopic` resources as the source of truth for topics the Topic Operator manages; do not change them with kafka-topics.sh. Check the docs for your release for how the Topic Operator handles such drift.

## Verify
- [ ] `Kafka` status `Ready=True`; all pods in different zones.
- [ ] A KafkaUser's credentials can produce/consume only allowed topics.

## Checked

- Date: 2026-11-02.
- Confirmed against: Strimzi deploying and configuring guides (Helm OCI install from quay.io/strimzi-helm, KafkaNodePool with strimzi.io/cluster label, roles, jbod storage with kraftMetadata and deleteClaim, listener types and scram-sha-512, rack topologyKey, cruiseControl, entity operator, KafkaRebalance modes add-brokers and remove-brokers, strimzi.io/manual-rolling-update annotation, jvmOptions -Xms/-Xmx, the v1 API note).
- Removed: the pinned Kafka version 3.9.0 (the guides now show 4.x versions) and the unconfirmed 0.41 default/revert claim.

Method: documentation only; no commands were run.
