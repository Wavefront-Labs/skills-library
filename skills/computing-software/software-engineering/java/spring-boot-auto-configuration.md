---
id: computing-software.software-engineering.java.spring-boot-auto-configuration
name: spring-boot-auto-configuration
category: computing-software
field: software-engineering
product: java
tags: [java, auto-configuration, conditionalonproperty, conditionalonmissingbean, spring-boot-starter, condition-evaluation-report, spring-boot, spring-boot-core]
level: advanced
status: docs-checked
description: "Understand and write Spring Boot auto-configuration: conditions, the AutoConfiguration.imports file, backing off with ConditionalOnMissingBean, and the conditions report."
sources: ["https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html", "https://docs.spring.io/spring-boot/reference/using/auto-configuration.html", "https://docs.spring.io/spring-boot/api/java/org/springframework/boot/autoconfigure/condition/package-summary.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Spring Boot auto-configuration

**Goal:** know why a bean exists (or doesn't), override defaults cleanly, and package
your own shared configuration as a starter.

## How it works
Boot loads classes listed in
`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` from every
jar. Each is an `@AutoConfiguration` class guarded by conditions; they back off when you define
your own bean.

## Seeing what happened
```bash
java -jar app.jar --debug          # CONDITIONS EVALUATION REPORT: positive/negative matches with reasons
```
or the Actuator `conditions` endpoint. Typical answer: "DataSourceAutoConfiguration matched: found class
HikariDataSource" or "did not match: @ConditionalOnMissingBean found bean 'dataSource'".

## Overriding defaults
1. Properties first (`spring.datasource.hikari.maximum-pool-size`).
2. Define your own bean of the type: most auto-configs use `@ConditionalOnMissingBean`.
3. Customizer beans when available (in Boot 4: `RestClientCustomizer`, `WebClientCustomizer`, `JsonMapperBuilderCustomizer`) -
   keep Boot's defaults and tweak.
4. Exclude: `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)` or
   `spring.autoconfigure.exclude=...`.

## Writing an auto-configuration (internal starter)
```java
@AutoConfiguration(after = WebMvcAutoConfiguration.class)   // before/after/beforeName/afterName order auto-configs
@ConditionalOnClass(AuditClient.class)
@ConditionalOnProperty(prefix = "acme.audit", name = "enabled", havingValue = "true", matchIfMissing = true)
@EnableConfigurationProperties(AuditProperties.class)
public class AuditAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    AuditClient auditClient(AuditProperties props) {
        return new AuditClient(props.endpoint());
    }
}
```
Register it:
```
# src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.acme.audit.autoconfigure.AuditAutoConfiguration
```
Boot looks for that `.imports` file in every published jar.

Conventions (from the Boot docs): an `acme-spring-boot` module with the auto-configuration code and an
`acme-spring-boot-starter` module that only brings in dependencies. Keep auto-configuration classes out of component scanning and do not let them enable it. Use
`@ConditionalOnBean` / `@ConditionalOnMissingBean` only on auto-configuration classes, which are processed after user bean definitions.

## Testing
```java
new ApplicationContextRunner()
    .withConfiguration(AutoConfigurations.of(AuditAutoConfiguration.class))
    .withPropertyValues("acme.audit.enabled=false")
    .run(ctx -> assertThat(ctx).doesNotHaveBean(AuditClient.class));
```
Fast, no full app, covers each condition.

## Verify
- [ ] Each condition has an ApplicationContextRunner test (on, off, user-override).
- [ ] `--debug` report explains every surprising bean in the app.

## Checked

Date: 2026-10-25. Documentation release: Spring Boot 4.1.2 and Spring Framework 7.0.10 (GitHub main documentation sources; releases of 2026-10-22).

Confirmed: the `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` file; `before`/`beforeName`/`after`/`afterName` on `@AutoConfiguration`; `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` with `havingValue` and `matchIfMissing`; `--debug` conditions report; `spring.autoconfigure.exclude`; Actuator `conditions` endpoint; `ApplicationContextRunner`; `AutoConfigurations` class; starter module naming; Boot 4 customizer interfaces (`RestClientCustomizer`, `WebClientCustomizer`, `JsonMapperBuilderCustomizer`).

Removed as unconfirmed: the `Jackson2ObjectMapperBuilderCustomizer` and `ObjectMapper` references (Boot 4 uses Jackson 3 `JsonMapper`), the `/actuator/conditions` URL form and the `spring.factories` removal remark (not in the current docs).

Method: documentation only; no commands were run.
