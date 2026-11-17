---
id: computing-software.messaging-and-integration.apache-zookeeper.logging-guidelines
name: logging-guidelines
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, logging, logback, slf4j, log-levels, contributor-guidelines]
level: practitioner
status: docs-checked
description: "ZooKeeper logging conventions: slf4j API, logback backend since 3.8.0, level meanings, parameterised messages, per-class loggers and exception handling."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperInternals.html
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging guidelines

- Use the slf4j API in code; logback is the backend since 3.8.0 and users pick the runtime configuration.
- Levels, most to least severe: ERROR, WARN, INFO, DEBUG, TRACE. Production typically logs INFO and above.
- Use parameterised placeholders for dynamic text.
- Name each logger after its class.
- When logging an exception, pass the exception object as the final argument so the stack trace is kept.
- `ZOO_LOG_DIR` (set in zkEnv.sh) chooses the log directory.
- Four-letter word trace masks (`stmk`) need TRACE enabled in logback.

Verify: an exception log line includes a stack trace and parameters are substituted.

## Checked

Method: docs-checked 2026-11-09 against zookeeperInternals.html (Logging and Developer Guidelines sections), zookeeperTools.html (zkEnv.sh) and zookeeperAdmin.html (stmk entry)
