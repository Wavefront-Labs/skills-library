---
id: computing-software.messaging-and-integration.apache-activemq-artemis.audit-logging
name: audit-logging
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,audit-logging,audit-base,audit-resource,audit-message,audit-log,activemq-artemis]
level: practitioner
status: docs-checked
description: "Turn on the three Artemis audit loggers (base, resource, message) by changing their log4j2 levels from OFF to INFO; output goes to audit.log."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/logging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit logging

Three audit loggers can be enabled separately:
- **base**: highly verbose, captures most events on JMX beans.
- **resource**: creation, update and deletion of resources such as addresses and queues, plus authentication; its main purpose is tracking console activity and access.
- **message**: production and consumption of messages.

They are disabled in the broker's `log4j2.properties`:
```properties
logger.audit_base.name = org.apache.activemq.audit.base
logger.audit_base.level = OFF
logger.audit_base.appenderRef.audit_log_file.ref = audit_log_file
logger.audit_base.additivity = false
```
(and the same pattern for `audit_resource` with `org.apache.activemq.audit.resource` and `audit_message` with `org.apache.activemq.audit.message`.) To enable, change the level from `OFF` to `INFO`, for example `logger.audit_base.level = INFO`. Once enabled, records go to a separate log file, by default `audit.log`.

All extra logging negatively impacts performance; whether it is too much depends on the use case.

## Checked

Method: docs-checked 2026-11-09 against logging.adoc (read in full). Removed the Verify step and an unsupported claim.
