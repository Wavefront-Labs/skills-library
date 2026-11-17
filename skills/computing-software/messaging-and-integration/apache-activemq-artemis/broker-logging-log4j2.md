---
id: computing-software.messaging-and-integration.apache-activemq-artemis.broker-logging-log4j2
name: broker-logging-log4j2
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,logging,log4j2,log4j2-properties,monitorinterval,logger-levels,trace,activemq-artemis]
level: practitioner
status: docs-checked
description: "Configure broker logging via log4j2.properties: the named loggers, raising one to TRACE, and reloading with monitorInterval."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/logging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broker logging

Artemis uses the SLF4J facade, with Log4j 2 shipped as the implementation. When started with `run`, config comes from `log4j2.properties` in the broker instance `etc` directory (console and file by default). Other CLI commands use `log4j2-utility.properties`, which by default logs only errors to the console.

## Loggers
`rootLogger` (anything unhandled), `org.apache.activemq.artemis.core.server`, `org.apache.activemq.artemis.utils`, `org.apache.activemq.artemis.journal`, `org.apache.activemq.artemis.jms`, `org.apache.activemq.artemis.integration.bootstrap`, plus three audit loggers (disabled by default): `org.apache.activemq.audit.base`, `.resource`, `.message`.

## Raise one logger
To get TRACE from `org.foo`:
```properties
logger.my_logger_ref.name=org.foo
logger.my_logger_ref.level=TRACE
```

## Reload without restart
```properties
# Monitor config file every 5 seconds for updates
monitorInterval = 5
```
Log4j2 reloads the file itself at that interval (seconds).

## Checked

Method: docs-checked 2026-11-09 against logging.adoc (read in full). Removed the Verify step and an unsupported notes section.
