---
id: computing-software.data-engineering.apache-kafka.authorization-audit-logging
name: authorization-audit-logging
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, kafka-audit-log, authorizer-log, kafka-acls, compliance]
level: practitioner
status: docs-checked
description: "Capture who did what on Kafka: the kafka.authorizer.logger log4j appender for allowed/denied operations, request logs, routing to a SIEM, and volume control."
sources:
  - https://kafka.apache.org/documentation/#security_authz
  - https://github.com/apache/kafka/blob/trunk/config/log4j2.yaml
  - https://github.com/apache/kafka/blob/trunk/metadata/src/main/java/org/apache/kafka/metadata/authorizer/StandardAuthorizerData.java
  - https://github.com/apache/kafka/blob/trunk/docs/security/security-model.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization audit logging

The built-in `StandardAuthorizer` logs decisions to the `kafka.authorizer.logger` logger:
- **Denied** at INFO level, when access to the resource was explicitly requested (checks that only filter lists or compute authorized operations log at TRACE).
- **Allowed** at DEBUG level (very high volume: every produce/fetch).
Line format: `Principal = User:orders-svc is Denied operation = WRITE from host = 10.1.2.3 on resource = Topic:LITERAL:payments for request = Produce with resourceRefCount = 1 based on rule ...`

## Configure (log4j2, as shipped in `config/log4j2.yaml` for Kafka 4.x)
```yaml
Appenders:
  RollingFile:
    - name: AuthorizerAppender
      fileName: "${sys:kafka.logs.dir}/kafka-authorizer.log"
      filePattern: "${sys:kafka.logs.dir}/kafka-authorizer.log.%d{yyyy-MM-dd-HH}"
      PatternLayout: {pattern: "[%d] %p %m (%c)%n"}
      TimeBasedTriggeringPolicy: {modulate: true, interval: 1}
Loggers:
  Logger:
    - name: kafka.authorizer.logger
      level: INFO              # DEBUG to log ALLOWED too
      additivity: false
      AppenderRef: [{ref: AuthorizerAppender}]
```
Kafka 4.0 migrated logging from Log4j to Log4j2 (see the upgrade notes for the conversion tool); older releases configure the same logger in `log4j.properties`.

## Make it useful
- Ship the file to a log platform off the broker and parse principal, operation, host, resource and decision.
- Alert on bursts of Denied for a principal (misconfigured client or probing).
- Logging every Allowed decision is rarely affordable: enable DEBUG only temporarily during investigations.
- `kafka.request.logger` is set to WARN in the shipped `log4j2.yaml`; the Kafka security model describes its request log as finer-grained detail useful for forensics, at much higher volume.

## Retention and integrity
Kafka has no built-in tamper-evident audit trail, so keep authorizer logs per your compliance rules in durable, append-only storage outside the broker host; broker log rotation discards them.

## Verify
- [ ] An unauthorised test write appears in the SIEM within a minute with principal and host.
- [ ] Broker disk not filling from audit logs (rotation configured).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: the logger name `kafka.authorizer.logger`, Denied at INFO and Allowed at DEBUG (StandardAuthorizerData source, including the TRACE case), the exact log line format built by `buildAuditMessage`, the `AuthorizerAppender` rolling-file settings and logger entry in `config/log4j2.yaml`, `kafka.request.logger` default WARN, the Log4j to Log4j2 migration in the 4.0 upgrade notes, and the no-tamper-evident-trail statement in the security model. Removed: AclAuthorizer, the Confluent Platform description and its source link, named log shippers, the `kafka-metadata-shell` and `kafka.controller` audit suggestion and the one-year retention figure.

Method: documentation only; no commands were run.
