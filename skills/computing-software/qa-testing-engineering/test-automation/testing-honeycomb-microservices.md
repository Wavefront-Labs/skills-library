---
id: computing-software.qa-testing-engineering.test-automation.testing-honeycomb-microservices
name: testing-honeycomb-microservices
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [testing-honeycomb, microservices-testing, integration-tests, test-strategy, contract-testing]
level: practitioner
status: draft
description: "Apply the testing honeycomb to microservices: favour service-level integration tests with real dependencies, few implementation-detail unit tests, minimal E2E."
sources:
  - https://engineering.atspotify.com/2018/01/testing-of-microservices
  - https://martinfowler.com/articles/microservice-testing/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing honeycomb for microservices

**Goal:** a test distribution suited to small services whose complexity lies in how they talk to databases, queues and other services, not in internal logic (Spotify engineering, 2018).

## Shape
- **Few "implementation detail" tests:** unit tests only for genuinely complex isolated logic.
- **Most tests are integrated tests of one service:** start the service (in-process or container) with real infrastructure (DB, broker via Testcontainers) and stubbed external services (WireMock), and test through its public API.
- **Few "integration" tests** across several real services; replaced largely by **contract tests** between services.

## Why
Unit tests with heavy mocking in a small service mostly verify the mocks and break on every refactor. Service-level tests survive refactoring, catch wiring and query defects, and still run in seconds with containers.

## Implementing
```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@Testcontainers
class OrderApiTest {
  @Container static PostgreSQLContainer<?> db = new PostgreSQLContainer<>("postgres:16");
  @RegisterExtension static WireMockExtension billing = WireMockExtension.newInstance().build();
  // POST /orders, assert response + row in DB + call made to billing stub
}
```

- One container set per test class or suite to keep speed; reset data between tests.
- Contract tests (Pact) for every consumer/provider pair.
- E2E only for a handful of business-critical journeys in a deployed environment.

## When not to use
Services with rich domain logic (pricing engines) still need a wide unit-test base: choose shape per service.

## Verify
Each service's suite runs locally in minutes, most tests exercise the public API with real infrastructure, and cross-service correctness relies on contracts rather than a large E2E suite.
