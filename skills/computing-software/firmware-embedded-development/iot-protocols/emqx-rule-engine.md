---
id: computing-software.firmware-embedded-development.iot-protocols.emqx-rule-engine
name: emqx-rule-engine
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [emqx-rule-engine, emqx-broker, emqx, rule-engine, sql, connector, iot-protocols]
level: practitioner
status: docs-checked
description: "EMQX rule engine and data integration: Route and transform MQTT messages inside EMQX without a custom consumer."
sources:
  - https://docs.emqx.com/en/emqx/latest/data-integration/rules.html
  - https://docs.emqx.com/en/emqx/latest/data-integration/rule-sql-syntax.html
  - https://docs.emqx.com/en/emqx/latest/data-integration/rule-sql-events-and-fields.html
  - https://docs.emqx.com/en/emqx/latest/data-integration/data-bridges.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EMQX rule engine and data integration

**Goal:** Route and transform MQTT messages inside EMQX without a custom consumer.

## Steps
1. Rules are SQL: the FROM clause names the source (a topic filter or event) and WHERE filters; for example `SELECT payload.temp AS t, clientid FROM "sensors/+/data" WHERE payload.temp > 30`; the `.` syntax needs JSON or Map payloads, otherwise convert with SQL functions
2. Event topics such as `$events/client_connected` and `$events/message_dropped` feed rules (the events page also lists slash forms such as `$events/client/connected`)
3. Attach actions: message republish, console output, or a sink to an external system through a connector (Kafka, PostgreSQL, HTTP, Amazon S3 and others); actions run in order
4. Test with the Dashboard rule test feature using a sample payload
5. Create rules in the Dashboard

## Gotcha
Heavy SQL on large payloads at a high message rate costs CPU, so filter early in WHERE. Sink metrics count matched, success, failed, inflight, queuing and dropped messages, so watch failed and dropped counts.

## Verify
- [ ] SQL tester returns expected output
- [ ] Sink metrics show matched and success counts
- [ ] Failed deliveries show in failed or queuing counts

## Checked

2026-11-03. Confirmed in the EMQX Rule Engine, Rule SQL syntax, SQL events and fields, and Data Integration pages: SELECT/FROM/WHERE structure, `payload.` field syntax, event topics, action types, sinks and connectors, rule test feature, metrics list. Removed: the claim that rules are configured through HOCON files and the REST API, and the "rule metrics" retry claim.
Method: documentation only; no commands were run.
