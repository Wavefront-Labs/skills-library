---
id: computing-software.software-engineering.java.spring-configuration-properties-and-profiles
name: spring-configuration-properties-and-profiles
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, configurationproperties, spring-profiles, externalized-configuration]
level: practitioner
status: gated
description: "Bind typed configuration with Spring Boot @ConfigurationProperties, validate it, and manage environment differences with profiles, config import and relaxed binding."
sources: ["https://docs.spring.io/spring-boot/reference/features/external-config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Boot configuration properties and profiles

## Typed properties
```java
@ConfigurationProperties(prefix = "app.mail")
@Validated
public record MailProps(@NotBlank String host, @Min(1) int port, Duration timeout) {}
```
Enable with `@ConfigurationPropertiesScan` or `@EnableConfigurationProperties`. Records and constructor binding give immutable config. Add the configuration processor for IDE metadata (artifact name: check the Spring Boot docs) (gated: unconfirmed, source is paywalled or blocked). Invalid values fail startup, which is desired.

## Sources and order (highest wins, simplified)
command-line args > `SPRING_APPLICATION_JSON` > JNDI/Java system properties > OS environment variables > config data files (profile-specific files outside the jar > `application.yml` outside the jar > profile-specific inside the jar > `application.yml` inside the jar) > `@PropertySource` > defaults. Profile-specific files override non-specific ones, and with several profiles the last wins. Check the reference page for the full list. Relaxed binding: a property like `my.service[0].other` maps to env `MY_SERVICE_0_OTHER`, so `app.mail.host` is `APP_MAIL_HOST`. Containers set config with env vars or mounted files via `spring.config.import=optional:configtree:/etc/config/`.

## Profiles
- Activate with the `spring.profiles.active` property: `--spring.profiles.active=prod`, or as env var `SPRING_PROFILES_ACTIVE=prod` (standard relaxed mapping).
- Profile files: `application-prod.yml`. In one multi-document YAML use `spring.config.activate.on-profile: prod`.
- Profile groups (`spring.profiles.group.prod=prod-db,metrics`) and `@Profile("dev")` on beans: see the profiles docs (gated: unconfirmed, source is paywalled or blocked).
- Never commit secrets: import from a secret store or env.

## Pitfalls
- `Duration` accepts a plain number (milliseconds by default, overridable with `@DurationUnit`), ISO-8601, or simple formats such as `10s`. Lists in env vars use indexed names (`MY_SERVICE_0_OTHER`).
- `@Value` bypasses relaxed binding and validation; prefer `@ConfigurationProperties`.
- Too many profiles hide config drift; keep prod differences small and tested.

## Verify
The Actuator `configprops` and `env` endpoints (secured) (gated: unconfirmed, source is paywalled or blocked) show bound values and their source; a missing required property stops the app at start.

## Checked

2026-11-02. Checked against the Spring Boot reference, Externalized Configuration. Confirmed: property source order (command line, SPRING_APPLICATION_JSON, JNDI, system properties, OS env vars, config data files in packaged/external order, profile-specific overriding, last profile wins), `spring.config.import=optional:configtree:/etc/config/`, `spring.config.activate.on-profile`, `@ConfigurationPropertiesScan`, relaxed binding and indexed env names, Duration formats. Fixed: the simplified order which omitted system properties/JNDI and the inside/outside jar split. Gated: profile groups, @Profile, actuator endpoints, configuration processor artifact name, which are on other pages.

Method: documentation only; no commands were run.
