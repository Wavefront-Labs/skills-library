---
id: computing-software.cloud-infrastructure-engineering.graylog.outputs-and-kafka
name: outputs-and-kafka
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [outputs, kafka-output, output-framework, cluster-to-cluster, journal-output]
level: advanced
status: docs-checked
description: "Send stream data out of Graylog with outputs: output types, journal preference and Enterprise Kafka output requirements."
sources:
  - https://go2docs.graylog.org/current/interacting_with_your_log_data/outputs.htm
  - https://go2docs.graylog.org/current/interacting_with_your_log_data/kafka_output.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# outputs and kafka

All streams write to the OpenSearch output by default. Extra outputs attach per stream; an output must be attached to a stream to send logs out.

Output types: Cluster-to-Cluster Forwarder (Enterprise, source to destination cluster), Enterprise Output Framework outputs (write to an on-disk journal, then send), and legacy non-framework outputs. Journal outputs are preferred for reliability.

**Kafka output** (Enterprise): create at **System > Outputs**, choose Kafka [Enterprise], Launch new output. Prerequisites: permission to manage outputs, every Graylog node can reach a broker (default port 9092), and the topic exists (or auto-creation is on); otherwise messages queue in the journal. Send Buffer Size defaults to 4096 and must be a power of two. For TLS or mutual TLS, keep truststore and keystore at the same local path on every node; this also applies to SASL over TLS. A message key field routes same-key records to one Kafka partition, but per-key ordering also needs Number of concurrent message senders set to 1 (default 2), and order holds only among messages handled by one Graylog node. TLS and SASL settings go in the Custom Kafka properties field as plain Kafka producer properties; those values are not encrypted, so anyone who can view the output can see the passwords. The undelivered journal is purged after Maximum Journal Message Age (default 12h).

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/interacting_with_your_log_data/outputs.htm and https://go2docs.graylog.org/current/interacting_with_your_log_data/kafka_output.htm (both read in full; the Kafka page is marked as introduced in Graylog 7.2). Corrected the ordering claim: a key alone does not guarantee order.
