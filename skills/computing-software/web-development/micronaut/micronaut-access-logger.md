---
id: computing-software.web-development.micronaut.micronaut-access-logger
name: micronaut-access-logger
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, access-logger, access-log, logback, log-format, netty]
level: intro
status: docs-checked
description: "Turn on the Micronaut Netty HTTP access logger, choose a log format and exclusions, and route its output to a dedicated Logback appender."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/accessLogger.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut access logger

Goal: Apache-style access logs for the HTTP server (works for HTTP/1 and HTTP/2).

## Enable
```yaml
micronaut:
  server:
    netty:
      access-logger:
        enabled: true
        logger-name: my-access-logger   # default HTTP_ACCESS_LOGGER
        log-format: common              # default: Common Log Format
        exclusions:                     # regexes of paths not to log
          - /health
          - /path/.+
```

## Add a logger for that name
Enabling is not enough; define a logger for the name (default `HTTP_ACCESS_LOGGER`). In Logback keep the pattern to just `%msg%n`, because the access logger formats the line itself:
```xml
<appender name="httpAccessLogAppender" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <append>true</append>
    <file>log/http-access.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
        <fileNamePattern>log/http-access-%d{yyyy-MM-dd}.log</fileNamePattern>
        <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder>
        <charset>UTF-8</charset>
        <pattern>%msg%n</pattern>
    </encoder>
    <immediateFlush>true</immediateFlush>
</appender>

<logger name="HTTP_ACCESS_LOGGER" additivity="false" level="info">
    <appender-ref ref="httpAccessLogAppender" />
</logger>
```

## Log format markers (Apache httpd syntax)
`%a` remote IP, `%A` local IP, `%b` bytes sent ('-' if none), `%B` bytes sent, `%h` remote host, `%H` protocol, `%{h}i` request header, `%{h}o` response header, `%{c}C` request cookie, `%{c}c` response cookie, `%l` identd user (always '-'), `%m` method, `%p` local port, `%q` query string, `%r` first request line, `%{attr}r` a Micronaut request attribute (read when response headers are written, '-' if unset), `%s` status, `%{format}t` time (`begin:` default or `end:` prefix, `DateTimeFormatter` syntax), `%{property}u` authenticated user (with micronaut-session the session id if no argument), `%U` URI, `%v` server name, `%D` ms taken, `%T` seconds taken. Omitting the argument of `%i`, `%o`, `%C`, `%c` prints all.

Aliases: `common` = `%h %l %u %t "%r" %s %b`; `combined` = `%h %l %u %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"`.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
