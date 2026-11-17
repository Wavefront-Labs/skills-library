---
id: computing-software.software-engineering.java.testcontainers-for-java-integration-tests
name: testcontainers-for-java-integration-tests
category: computing-software
field: software-engineering
product: java
tags: [java, java-test-libraries, testcontainers-java, testcontainers, serviceconnection, integration-tests, reusable-containers]
level: practitioner
status: docs-checked
description: "Run real services in JUnit 5 tests with Testcontainers: @Testcontainers, container lifecycle, Spring Boot container beans, @ServiceConnection and dynamic properties."
sources: ["https://java.testcontainers.org/", "https://docs.spring.io/spring-boot/reference/testing/testcontainers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testcontainers for Java integration tests

Testcontainers for Java provides lightweight, throwaway instances of databases, browsers or anything that runs in a Docker container. It needs Docker (see its general Docker requirements) and a supported test framework (JUnit 4, JUnit 5 Jupiter, Spock, or manual lifecycle control). It ships a core JAR plus one JAR per module; use the `testcontainers-bom` to avoid giving each module a version. Private dependencies (docker-java-core, Guava, OkHttp and others) are shaded into the core JAR under `org.testcontainers.shaded`.

## JUnit 5 extension
```java
@Testcontainers
@SpringBootTest
class MyIntegrationTests {
    @Container
    static Neo4jContainer neo4j = new Neo4jContainer("neo4j:5");   // pin the tag
}
```
`@Testcontainers` activates the extension and `@Container` marks container fields. Static fields stop after the test class; non-static fields stop after each test method.

## Spring Boot integration
- **Caution:** Spring's TestContext framework may cache the `ApplicationContext` beyond the point where the extension stopped a container, so a later test or bean destruction can fail on a stopped container. Prefer managing containers as Spring beans (or importing container declarations) when the context must stay usable while cached.
- **Container beans:** declare the container as a `@Bean` in a `@TestConfiguration(proxyBeanMethods = false)` class and `@Import` it into the test. Spring starts container beans before all other beans and stops them after all others are destroyed, once per cached application context.
- **Interface declarations:** declare containers as static fields on an interface and import them with `@ImportTestcontainers(MyContainers.class)` on a test configuration class.
- **`@ServiceConnection`:** annotate the container field (or bean) and Boot creates the matching `ConnectionDetails` bean, overriding connection properties, so no property wiring is needed. Add the `spring-boot-testcontainers` module as a test dependency. A `PostgreSQLContainer` gives both `JdbcConnectionDetails` and `R2dbcConnectionDetails` unless you narrow it with the annotation's `type` attribute.
- **Generic containers:** on a `@Bean` method Boot uses the return type, so with `GenericContainer` you must give the hint, for example `@ServiceConnection(name = "redis")`. The same `name` attribute makes custom or mirrored images match.
- **Dynamic properties:** a static `@DynamicPropertySource` method adds values to the Environment, for example `registry.add("spring.neo4j.uri", neo4j::getBoltUrl)`; more verbose but more flexible than service connections.

## Verify
- [ ] Containers are pinned to an explicit image tag.
- [ ] Tests pass when run alone and in a full suite that reuses cached contexts.

## Checked
Read the Testcontainers for Java home page and the Spring Boot Testcontainers page in full. Removed as unconfirmed: the PostgreSQL JDBC example (the current docs show version 2 package layouts and non-generic container classes), the Boot 3.1 version claim, singleton and reuse properties, wait strategies, CI and Docker-in-Docker variables, registry prefix settings and Failsafe naming advice.
Method: docs-checked 2026-11-09 against the Testcontainers for Java home page and the Spring Boot Testcontainers reference page.
