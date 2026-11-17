---
id: computing-software.software-engineering.spring-boot.startup-failure-and-lazy-init
name: startup-failure-and-lazy-init
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, failureanalyzer, startup-failure, conditions-report, lazy-initialization, spring-main-lazy-initialization]
level: practitioner
status: docs-checked
description: "Diagnose Spring Boot startup failures with FailureAnalyzers and the --debug conditions report, and enable lazy initialization with its trade-offs."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Startup information: INFO logging shows startup details such as the launching user. Turn it off with `spring.main.log-startup-info=false` (this also stops logging the active profiles). Override `logStartupInfo(boolean)` in a `SpringApplication` subclass to add more.

Failure analysis: when startup fails, registered `FailureAnalyzer` beans can print a dedicated message and a concrete action. Example: port 8080 in use gives "Embedded servlet container failed to start. Port 8080 was already in use." with the action to stop the listening process or configure another port. You can add your own analyzers (see the how-to guide).

When no analyzer handles the exception, display the full conditions report: enable the `debug` property (`java -jar myproject-0.0.1-SNAPSHOT.jar --debug`) or enable `DEBUG` logging for `ConditionEvaluationReportLoggingListener`.

Lazy initialization creates beans when needed instead of at startup, which can reduce startup time. In a web app many web beans are not initialized until the first HTTP request.

Enable via `SpringApplicationBuilder.lazyInitialization`, `SpringApplication.setLazyInitialization`, or:
```yaml
spring:
  main:
    lazy-initialization: true
```
Downsides stated on the page: a misconfigured bean fails only when first initialized rather than at startup, and the JVM needs enough memory for all beans, not just those created at startup. Hence it is off by default and tuning the JVM heap first is recommended.

Exclude specific beans with `@Lazy(false)`.

## Checked

2026-11-07. Read features/spring-application.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
