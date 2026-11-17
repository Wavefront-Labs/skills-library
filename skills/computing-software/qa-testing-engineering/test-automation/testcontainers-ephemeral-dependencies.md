---
id: computing-software.qa-testing-engineering.test-automation.testcontainers-ephemeral-dependencies
name: testcontainers-ephemeral-dependencies
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [testcontainers, integration-testing, docker, ephemeral-dependencies, test-data-management]
level: practitioner
status: draft
description: "Run integration tests against real Postgres, Kafka or Redis in throwaway containers with Testcontainers (Java, Python, Node): wait strategies, reuse and CI setup."
sources:
  - https://java.testcontainers.org/
  - https://testcontainers-python.readthedocs.io/
  - https://node.testcontainers.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ephemeral dependencies with Testcontainers

**Goal:** integration tests use real infrastructure versions, started and destroyed by the test run, no shared test DB.

## Java (JUnit 5)
```java
@Testcontainers
class OrderRepoIT {
  @Container
  static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");

  @DynamicPropertySource
  static void props(DynamicPropertyRegistry r) {
    r.add("spring.datasource.url", pg::getJdbcUrl);
    r.add("spring.datasource.username", pg::getUsername);
    r.add("spring.datasource.password", pg::getPassword);
  }
}
```
Spring Boot 3.1+: `@ServiceConnection` on the container field replaces the property wiring.

## Python
```python
from testcontainers.postgres import PostgresContainer
@pytest.fixture(scope="session")
def pg_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()
```

## Node
```ts
const pg = await new PostgreSqlContainer('postgres:16-alpine').start();
process.env.DATABASE_URL = pg.getConnectionUri();
afterAll(() => pg.stop());
```

## Wait strategies
Default waits for the mapped port; for apps use `Wait.forLogMessage(".*ready.*", 1)` or `Wait.forHttp("/health")`. Most container failures in CI are wrong wait strategies.

## Speed
- Session/class-scoped containers + per-test data reset (rollback/truncate).
- Pin image tags; pre-pull images in CI.
- Local only: `testcontainers.reuse.enable=true` in `~/.testcontainers.properties` and `.withReuse(true)` to keep containers between runs.

## CI
Needs a Docker daemon: GitHub Actions ubuntu runners work out of the box; in Kubernetes runners use Docker-in-Docker or Testcontainers Cloud. Ryuk (the reaper container) cleans up; disable only if your CI forbids privileged containers (`TESTCONTAINERS_RYUK_DISABLED=true`), then clean up yourself.

## Gotchas
- Never hard-code ports; always read the mapped port from the container.
- Apple Silicon: some images lack arm64 variants; pick multi-arch tags.

## Verify
Suite runs on a clean machine with only Docker installed, and no containers are left running after (`docker ps`).
