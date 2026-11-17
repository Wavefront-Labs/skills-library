---
id: computing-software.software-engineering.java.mdc-and-structured-logging-with-slf4j
name: mdc-and-structured-logging-with-slf4j
category: computing-software
field: software-engineering
product: java
tags: [java, java-observability, logging-mdc, slf4j, logback, structured-logging, correlation-id, ecs-json-logging]
level: practitioner
status: docs-checked
description: "Add correlation ids with SLF4J MDC, copy them across executor threads, and emit JSON logs with Spring Boot structured logging."
sources: ["https://www.slf4j.org/manual.html#mdc", "https://docs.spring.io/spring-boot/reference/features/logging.html#features.logging.structured", "https://logback.qos.ch/manual/mdc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MDC and structured logging

## MDC for per-request context
```java
public class CorrelationFilter extends OncePerRequestFilter {
    @Override protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String id = Optional.ofNullable(req.getHeader("X-Request-Id")).orElse(UUID.randomUUID().toString());
        MDC.put("requestId", id);
        res.setHeader("X-Request-Id", id);
        try { chain.doFilter(req, res); } finally { MDC.clear(); }
    }
}
```
Show MDC values in Logback lines with a pattern such as `%d %-5level [%X{requestId}] %logger{36} - %msg%n`. In Spring Boot you can add MDC content by overriding only the level pattern, for example `logging.pattern.level=user:%X{user} %5p`.

## Crossing threads
A copy of the MDC cannot always be inherited by worker threads, notably with `java.util.concurrent.Executors` thread pools. Logback's manual recommends calling `MDC.getCopyOfContextMap()` on the submitting thread, and as the task's first action calling `MDC.setContextMap()` with that copy:
```java
Map<String,String> ctx = MDC.getCopyOfContextMap();
executor.submit(() -> { MDC.setContextMap(ctx); try { work(); } finally { MDC.clear(); } });
```

## JSON logs
- Spring Boot supports ECS, GELF and Logstash JSON formats out of the box. Enable with `logging.structured.format.console` (or `.file`) set to `ecs`, `gelf` or `logstash`. Related properties include `logging.structured.json.include`, `exclude`, `rename` and `add` (for example `logging.structured.json.add.service=orders`).
- The ECS format adds every MDC key-value pair to the JSON object.
- SLF4J 2 fluent API adds structured pairs: `log.atInfo().addKeyValue("orderId", id).log("order placed")`; Spring Boot's ECS format includes these key-value pairs too.
- Use parameterised messages (`log.info("user {}", id)`) rather than string concatenation.

## Checked

Method: docs-checked 2026-11-09 against the SLF4J manual (fluent API, addKeyValue, parameterised messages), the Logback MDC manual (managed threads, getCopyOfContextMap and setContextMap) and the Spring Boot logging page (structured logging formats and properties, MDC in ECS, level pattern with %X). Dropped unconfirmed claims (Micrometer traceId in MDC, TaskDecorator, exception-last rule, secrets redaction, async appender drops, log injection, Actuator loggers, pre-3.4 encoder).
