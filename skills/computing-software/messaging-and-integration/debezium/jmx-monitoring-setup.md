---
id: computing-software.messaging-and-integration.debezium.jmx-monitoring-setup
name: jmx-monitoring-setup
category: computing-software
field: messaging-and-integration
product: debezium
tags: [monitoring, jmx, kafka-connect, metrics]
level: practitioner
status: docs-checked
description: "Enable JMX on Kafka and Kafka Connect, locally or in Debezium images, to read Debezium connector metrics."
sources:
  - https://debezium.io/documentation/reference/stable/operations/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium connectors publish extra JMX metrics (snapshot, streaming, schema history) on top of Kafka and Kafka Connect metrics. You must enable JMX when starting each service.

Local installation, environment variables for `kafka-server-start.sh` and `connect-distributed.sh`:

- `JMX_PORT`: enables JMX and sets `-Dcom.sun.management.jmxremote.port`.
- `KAFKA_JMX_OPTS`: JVM options. Defaults are `-Dcom.sun.management.jmxremote`, `-Dcom.sun.management.jmxremote.authenticate=false` and `-Dcom.sun.management.jmxremote.ssl=false`.

Use a distinct port per service on the same machine.

Docker with Debezium images need extra variables because the JVM must advertise a host name:

- `JMXPORT` (required): used for both `jmxremote.port` and `jmxremote.rmi.port`.
- `JMXHOST` (required): the Docker host address clients use; `localhost` or `127.0.0.1` will not work, and `0.0.0.0` typically does.
- `JMXAUTH`: `true` or `false`, default `false`.
- `JMXSSL`: whether clients use TLS.

Connector metrics exist per connector type (PostgreSQL, MySQL, SQL Server, MongoDB, Oracle and others).

The docs also cover exposing metrics to Prometheus and Grafana and capturing Java Flight Recordings.

Gotcha: the defaults disable authentication and SSL. Restrict the JMX port to a trusted network or enable both.

Check: connect a JMX client such as JConsole and browse the MBeans.

## Checked

2026-11-08. Confirmed against the Debezium page operations/monitoring, read in full: JMX_PORT and KAFKA_JMX_OPTS defaults, the Docker JMXPORT, JMXHOST, JMXAUTH and JMXSSL variables, Prometheus and Grafana and Flight Recorder notes. Removed the claim about customised MBean names and the debezium.* MBean name, which this page does not state.

Method: documentation only; no commands were run.
