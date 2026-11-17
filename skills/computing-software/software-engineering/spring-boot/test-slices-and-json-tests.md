---
id: computing-software.software-engineering.spring-boot.test-slices-and-json-tests
name: test-slices-and-json-tests
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, testing, test-slices, jsontest, jacksontester, autoconfigure, excludeautoconfiguration]
level: practitioner
status: docs-checked
description: "How Spring Boot test slices work, excluding auto-configuration, combining slices, and @JsonTest with JacksonTester, GsonTester, JsonbTester and BasicJsonTester."
sources:
  - https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Slices load only the configuration needed to test part of the application (for example controller URL mapping without database calls, or JPA entities without the web layer). With `spring-boot-test-autoconfigure` the test modules provide `@...Test` annotations that load the `ApplicationContext` and `@AutoConfigure...` annotations that adjust auto-configuration. Each slice restricts component scanning and loads a very restricted set of auto-configuration classes. To exclude one use the `excludeAutoConfiguration` attribute of most `@...Test` annotations, or `@ImportAutoConfiguration#exclude`. Multiple `@...Test` slices in one test are not supported: pick one and add the other slices' `@AutoConfigure...` annotations by hand. `@AutoConfigure...` annotations also work with plain `@SpringBootTest`.

`@JsonTest` (from `spring-boot-test-autoconfigure`) auto-configures the available JSON mapper: Jackson `JsonMapper` with `@JacksonComponent` beans and `JacksonModule`s; deprecated Jackson 2 `ObjectMapper` with `@JsonComponent` and `Module`s; `Gson`; or `Jsonb`. The auto-configurations it enables are listed in the appendix; to configure elements of the auto-configuration use `@AutoConfigureJsonTesters`.

AssertJ-based helpers work with JSONAssert and JsonPath: `JacksonTester`, `GsonTester`, `JsonbTester`, and `BasicJsonTester` (Strings). Fields of these types on the test class can be `@Autowired` under `@JsonTest`. Outside `@JsonTest` (plain unit tests) call the helper's `initFields` in a `@BeforeEach` method.

## Checked

2026-11-07. Read testing/spring-boot-applications.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Two sentences reworded to match the page (slice and JSON tester wording). The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
