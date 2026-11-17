---
id: computing-software.software-engineering.spring-boot.springboottest-mock-and-running-server
name: springboottest-mock-and-running-server
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, testing, mockmvc, resttestclient, webtestclient, localserverport, mockitobean]
level: practitioner
status: docs-checked
description: "Test web endpoints with MockMvc, MockMvcTester, RestTestClient or WebTestClient in a mock environment or against a random-port server, and mock beans with @MockitoBean."
sources:
  - https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mock environment (default): the server is not started. For Spring MVC, available integrations: regular `MockMvc` (Hamcrest), `MockMvcTester` (wraps `MockMvc`, AssertJ), `RestTestClient` and `WebTestClient` with `MockMvc` plugged in as the server (`@AutoConfigureMockMvc`, `@AutoConfigureRestTestClient`, `@AutoConfigureWebTestClient`). For WebFlux endpoints use `WebTestClient`. To focus only on the web layer use `@WebMvcTest`.

Limit: mocking occurs at the Spring MVC layer, so code relying on lower-level servlet container behaviour cannot be tested with `MockMvc`; for example you can test that MVC throws and handles exceptions but not that a specific custom error page is rendered. Use a running server for that.

Running server: use `@SpringBootTest(webEnvironment=WebEnvironment.RANDOM_PORT)`. `@LocalServerPort` injects the actual port. Autowire a `RestTestClient` with `@AutoConfigureRestTestClient` (resolves relative links to the running server, with a response-verification API; AssertJ assertions via `RestTestClientResponse`). With `spring-webflux` on the classpath, `@AutoConfigureWebTestClient` gives a `WebTestClient`, which can also be used in a mock environment (from `spring-boot-webflux-test`). Certain sliced tests need `@AutoConfigureWebServer` to get an embedded server.

Customizing: register `RestTestClientBuilderCustomizer` or `WebTestClientBuilderCustomizer` beans; they receive the builder.

Mocking beans: Spring Framework's `@MockitoBean` defines a Mockito mock of a bean in the context, and `@MockitoSpyBean` a spy.

## Checked

2026-11-07. Read testing/spring-boot-applications.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
