---
id: computing-software.messaging-and-integration.apache-kafka.kafka-secure-running-cluster
name: kafka-secure-running-cluster
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, security-inter-broker-protocol, incremental-bounce, ssl-migration]
level: practitioner
status: docs-checked
description: "Add SSL or SASL to a live cluster in phased rolling bounces while keeping a PLAINTEXT port open until the end."
sources:
  - https://kafka.apache.org/42/security/incorporating-security-features-in-a-running-cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: secure a running cluster without downtime.

Phases:
1. Incrementally bounce brokers to open additional secured ports.
2. Restart clients on the secured port instead of PLAINTEXT.
3. Incrementally bounce again to enable broker-to-broker security if required.
4. Final incremental bounce to close the PLAINTEXT port.

Client-broker and broker-broker protocols must be enabled in separate bounces, and a PLAINTEXT port must stay open throughout. Stop brokers cleanly with SIGTERM, and wait for restarted replicas to rejoin the ISR before moving to the next node.

SSL everywhere example:
```
# bounce 1
listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092
# clients: bootstrap.servers=[broker1:9092,...] security.protocol=SSL
# bounce 2
listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092
security.inter.broker.protocol=SSL
# bounce 3
listeners=SSL://broker1:9092
security.inter.broker.protocol=SSL
```
To add SASL authentication for clients while keeping SSL between brokers, open a second secured port in the first bounce: `listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092,SASL_SSL://broker1:9093`, point clients at 9093 with `security.protocol = SASL_SSL`, use `security.inter.broker.protocol=SSL` in bounce 2, and finish with `listeners=SSL://broker1:9092,SASL_SSL://broker1:9093`.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 page Incorporating Security Features in a Running Cluster (full page). An unsupported closing rationale paragraph was removed.
