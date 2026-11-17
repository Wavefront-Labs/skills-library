---
id: computing-software.cloud-infrastructure-engineering.docker.testcontainers-for-java-junit5
name: testcontainers-for-java-junit5
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers, testcontainers-java, junit5, spring-boot, service-connection, dynamic-property-source, singleton-container, integration-tests]
level: practitioner
status: docs-checked
description: "Write Java integration tests with Testcontainers: BOM and module deps, JUnit 5 @Container lifecycles, Spring Boot @ServiceConnection, singleton containers, JDBC URL shortcut."
sources: ["https://java.testcontainers.org/quickstart/junit_5_quickstart/", "https://java.testcontainers.org/test_framework_integration/junit_5/", "https://java.testcontainers.org/test_framework_integration/manual_lifecycle_control/", "https://java.testcontainers.org/modules/databases/jdbc/", "https://java.testcontainers.org/modules/databases/postgres/", "https://java.testcontainers.org/features/reuse/", "https://docs.spring.io/spring-boot/reference/testing/testcontainers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testcontainers for Java (JUnit 5)

## Dependencies
Use the BOM so module versions stay aligned:
```xml
<dependencyManagement><dependencies>
  <dependency>
    <groupId>org.testcontainers</groupId><artifactId>testcontainers-bom</artifactId>
    <version>${testcontainers.version}</version><type>pom</type><scope>import</scope>
  </dependency>
</dependencies></dependencyManagement>
<dependencies>
  <dependency><groupId>org.testcontainers</groupId><artifactId>testcontainers-junit-jupiter</artifactId><scope>test</scope></dependency>
  <dependency><groupId>org.testcontainers</groupId><artifactId>testcontainers-postgresql</artifactId><scope>test</scope></dependency>
</dependencies>
```
Gradle: `testImplementation platform("org.testcontainers:testcontainers-bom:$tcVersion")` plus
the modules, and `test { useJUnitPlatform() }`. These are the Testcontainers 2.x coordinates
(`testcontainers-junit-jupiter`, `testcontainers-postgresql`, and the core `testcontainers`); the
current quickstart and Postgres module pages use them. A Postgres JDBC driver must be added
separately. In 2.x `PostgreSQLContainer` is in `org.testcontainers.postgresql` and is not generic
(`PostgreSQLContainer pg`); on 1.x it is `PostgreSQLContainer<?>` in `org.testcontainers.containers`.

## JUnit 5 lifecycle
```java
@Testcontainers
class OrderRepositoryTest {
    @Container   // static = one container for the class; instance field = one per test method
    static PostgreSQLContainer pg = new PostgreSQLContainer("postgres:16-alpine")
        .withInitScript("schema.sql");

    @Test
    void savesOrder() throws Exception {
        try (var conn = DriverManager.getConnection(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())) {
            // ...
        }
    }
}
```
Always use `getJdbcUrl()`, `getHost()`, `getMappedPort(5432)`; ports are random.

## Spring Boot
Spring Boot's `@ServiceConnection` wires connection details automatically; for a `GenericContainer` the
`name` attribute says which service the image is (`@ServiceConnection(name = "redis")`):
```java
@SpringBootTest
@Testcontainers
class ApiIT {
    @Container @ServiceConnection
    static PostgreSQLContainer pg = new PostgreSQLContainer("postgres:16-alpine");
    @Container @ServiceConnection(name = "redis")
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine").withExposedPorts(6379);
}
```
Without service connections (the Spring Boot docs call this more verbose but more flexible), use `@DynamicPropertySource`:
```java
@DynamicPropertySource
static void props(DynamicPropertyRegistry r) {
    r.add("spring.datasource.url", pg::getJdbcUrl);
    r.add("spring.datasource.username", pg::getUsername);
    r.add("spring.datasource.password", pg::getPassword);
}
```
To run the app locally against containers, Spring Boot's docs describe a test-classpath main class that launches the application with `SpringApplication.from(...)` and a container configuration.

## Singleton containers (fast suites)
Per-class containers restart Postgres for every test class. Share one per JVM:
```java
abstract class AbstractIT {
    static final PostgreSQLContainer PG = new PostgreSQLContainer("postgres:16-alpine");
    static { PG.start(); }      // stopped by Ryuk at the end of the suite; no @Container annotation here
}
```
All inheriting test classes share the one container; isolate tests with transactions or truncation.

## JDBC URL shortcut
For quick DAO tests with no container code, modify the JDBC URL, for example `jdbc:tc:postgresql:16-alpine:///databasename`, as shown on the
JDBC page; the Testcontainers JDBC driver (`org.testcontainers.jdbc.ContainerDatabaseDriver`)
must be on the classpath, and Spring Boot 2.3.0 and later picks the driver up from the URL.

## Gotchas
- Pin image tags (`postgres:16-alpine`), never `latest`.
- The JUnit 5 extension has only been tested with sequential test execution; parallel execution is documented as unsupported.
- Reuse across runs: `.withReuse(true)` plus `TESTCONTAINERS_REUSE_ENABLE=true` or
  `testcontainers.reuse.enable=true` in `~/.testcontainers.properties` (not in a classpath properties file);
  start the container manually and do not call `stop()`. Container configuration must be identical to be reused.
- CI and Ryuk/socket settings: see the testcontainers-ryuk-ci-and-wait-strategies skill.

## Verify
```bash
./mvnw -Dtest=OrderRepositoryTest test     # docker ps during the run shows the postgres container and a Ryuk container
```

## Checked
Documentation release: testcontainers-java 2.0.5 docs (quickstart/junit_5_quickstart, test_framework_integration/junit_5 and manual_lifecycle_control, features/reuse, modules/databases/jdbc and postgres) and source (modules/postgresql, modules/jdbc), plus the Spring Boot reference page "Testcontainers" and "Dev Services" (main as of 2026-10-26).
Confirmed: artifacts `testcontainers-junit-jupiter` and `testcontainers-postgresql`; non-generic `org.testcontainers.postgresql.PostgreSQLContainer` with `withInitScript`; static vs instance `@Container` lifecycles; singleton container pattern stopped by Ryuk; sequential-only JUnit 5 extension note; reuse via `TESTCONTAINERS_REUSE_ENABLE` or user properties file only; `jdbc:tc:` URLs and the Spring Boot 2.3.0 driver note; `@ServiceConnection` with `name` for generic containers; `@DynamicPropertySource`; `SpringApplication.from(...)` at development time.
Corrected: 2.x coordinates and generics; parallel execution is not supported by the extension (the text said static containers are fine); reuse needs the container started manually.
Removed as unsupported: the "Boot 3.1+" gate, the exact Ryuk-at-JVM-exit wording, the `TestApplication` snippet and Spring context caching remark.
Method: documentation only; no commands were run.
