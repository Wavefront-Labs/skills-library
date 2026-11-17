---
id: computing-software.systems-network-administration.apache-tomcat.juli-logging-properties
name: juli-logging-properties
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, logging, juli, logging-properties, asyncfilehandler, log-rotation, maxdays, log-levels, consolehandler, catalina-out]
level: practitioner
status: docs-checked
description: "Configure Tomcat 10.1 JULI logging in conf/logging.properties: AsyncFileHandler directory, prefix, maxDays, bufferSize, per-logger levels, ConsoleHandler duplicates."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JULI logging (`conf/logging.properties`)

Tomcat logging (JULI) is configured in `logging.properties`.

Handler properties from the page's example file:
```properties
1catalina.org.apache.juli.AsyncFileHandler.level = ALL
1catalina.org.apache.juli.AsyncFileHandler.directory = ${catalina.base}/logs
1catalina.org.apache.juli.AsyncFileHandler.prefix = catalina.
1catalina.org.apache.juli.AsyncFileHandler.maxDays = 90
1catalina.org.apache.juli.AsyncFileHandler.encoding = UTF-8
```

- `maxDays = 90` in the example; the `3manager` handler also sets `bufferSize = 16384`.
- Handlers are named with a numeric prefix (`1catalina.`, `2localhost.`, `3manager.`), each with its own `directory`, `prefix` and `encoding`; `${catalina.base}` is used in `directory`.
- Per-host and per-app files: `org.apache.catalina.core.ContainerBase.[Catalina].[localhost].handlers = 2localhost.org.apache.juli.AsyncFileHandler`.

Raise detail for one logger, for example log each component that changes state:
```properties
org.apache.catalina.util.LifecycleBase.level = FINE
```
The example file also sets `ContainerBase.[Catalina].[localhost].[/manager].level = INFO` with the `3manager` handler. A web application can carry its own `WEB-INF/classes/logging.properties` using `${classloader.webappName}.` as the prefix.

Production notes from the page: by default logging goes to both an AsyncFileHandler and a ConsoleHandler, and the console output is usually captured into a file such as `catalina.out`, so you get two copies; consider removing ConsoleHandler. Consider removing AsyncFileHandlers for applications you do not use (for example host-manager), and consider configuring an access log.

## Checked

2026-11-04. Read the Tomcat 10.1 Logging page (logging.html): confirmed the AsyncFileHandler level, directory, prefix, maxDays 90, encoding and bufferSize properties, the ContainerBase per-host and per-manager handlers, the LifecycleBase FINE example, the web application logging.properties with classloader.webappName and the production notes. Removed the handlers lines, level list, maxDays and bufferSize semantics, async tuning, useParentHandlers, LogManager and start-script claims, the session-package example and the rotated-file verify step, none of which the page text shows.

Method: documentation only; no commands were run.
