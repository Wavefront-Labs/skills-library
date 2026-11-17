---
id: computing-software.software-engineering.spring-boot.configurationproperties-validation
name: configurationproperties-validation
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, validated, jsr-303, jakarta-validation, configurationproperties, value-annotation, spel]
level: practitioner
status: docs-checked
description: "Validate @ConfigurationProperties with @Validated and jakarta.validation, cascade with @Valid, add a custom validator, and compare with @Value."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot validates `@ConfigurationProperties` classes annotated with Spring's `@Validated`. Put JSR-303 `jakarta.validation` constraint annotations on fields, with a compliant implementation on the classpath. You can alternatively annotate the `@Bean` method that creates the properties with `@Validated`.

To cascade into nested properties, annotate the nested field with `@Valid`.

Custom validator: define a bean named `configurationPropertiesValidator` implementing Spring's `Validator`. Declare its `@Bean` method `static`: it is created very early, and static lets it be created without instantiating the `@Configuration` class, avoiding early-instantiation problems.

Check values at runtime on `/actuator/configprops` (or the JMX equivalent).

`@ConfigurationProperties` versus `@Value`:

| Feature | @ConfigurationProperties | @Value |
|---|---|---|
| Relaxed binding | Yes | Limited |
| Metadata support | Yes | No |
| SpEL evaluation | No | Yes |

For `@Value`, use canonical kebab-case names: `@Value("${demo.item-price}")` picks up `demo.item-price`, `demo.itemPrice` and `DEMO_ITEMPRICE`; `${demo.itemPrice}` does not pick up `demo.item-price`.

For your own sets of keys, group them in a `@ConfigurationProperties` POJO. SpEL in property files is not evaluated when files are parsed, but is evaluated when the value is consumed through `@Value`.

## Checked

2026-11-07

Read the @ConfigurationProperties Validation and @ConfigurationProperties vs. @Value sections of external-config.adoc (docs-repo source of the cited Externalized Configuration page). The include-code examples (MyProperties, nested/MyProperties) were not opened; claims rest on page prose.
Confirmed: validation when annotated with Spring's @Validated, jakarta.validation JSR-303 constraints with a compliant implementation on the classpath; @Validated on the @Bean method as an alternative; @Valid for cascading to nested properties; configurationPropertiesValidator bean with static @Bean method and the early-instantiation reason; /actuator/configprops or JMX equivalent; the feature table (relaxed binding Yes/Limited, metadata Yes/No, SpEL No/Yes); kebab-case guidance with the demo.item-price / demo.itemPrice / DEMO_ITEMPRICE example; POJO grouping advice; SpEL in property files not evaluated at parse time but evaluated when consumed through @Value.
Nothing trimmed.

Method: documentation only; no commands were run.
