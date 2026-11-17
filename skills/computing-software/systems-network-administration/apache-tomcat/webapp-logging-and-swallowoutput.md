---
id: computing-software.systems-network-administration.apache-tomcat.webapp-logging-and-swallowoutput
name: webapp-logging-and-swallowoutput
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, logging, per-webapp-logging, swallowoutput, servletcontext-log, classloader-webappname, log4j]
level: practitioner
status: docs-checked
description: "Give a Tomcat 10.1 web app its own log files with WEB-INF/classes/logging.properties, plus the page's production logging tips and the Log4j pointer."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-application logging

`WEB-INF/classes/logging.properties`:
```properties
handlers = org.apache.juli.AsyncFileHandler, java.util.logging.ConsoleHandler

org.apache.juli.AsyncFileHandler.level = ALL
org.apache.juli.AsyncFileHandler.directory = ${catalina.base}/logs
org.apache.juli.AsyncFileHandler.prefix = ${classloader.webappName}.
org.apache.juli.AsyncFileHandler.encoding = UTF-8

java.util.logging.ConsoleHandler.level = ALL
java.util.logging.ConsoleHandler.formatter = org.apache.juli.OneLineFormatter
```
The page's example for a web app uses `${classloader.webappName}` as the file prefix. Production tips from the page: consider removing the ConsoleHandler (output is usually captured to catalina.out, so messages appear twice) and the AsyncFileHandlers of unused apps, and consider configuring an access log.

Log4j: the page gives no steps and points to the Log4j project's instructions for Tomcat's internal logging.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Logging page (web app logging.properties example, production notes, Log4j pointer). Removed the other substitution variables, the servlet log levels and logger category, the swallowOutput claims, the same-named-loggers claim and the generic verify line; the fetched page text did not contain them.

Method: documentation only; no commands were run.
