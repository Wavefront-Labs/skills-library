---
id: computing-software.ai-ml-engineering.seldon-core-2.kafka-self-hosted-strimzi-install-and-auth
name: kafka-self-hosted-strimzi-install-and-auth
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, kafka, strimzi, strimzi-operator, kraft, kafka-security-protocol, sasl-scram, mtls, kafkauser, helm-values, brokervalidationsecret]
level: practitioner
status: docs-checked
description: "Self-hosted Kafka for Seldon Core 2 with Strimzi: install the operator and cluster, then set Helm values for mTLS or SASL/SCRAM."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/kafka.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/strimzi-mtls.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/strimzi-sasl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-hosted Kafka with Strimzi: install and authentication

Kafka is required for data-centric Pipelines. The docs recommend a managed Kafka for production; Strimzi is for trial, dev and testing.

## Install
The Strimzi operator must be in the same namespace as the Kafka cluster so Core can use the mTLS certificates Strimzi creates.
```bash
helm upgrade --install strimzi-kafka-operator strimzi/strimzi-kafka-operator --namespace seldon-mesh --create-namespace
helm upgrade seldon-core-v2-kafka kafka/strimzi -n seldon-mesh --install
```
The docs use KRaft rather than Zookeeper and warn that the Strimzi KRaft install is not production ready; KRaft needs Kafka 3.4 or above. Each Strimzi operator version supports a subset of Kafka versions. With Ansible: `ansible-playbook playbooks/setup-ecosystem.yaml -e full_install=no -e install_kafka=yes`.

## Security protocol
The Helm value `security.kafka.protocol` is `SSL` for mTLS and `SASL_SSL` for SASL/SCRAM, as in the two examples below.

## mTLS
Enable the broker listener in the Strimzi chart values: `broker.tls.enabled: true`, port 9093, `listenerType: internal`, `authentication.type: tls`. Create a `KafkaUser` named `seldon` with label `strimzi.io/cluster: seldon` and `authentication.type: tls` in seldon-mesh. Then install the setup chart with:
```yaml
kafka:
  bootstrap: seldon-kafka-bootstrap.seldon-mesh.svc.cluster.local:9093
security:
  kafka:
    protocol: SSL
    ssl:
      client:
        secret: seldon
        brokerValidationSecret: seldon-cluster-ca-cert
        keyPath: /tmp/certs/kafka/client/user.key
        crtPath: /tmp/certs/kafka/client/user.crt
        caPath: /tmp/certs/kafka/client/ca.crt
        brokerCaPath: /tmp/certs/kafka/broker/ca.crt
```

## SASL/SCRAM
Create the cluster with `broker.tls.authentication.type: scram-sha-512` (Ansible: `-e @../k8s/samples/ansible-strimzi-kafka-sasl-scram.yaml -e strimzi_kafka_operator_feature_gates=""`). That also creates user `seldon` with its password in a secret. Helm values:
```yaml
kafka:
  bootstrap: seldon-kafka-bootstrap.seldon-mesh.svc.cluster.local:9093
security:
  kafka:
    protocol: SASL_SSL
    sasl:
      mechanism: SCRAM-SHA-512
      client:
        username: seldon
        secret: seldon
        passwordPath: password
    ssl:
      client:
        brokerValidationSecret: seldon-cluster-ca-cert
        brokerCaPath: /tmp/certs/kafka/broker/ca.crt
```
Install with `helm install seldon-v2 k8s/helm-charts/seldon-core-v2-setup/ -n seldon-mesh -f <values file>`, then the SeldonRuntime chart.

## Checked
2026-11-09. Confirmed against docs-gb/kubernetes/kafka.md, strimzi-mtls.md and strimzi-sasl.md (Seldon Core v2 branch): Kafka required for data-centric Pipelines; managed Kafka recommended for production and Strimzi for trial, dev and testing; the operator in the same namespace as the cluster; both Helm commands; KRaft, the not-production-ready warning, Kafka 3.4 or above and the Strimzi/Kafka version subset; the Ansible command for Kafka only; the mTLS broker values, the `seldon` KafkaUser with label `strimzi.io/cluster: seldon`, the `seldon-cluster-ca-cert` secret and both Helm values blocks; the SASL/SCRAM Ansible override, user `seldon` with password in a secret, and values block; the `helm install seldon-v2` command and SeldonRuntime install. Removed: the `KAFKA_SECURITY_PROTOCOL` variable name and the `PLAINTEXT` option (not on these pages).
Method: documentation only; no commands were run.
