---
id: computing-software.ai-ml-engineering.seldon-core-2.kafka-managed-services-authentication
name: kafka-managed-services-authentication
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, kafka, managed-kafka, aws-msk, confluent-cloud, azure-event-hub, sasl-plain, sasl-oauthbearer, kafka-acls, replicationfactor, kafka-debug, min-insync-replicas]
level: advanced
status: docs-checked
description: "Connect Seldon Core 2 to managed Kafka: AWS MSK (mTLS, SASL/SCRAM), Confluent Cloud (SASL/PLAIN, OAUTHBEARER) and Azure Event Hub, with Helm values, secrets and troubleshooting."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/aws-msk-mtls.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/aws-msk-sasl.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/confluent-sasl.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/confluent-oauth.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/getting-started/kubernetes-installation/security/azure-event-hub-sasl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed Kafka authentication

Documented managed options: Confluent Cloud (SASL/PLAIN, SASL/OAUTHBEARER), Amazon MSK (mTLS, SASL/SCRAM) and Azure Event Hub (SASL/PLAIN). In all cases set `kafka.bootstrap` to the broker endpoints and tune `kafka.topics.replicationFactor` and `kafka.topics.numPartitions` to the cluster. For any problem, set `kafka.debug=all`.

## AWS MSK mTLS
Outside AWS, MSK needs a public endpoint. Using kafka-acls with the mTLS client config, grant the client certificate CommonName principal (`User:CN=myname`) all operations on topics, the cluster (so topics can be created on demand) and groups, each using the wildcard resource.

Create two secrets: `aws-msk-client` from files `tls.key`, `tls.crt` and `ca.crt` (private key exported from the JKS keystore), and `aws-msk-broker-ca` holding `ca.crt` extracted from the Amazon truststore (keytool to PKCS12, then openssl to PEM). Values: `security.kafka.protocol: SSL`, `ssl.client.secret: aws-msk-client`, `ssl.client.brokerValidationSecret: aws-msk-broker-ca`.

If the pipeline gateway producer reports not enough in-sync replicas, `kafka.topics.replicationFactor` is below the cluster `min.insync.replicas` (default 2 on MSK); set them equal.

## AWS MSK SASL/SCRAM (new in 2.5.0)
Store the password in a secret, for example `aws-msk-kafka-secret` created with `--from-literal password=<value>`. Values: `protocol: SASL_SSL`, `sasl.mechanism: SCRAM-SHA-512`, `sasl.client.username`, `sasl.client.secret: aws-msk-kafka-secret`, `passwordPath: password`.

## Confluent Cloud SASL/PLAIN (new in 2.5.0)
Create a cluster API key: key is the username, secret the password (kept in secret `confluent-kafka-sasl`). Values: `protocol: SASL_SSL`, `mechanism: PLAIN`, plus `kafka.consumer.messageMaxBytes` and `kafka.producer.messageMaxBytes` of 8388608.

## Confluent Cloud OAUTHBEARER
Register the identity provider and an identity pool in Confluent. The secret (`confluent-kafka-oauth`) holds `method: OIDC`, `client_id`, `client_secret`, `token_endpoint_url`, `extensions` (`logicalCluster=<cluster id>,identityPoolId=<pool id>`) and an empty `scope`. Values use `mechanism: OAUTHBEARER` with `sasl.client.secret` set to that secret.

## Azure Event Hub
Needs at least Standard tier, because Basic lacks the Kafka protocol. Core creates 2 topics per model and pipeline plus one error topic, so total topics are 2 x (models + pipelines) + 1, which may exceed Standard quotas; check quotas if topic creation fails. Do not pre-create Event Hubs. Use the namespace-level connection string (needed to create topics dynamically) as the password in a secret. Values: `bootstrap: <namespace>.servicebus.windows.net`, `mechanism: PLAIN`, and username literally `$ConnectionString`, which is not a variable to replace.

## Checked

2026-11-04. Confirmed against the AWS MSK mTLS and SASL, Confluent SASL and OAuth, and Azure Event Hub pages (Seldon Core 2 docs, v2 branch): secrets, Helm values, ACL steps, min.insync.replicas default, Event Hub tier and topic-count formula. Removed or corrected: the word 'tested' (page does not say tested).

Method: documentation only; no commands were run.
