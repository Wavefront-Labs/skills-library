---
id: computing-software.software-engineering.spring-boot.configurationproperties-binding-styles
name: configurationproperties-binding-styles
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, configurationproperties, javabean-binding, constructor-binding, defaultvalue, records, type-safe-configuration]
level: practitioner
status: docs-checked
description: "Bind properties to @ConfigurationProperties classes by JavaBean setters or constructors, with @DefaultValue, @ConstructorBinding, @Name and records."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type-safe `@ConfigurationProperties` classes replace scattered `@Value("${property}")` injection.

JavaBean binding relies on a default empty constructor plus getters and setters (standard Java Beans property descriptors). A setter may be omitted for pre-initialized mutable Maps/Collections and pre-initialized nested POJOs; the binder needs a setter to create a nested object itself. With Lombok, make sure it generates no special constructor. Static properties are not bound.

Constructor binding gives an immutable class:
- a single parameterized constructor implies constructor binding; with several constructors mark one with `@ConstructorBinding`;
- opt out by annotating the constructor `@Autowired` or making it `private` (Kotlin: empty primary constructor);
- records work, and need `@ConstructorBinding` only with multiple constructors;
- nested members are also bound through their constructor;
- the class must be enabled via `@EnableConfigurationProperties` or configuration property scanning, not as a `@Component`, `@Bean` or `@Import` bean;
- compile with `-parameters` (automatic with the Spring Boot Gradle plugin or Maven with `spring-boot-starter-parent`);
- `Optional` is not recommended; an unset constructor-bound `Optional` binds empty.

`@DefaultValue` on constructor parameters or record components supplies defaults (placeholders resolved, conversion applied). If `my.service.security.username=admin` is set but `roles` is not, `@DefaultValue("USER")` binds `List.of("USER")`. If no `security` property exists, the nested instance is `null`; define it empty (`security: {}` in YAML, `my.service.security=` in properties) to get a fully defaulted instance, or put an empty `@DefaultValue` on the parameter to always get a non-null one.

Reserved words (for example `my.service.import`) need `@Name` on the field or constructor parameter.

Defaults inside the class are not reflected in the Environment, so `@Value("${my.service.enabled}")` fails unless you supply a default.

## Checked

2026-11-07

Read the Type-safe Configuration Properties, JavaBean Properties Binding, Constructor Binding, @DefaultValue and Binding and Default Values sections of external-config.adoc (docs-repo source of the cited Externalized Configuration page). The include-code examples (MyProperties variants, primaryconstructor, nonnull) were not opened; claims rest on the page prose and its listed bound values.
Confirmed: @Value cumbersomeness intro; default empty constructor plus getters/setters via Java Beans property descriptors; setter omission for pre-initialized mutable Maps/Collections and nested POJOs, setter needed for on-the-fly creation; Lombok warning; static properties unsupported; single parameterized constructor implies constructor binding, @ConstructorBinding for several constructors; opt-out via @Autowired or private (Kotlin empty primary constructor); records; nested constructor binding; must be enabled by @EnableConfigurationProperties or scanning, not Component/Bean/Import beans; -parameters with Gradle plugin or spring-boot-starter-parent; Optional not recommended and binds empty; reserved word my.service.import with @Name on field and on constructor parameter; @DefaultValue placeholders and conversion, the admin / USER example, null Security when absent, security: {} and my.service.security= for a defaulted instance, empty @DefaultValue for non-null; defaults not in the Environment so @Value("${my.service.enabled}") needs a default.
Nothing trimmed.

Method: documentation only; no commands were run.
