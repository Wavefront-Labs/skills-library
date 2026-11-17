---
id: computing-software.software-engineering.spring-boot.springapplication-customization
name: springapplication-customization
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, springapplication, springapplicationbuilder, webapplicationtype, applicationarguments, context-hierarchy]
level: practitioner
status: docs-checked
description: "Customize a local SpringApplication, build parent/child contexts with SpringApplicationBuilder, set the web application type and read application arguments."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default bootstrap: `SpringApplication.run(MyApplication.class, args)` from `main()`. If defaults do not suit, create a local `SpringApplication` instance and customize it (for example to turn off the banner). Constructor arguments are configuration sources for beans, usually `@Configuration` classes but possibly `@Component` classes. Settings can also come from `application.properties`.

Fluent builder: `SpringApplicationBuilder` chains calls and has `parent` and `child` methods for an ApplicationContext hierarchy. Restrictions: web components must be in the child context, and parent and child share the same Environment.

Web environment: `SpringApplication` picks the `WebApplicationType`:
- Spring MVC present: `AnnotationConfigServletWebServerApplicationContext`
- else WebFlux present: `AnnotationConfigReactiveWebServerApplicationContext`
- otherwise `AnnotationConfigApplicationContext`

With MVC plus WebFlux's `WebClient` together, MVC is used. Override with `setWebApplicationType(WebApplicationType)`, or take full control with `setApplicationContextFactory(...)`. Calling `setWebApplicationType(WebApplicationType.NONE)` is often desirable in JUnit tests.

Application arguments: inject an `ApplicationArguments` bean for the raw `String[]` plus parsed option and non-option arguments. Boot also registers a `CommandLinePropertySource`, so single arguments can be injected with `@Value`.

Admin features: set `spring.application.admin.enabled` to expose `SpringApplicationAdminMXBean` on the platform MBeanServer for remote administration or service wrappers. The HTTP port is available under the key `local.server.port`.

## Checked

2026-11-07. Read features/spring-application.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
