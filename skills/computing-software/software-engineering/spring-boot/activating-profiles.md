---
id: computing-software.software-engineering.spring-boot.activating-profiles
name: activating-profiles
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, profiles, spring-profiles-active, spring-profiles-default, profile-annotation, setadditionalprofiles]
level: intro
status: docs-checked
description: "Mark beans with @Profile, activate profiles via spring.profiles.active or --spring.profiles.active, tune the default profile, and know profile name rules."
sources:
  - https://docs.spring.io/spring-boot/reference/features/profiles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Profiles segregate parts of the configuration for certain environments. Any `@Component`, `@Configuration` or `@ConfigurationProperties` can carry `@Profile` to limit when it loads. If `@ConfigurationProperties` beans are registered via `@EnableConfigurationProperties`, put `@Profile` on the `@Configuration` class that has that annotation; if they are scanned, put it on the properties class itself.

Activate with the `spring.profiles.active` property, in any way properties can be set:
```yaml
spring:
  profiles:
    active: "dev,hsqldb"
```
or on the command line: `--spring.profiles.active=dev,hsqldb`. It follows the usual property-source ordering, so a command-line switch *replaces* a value from `application.properties`.

With no active profile, the `default` profile is enabled. Rename it with `spring.profiles.default` (for example `"none"`).

Constraint: `spring.profiles.active` and `spring.profiles.default` work only in non-profile-specific documents. They cannot appear in profile-specific files or in documents activated by `spring.config.activate.on-profile`. In the page's example the second document, which has `on-profile: "prod"` plus `profiles.active: "metrics"`, is invalid.

Profile names may contain letters, numbers and `-`, `_`, `.`, `+`, `@`, and must start and end with a letter or number. Set `spring.profiles.validate` to `false` for more flexible names.

Programmatic activation: `SpringApplication.setAdditionalProfiles(...)` before running, or Spring's `ConfigurableEnvironment`.

The page says profile-specific variants of `application.properties` (or `application.yaml`) and of files referenced through `@ConfigurationProperties` are also loaded; the details are in the externalized-configuration page (see config-file-locations).

## Checked

2026-11-07

Read profiles.adoc (docs-repo source of the cited profiles page) in full: all sections, including "Programmatically Setting Profiles" and "Profile-specific Configuration Files". Also opened the included ProductionConfiguration.java example from the docs repo (a @Configuration class annotated @Profile("production")).
Confirmed: @Component/@Configuration/@ConfigurationProperties can carry @Profile; the @EnableConfigurationProperties vs scanning NOTE; `spring.profiles.active` example "dev,hsqldb" and `--spring.profiles.active=dev,hsqldb`; the `default` profile and `spring.profiles.default` ("none"); active/default only in non-profile-specific documents, with the `on-profile: "prod"` plus `active: "metrics"` document as the invalid example; command line replaces application.properties; profile name characters (`-`, `_`, `.`, `+`, `@`, start and end with letter or number) and `spring.profiles.validate: false`; `setAdditionalProfiles(...)` and ConfigurableEnvironment.
Trimmed: the `application-{profile}` filename pattern, which this page does not state (it points to the externalized-configuration page).

Method: documentation only; no commands were run.
