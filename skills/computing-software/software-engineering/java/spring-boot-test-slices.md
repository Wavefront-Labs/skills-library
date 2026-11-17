---
id: computing-software.software-engineering.java.spring-boot-test-slices
name: spring-boot-test-slices
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, webmvctest, springboottest, datajpatest, test-slices]
level: practitioner
status: gated
description: "Choose and write Spring Boot test slices: @WebMvcTest, @DataJpaTest and @SpringBootTest, with mocks, test databases, context caching and speed trade-offs."
sources: ["https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Boot test slices

**Goal:** the smallest context that proves the behaviour.

## Which slice
| Annotation | Loads | Use for |
|---|---|---|
| `@WebMvcTest(UserController.class)` | MVC layer only (controllers, advice, converters, security filters), no services | request mapping, validation, JSON, status codes |
| `@DataJpaTest` | `@Entity` scanning, Spring Data JPA repositories, embedded DB if available; tests are transactional and roll back | queries, mappings |
| `@SpringBootTest` | full context | wiring and end-to-end flows |
| `@JsonTest`, `@RestClientTest` | JSON mapping / REST client (`@RestClientTest` not on the fetched page) (gated: unconfirmed, source is paywalled or blocked) | focused |

## Examples
```java
@WebMvcTest(UserController.class)
class UserControllerTest {
  @Autowired MockMvc mvc;
  @MockitoBean UserService service;     // Spring Framework annotation (org.springframework.test.context.bean.override.mockito); older Boot used @MockBean
  @Test void notFound() throws Exception {
    when(service.find(1L)).thenThrow(new NotFoundException());
    mvc.perform(get("/users/1")).andExpect(status().isNotFound());
  }
}
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)     // use the real engine via Testcontainers
class UserRepoTest { @Autowired UserRepository repo; }
@SpringBootTest(webEnvironment = RANDOM_PORT)
class AppIT { @Autowired TestRestTemplate rest; }
```

## Practices
- `@DataJpaTest` configures an embedded database if one is on the classpath; to test against a real database use `@AutoConfigureTestDatabase(replace = Replace.NONE)` (for example with Testcontainers).
- Contexts are cached by configuration; avoid different `@MockitoBean`/properties per class that multiply contexts (gated: unconfirmed, source is paywalled or blocked).
- A `@Transactional` test with `RANDOM_PORT` or `DEFINED_PORT` does not roll back server-side work: client and server run in separate threads and transactions.
- Security tests: see the Spring Security testing docs for `@WithMockUser` and CSRF helpers (gated: unconfirmed, source is paywalled or blocked).

## Verify
Suite time stays low; the slice test fails when the controller mapping changes, and does not need a database to start.

## Checked

2026-11-02. Checked against the Spring Boot reference, Testing Spring Boot Applications. Confirmed: `@SpringBootTest` RANDOM_PORT, `@WebMvcTest` with `@MockitoBean` (a Spring Framework annotation), `@DataJpaTest` entity scan, embedded DB, transactional behaviour, `@AutoConfigureTestDatabase(replace = Replace.NONE)`, `@JsonTest`, and the RANDOM_PORT/transaction caveat. Fixed: `replace = NONE` to `Replace.NONE`, the @Transactional advice made precise. Gated: context caching, `@RestClientTest`, spring-security-test details (other docs). The table row text for `@WebMvcTest` follows the page's controller-focused description.

Method: documentation only; no commands were run.
