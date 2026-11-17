---
id: computing-software.messaging-and-integration.apache-activemq-artemis.client-application-logging
name: client-application-logging
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,client-logging,slf4j,log4j2-configurationfile,jms-client,activemq-artemis]
level: intro
status: docs-checked
description: "Enable logging in an Artemis client by adding an SLF4J implementation such as log4j-slf4j2-impl and a log4j2.properties on the classpath or -Dlog4j2.configurationFile."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/logging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging in a client application

The client libraries log through SLF4J, so your application must bring a logging implementation. With Log4j2 and Maven, add the client and the binding:
```xml
<dependency>
   <groupId>org.apache.artemis</groupId>
   <artifactId>artemis-jms-client</artifactId>
   <version>${artemis.version}</version>
</dependency>
<dependency>
   <groupId>org.apache.logging.log4j</groupId>
   <artifactId>log4j-slf4j2-impl</artifactId>
   <version>${log4j.version}</version>
</dependency>
```
Supply configuration as `log4j2.properties` on the classpath (picked up automatically) or point to a file:
```
-Dlog4j2.configurationFile=file:///path/to/custom-log4j2-config.properties
```
Minimal properties from the manual's example, INFO to the console:
```properties
monitorInterval = 5
rootLogger.level = INFO
rootLogger.appenderRef.console.ref = console
logger.activemq.name=org.apache.activemq
logger.activemq.level=INFO
appender.console.type=Console
appender.console.name=console
appender.console.layout.type=PatternLayout
appender.console.layout.pattern=%d %-5level [%logger] %msg%n
```
The manual's full example adds a daily `RollingFile` appender with a cron triggering policy.

## Checked

Method: docs-checked 2026-11-09 against logging.adoc (read in full). Removed the Verify step and unsupported notes.
