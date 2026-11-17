---
id: computing-software.software-engineering.java.writing-a-custom-spring-boot-starter
name: writing-a-custom-spring-boot-starter
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot-core, custom-starter, auto-configuration, configuration-properties, autoconfiguration-imports]
level: advanced
status: docs-checked
description: "Package a reusable Spring Boot starter: autoconfigure module, @AutoConfiguration, AutoConfiguration.imports file, properties metadata and ApplicationContextRunner tests."
sources: ["https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html", "https://docs.spring.io/spring-boot/specification/configuration-metadata/annotation-processor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Spring Boot starter

Layout: an autoconfigure module (code) plus a starter module that depends on it and the library. The two-module split is not required: if the auto-configuration is simple and has no optional features, merging them into the starter is an option; separate them when the library has optional features or you want a starter that expresses an opinion about optional dependencies.

```java
@ConfigurationProperties("acme.client")
public record AcmeProperties(URI baseUrl, Duration timeout) {}

@AutoConfiguration
@ConditionalOnClass(AcmeClient.class)
@EnableConfigurationProperties(AcmeProperties.class)
public class AcmeAutoConfiguration {
    @Bean @ConditionalOnMissingBean
    AcmeClient acmeClient(AcmeProperties p) { return new AcmeClient(p.baseUrl(), p.timeout()); }
}
```
Spring Boot looks for `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` in your published jar; list your auto-configuration classes there, one class name per line. Add `spring-boot-configuration-processor` as an annotation processor to generate `spring-configuration-metadata.json` for IDE completion.

## Rules
- Auto-configurations must be loaded only by being named in the imports file; define them in a specific package space, never as component-scan targets, and do not enable component scanning inside them. Use specific `@Import` annotations instead.
- Annotate beans `@ConditionalOnMissingBean` so applications can override them.
- Guard code that refers to optional classes with `@ConditionalOnClass`; condition-evaluation order matters for `@ConditionalOnBean` and `@ConditionalOnMissingBean`, which are safe on auto-configuration classes because those load after user bean definitions.

## Verify
```java
new ApplicationContextRunner().withConfiguration(AutoConfigurations.of(AcmeAutoConfiguration.class))
  .withPropertyValues("acme.client.timeout=2s").run(ctx -> assertThat(ctx).hasSingleBean(AcmeClient.class));
```
Test the negative case too: the bean is absent when the user defines their own.

## Checked

Method: docs-checked 2026-11-09 against the Spring Boot developing-auto-configuration page (imports file, component scanning warning, conditions, ApplicationContextRunner, module split guidance) and the configuration metadata annotation processor page. Dropped unconfirmed claims (Boot 2.7 history and spring.factories, property prefix advice, after/before ordering, @DefaultValue usage).
