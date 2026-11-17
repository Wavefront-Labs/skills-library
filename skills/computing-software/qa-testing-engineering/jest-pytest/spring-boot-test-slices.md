---
id: computing-software.qa-testing-engineering.jest-pytest.spring-boot-test-slices
name: spring-boot-test-slices
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [spring-boot-test, webmvctest, datajpatest, mockitobean, springboottest]
level: practitioner
status: docs-checked
description: "Test Spring Boot apps with the right slice: @WebMvcTest with MockMvc, @DataJpaTest, @JsonTest, full @SpringBootTest with random port, @MockitoBean and context caching."
sources:
  - https://github.com/spring-projects/spring-boot/blob/main/documentation/spring-boot-docs/src/docs/antora/modules/reference/pages/testing/spring-boot-applications.adoc
  - https://github.com/spring-projects/spring-boot/blob/main/documentation/spring-boot-docs/src/docs/antora/modules/reference/pages/testing/test-modules.adoc
  - https://github.com/spring-projects/spring-boot/blob/main/documentation/spring-boot-docs/src/docs/antora/modules/reference/pages/testing/testcontainers.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/testing/testcontext-framework/ctx-management/caching.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/testing/annotations/integration-spring/annotation-mockitobean.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Boot test slices

## Pick the narrowest slice
In Spring Boot 4 the slice annotations come from per-technology test modules, for example `@WebMvcTest` (package `org.springframework.boot.webmvc.test.autoconfigure`, module `spring-boot-webmvc-test`), `@DataJpaTest` (`spring-boot-data-jpa-test`) and `@RestClientTest` (`spring-boot-restclient-test`); check imports when upgrading from 3.x.

| Annotation | Loads | Use |
|---|---|---|
| `@WebMvcTest(OrderController.class)` | MVC infrastructure; scans controllers, controller advice, filters and similar web beans, not plain `@Component` beans | controller mapping, validation, JSON |
| `@DataJpaTest` | JPA, repositories, embedded/test DB, transactional rollback | queries, mappings |
| `@JsonTest` | Jackson config | serialisation contracts |
| `@RestClientTest` | Jackson/Gson/Jsonb, a `RestClient.Builder` and `MockRestServiceServer` | outbound HTTP clients |
| `@SpringBootTest` | whole context | integration, wiring |

## WebMvcTest
```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
  @Autowired MockMvc mvc;
  @MockitoBean OrderService service;        // Spring Framework annotation: org.springframework.test.context.bean.override.mockito.MockitoBean

  @Test void returns404() throws Exception {
    when(service.find(42L)).thenReturn(Optional.empty());
    mvc.perform(get("/orders/42").accept(MediaType.APPLICATION_JSON))
       .andExpect(status().isNotFound())
       .andExpect(jsonPath("$.error").value("not_found"));
  }
}
```

## DataJpaTest with a real database
```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepoTest {
  @Container @ServiceConnection static PostgreSQLContainer pg = /* container for your production Postgres version */;
  @Autowired OrderRepository repo;
}
```
H2 hides dialect differences; prefer the production engine via Testcontainers.

## Full context
```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient              // org.springframework.boot.resttestclient.autoconfigure
class ApiIT { @Autowired RestTestClient client; /* or WebTestClient with @AutoConfigureWebTestClient */ }
```

## Context caching
Spring caches contexts under a key built from the configuration classes, active profiles, `@TestPropertySource`, `@DynamicPropertySource` methods, bean overrides such as `@MockitoBean` / `@MockitoSpyBean`, and more. Any difference creates a new context (slow). Standardise mocks in a shared base class or meta-annotation; `@DirtiesContext` only when unavoidable.

## Gotchas
- `@SpringBootTest` defaults to a mock web environment without a server; to use `MockMvc` (or `MockMvcTester`, `RestTestClient`) there, add `@AutoConfigureMockMvc` (or the matching `@AutoConfigure...` annotation).
- `@Transactional` rolls tests back by default, but with `RANDOM_PORT` or `DEFINED_PORT` the client and server run in separate threads and transactions, so server-side work is not rolled back.
- With Spring Security on the classpath `@WebMvcTest` also picks up security configuration; use Spring Security's test support rather than disabling security.

## Verify
Test logs show few context loads ("Started ... in") for the whole suite; slice tests run in seconds.

## Checked

Date: 2026-10-25. Documentation release: Spring Boot 4.1.2 and Spring Framework 7.0.10 (GitHub main documentation sources; releases of 2026-10-22).

Confirmed: `@SpringBootTest` web environments and the default MOCK mode; `@AutoConfigureMockMvc` / `@AutoConfigureRestTestClient` / `@AutoConfigureWebTestClient`; `@WebMvcTest` scanning rules, Security behaviour and module names; `@DataJpaTest` transactional by default and `@AutoConfigureTestDatabase`; `@RestClientTest` contents; `@MockitoBean` as a Spring Framework annotation; context cache key components; Testcontainers `@Testcontainers` / `@Container` on static fields, `@ServiceConnection`, and the `org.testcontainers.postgresql.PostgreSQLContainer` class.

Removed as unconfirmed: the `TestRestTemplate` example (not in the Boot 4 testing docs; replaced by `RestTestClient`), the "Spring Boot 3.4+" version note, the generic `PostgreSQLContainer<?>` constructor with a pinned postgres:16 image, and the `@WithMockUser` name.

Method: documentation only; no commands were run.
