---
id: computing-software.software-engineering.spring-boot.log-levels-and-groups
name: log-levels-and-groups
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, logging, logging-level, log-groups, root-logger, environment-variables]
level: intro
status: docs-checked
description: "Set logger levels with logging.level.<name>, via environment variables, and define logging.group.* groups; includes the predefined web and sql groups."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All supported logging systems take levels from the Spring Environment as `logging.level.<logger-name>=<level>`, where level is TRACE, DEBUG, INFO, WARN, ERROR, FATAL or OFF. The root logger is `logging.level.root`.

```yaml
logging:
  level:
    root: "warn"
    org.springframework.web: "debug"
    org.hibernate: "error"
```

Environment variable form: `LOGGING_LEVEL_ORG_SPRINGFRAMEWORK_WEB=DEBUG` sets `org.springframework.web` to DEBUG. This works only at package level: relaxed binding always lowercases environment variable names, so a single class cannot be configured this way. For a class use the `SPRING_APPLICATION_JSON` variable instead.

Log groups let you configure several loggers at once:
```yaml
logging:
  group:
    tomcat: "org.apache.catalina,org.apache.coyote,org.apache.tomcat"
  level:
    tomcat: "trace"
```

Predefined groups:
- `web`: `org.springframework.core.codec`, `org.springframework.http`, `org.springframework.web`, `org.springframework.boot.actuate.endpoint.web`, `org.springframework.boot.web.servlet.ServletContextInitializerBeans`
- `sql`: `org.springframework.jdbc.core`, `org.hibernate.SQL`, and the jOOQ `LoggerListener`

Levels can also be changed at runtime through the actuator loggers endpoint (see actuator-loggers-endpoint).

## Checked

2026-11-07

Read logging.adoc (docs-repo source of the cited Logging page) in full (935 lines), using the Log Levels and Log Groups sections. The closing sentence about the actuator loggers endpoint is not on the Logging page; it rests on loggers.adoc, which was read in full for the actuator-loggers-endpoint skill.
Confirmed: logging.level.<logger-name> with TRACE, DEBUG, INFO, WARN, ERROR, FATAL, OFF; logging.level.root; the YAML example; LOGGING_LEVEL_ORG_SPRINGFRAMEWORK_WEB=DEBUG; package-level-only limit because relaxed binding lowercases environment variables, with SPRING_APPLICATION_JSON as the class-level route; the tomcat group example; the predefined web and sql groups with their logger lists.
Nothing trimmed.

Method: documentation only; no commands were run.
