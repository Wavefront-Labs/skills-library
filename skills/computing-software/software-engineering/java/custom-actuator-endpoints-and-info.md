---
id: computing-software.software-engineering.java.custom-actuator-endpoints-and-info
name: custom-actuator-endpoints-and-info
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot-core, custom-actuator-endpoint, actuator, endpoint-exposure]
level: practitioner
status: docs-checked
description: "Add custom Spring Boot Actuator endpoints with @Endpoint and @ReadOperation, expose them over HTTP and JMX, and secure them correctly."
sources: ["https://docs.spring.io/spring-boot/reference/actuator/endpoints.html#actuator.endpoints.implementing-custom", "https://docs.spring.io/spring-boot/reference/actuator/endpoints.html#actuator.endpoints.security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom actuator endpoints

```java
@Component
@Endpoint(id = "features")                         // GET /actuator/features
public class FeaturesEndpoint {
    private final Map<String, Boolean> flags = new ConcurrentHashMap<>();

    @ReadOperation public Map<String, Boolean> all() { return flags; }
    @WriteOperation public void set(String name, boolean enabled) { flags.put(name, enabled); }
}
```
```yaml
management:
  endpoints.web.exposure.include: health,features
```
A bean annotated `@Endpoint` has its `@ReadOperation`, `@WriteOperation` and `@DeleteOperation` methods exposed automatically over JMX and, in a web application, over HTTP (Jersey, Spring MVC or WebFlux; Spring MVC wins if both Jersey and MVC are present). Use `@WebEndpoint` or `@JmxEndpoint` to restrict an endpoint to one technology; `@WebEndpoint` is exposed only over HTTP, not JMX.

## Gotchas
- Only `health` is exposed by default, over both web and JMX (`management.endpoints.web.exposure.include` and `management.endpoints.jmx.exposure.include` default to `health`); a custom endpoint must be listed in `exposure.include`.
- Write operations on an unauthenticated management endpoint are an attack surface: secure endpoints with Spring Security rules built on `EndpointRequest`.

## Verify
`curl localhost:8080/actuator/features` returns JSON once the endpoint id is in the exposure list.

## Checked

Method: docs-checked 2026-11-09 against the Spring Boot actuator endpoints page (exposure defaults table, EndpointRequest security section, Implementing Custom Endpoints). Dropped unconfirmed claims (Selector paths, InfoContributor, HealthIndicator, show-details, separate management port, health probe advice, env sanitising).
