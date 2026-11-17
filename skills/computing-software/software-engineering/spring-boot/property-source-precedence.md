---
id: computing-software.software-engineering.spring-boot.property-source-precedence
name: property-source-precedence
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, externalized-configuration, property-source, precedence, override, environment]
level: practitioner
status: docs-checked
description: "Spring Boot property source order from default properties to command line and test sources, with later sources overriding earlier ones, plus config data file order."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spring Boot uses a fixed PropertySource order so values can be overridden sensibly. Later sources override earlier ones.

Order (lowest to highest):
1. Default properties (`SpringApplication.setDefaultProperties`)
2. `@PropertySource` on `@Configuration` classes (added to the Environment only at context refresh, too late for `logging.*` and `spring.main.*`)
3. Config data such as `application.properties`
4. `random.*` (RandomValuePropertySource)
5. OS environment variables
6. Java system properties
7. JNDI `java:comp/env`
8. ServletContext init parameters
9. ServletConfig init parameters
10. `SPRING_APPLICATION_JSON`
11. Command line arguments
12. `properties` attribute on tests (`@SpringBootTest` and slice annotations)
13. `@DynamicPropertySource`
14. `@TestPropertySource`
15. Devtools global settings properties when devtools is active

Config data files, in order: packaged `application.*`, packaged `application-{profile}.*`, external `application.*`, external `application-{profile}.*`.

Notes from the page:
- Stick to one format; if `.properties` and YAML sit in the same location, `.properties` wins.
- Environment variables cannot contain periods on most operating systems, so use underscores (`SPRING_CONFIG_NAME` for `spring.config.name`).
- One-off override: `java -jar app.jar --name="Spring"`.
- To find out why a property has a value, use the `env` and `configprops` actuator endpoints.

## Checked

2026-11-07. Read features/external-config.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
