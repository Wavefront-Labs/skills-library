---
id: computing-software.software-engineering.spring-boot.springboottest-web-environments-and-configuration
name: springboottest-web-environments-and-configuration
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, testing, springboottest, webenvironment, testconfiguration, usemainmethod, random-port]
level: practitioner
status: docs-checked
description: "@SpringBootTest webEnvironment modes, web app type detection, finding and excluding test configuration, @TestConfiguration, useMainMethod, arguments and JMX."
sources:
  - https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@SpringBootTest` is an alternative to the standard spring-test `@ContextConfiguration` when you need Boot features; it creates the context through `SpringApplication` (external properties, logging and other Boot features are installed in the context by default only if `SpringApplication` creates it). JUnit 4 needs `@RunWith(SpringRunner.class)`; with JUnit 6 `@ExtendWith(SpringExtension.class)` is not needed.

`webEnvironment`:
- `MOCK` (default): web `ApplicationContext` with a mock web environment, no embedded server; falls back to a non-web context if no web environment is on the classpath.
- `RANDOM_PORT`: `WebServerApplicationContext`, real server on a random port (also starts the management server on a separate random port if one is configured).
- `DEFINED_PORT`: real server on the configured port or `8080`.
- `NONE`: `SpringApplication`-created context, no web environment.

A `@Transactional` test rolls back by default, but with `RANDOM_PORT` or `DEFINED_PORT` client and server run in separate threads and transactions, so server transactions do not roll back.

Web type: MVC if available; WebFlux if only WebFlux; if both are present MVC wins, so set `spring.main.web-application-type` to test a reactive app.

Configuration detection: `@*Test` annotations search upwards from the test's package for a class annotated `@SpringBootApplication` or `@SpringBootConfiguration`. A nested `@TestConfiguration` adds to the primary configuration; a nested `@Configuration` replaces it. With slice tests avoid area-specific settings on the main application class; an explicit `@ComponentScan` on it disables the slicing exclude filters, so redefine them. Spring caches contexts between tests with identical configuration.

Excluding: a top-level `@TestConfiguration` class is not picked up by scanning; import it explicitly where needed. Direct `@ComponentScan` use needs `TypeExcludeFilter` registered. Imported `@TestConfiguration` is processed before an inner-class one and before scanned configuration.

Main method: by default `@SpringBootTest` does not call `main`; set `useMainMethod` to `UseMainMethod.ALWAYS` (fails if no main) or `WHEN_AVAILABLE` (use `main` if one is available, otherwise standard loading) so customizations made in `main` apply; for example, additional profiles set there are active when the context starts.

Arguments: pass them with the `args` attribute.

JMX: disabled in tests because contexts are cached; if a test needs an `MBeanServer`, mark the context dirty.

## Checked

2026-11-07. Read testing/spring-boot-applications.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Two sentences reworded to match the page (web environment and configuration-detection wording). The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
