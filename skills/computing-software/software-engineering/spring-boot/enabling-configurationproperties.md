---
id: computing-software.software-engineering.spring-boot.enabling-configurationproperties
name: enabling-configurationproperties
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, enableconfigurationproperties, configurationpropertiesscan, third-party-configuration, bean-name, configurationproperties]
level: practitioner
status: docs-checked
description: "Register @ConfigurationProperties types with @EnableConfigurationProperties or @ConfigurationPropertiesScan, bind third-party beans, and know the bean naming rule."
sources:
  - https://docs.spring.io/spring-boot/reference/features/external-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spring Boot can bind `@ConfigurationProperties` types and register them as beans in two ways.

1. `@EnableConfigurationProperties(SomeProperties.class)` on any `@Configuration` class. Use it when scanning is unsuitable, for example in your own auto-configuration or for conditional enabling.
2. `@ConfigurationPropertiesScan`, typically on the main `@SpringBootApplication` class (any `@Configuration` class works). Scanning starts at the package of the declaring class; pass specific packages to narrow it.

Bean name: `<prefix>-<fqn>`, where prefix is the annotation's environment key prefix and fqn the fully qualified class name. With no prefix only the fqn is used. `SomeProperties` in `com.example.app` with prefix `some.properties` is named `some.properties-com.example.app.SomeProperties`.

Inject the properties bean like any other bean. Recommended: keep these classes dealing only with the environment and do not inject other beans. For corner cases use setter injection or `*Aware` interfaces such as `EnvironmentAware`. To inject beans through the constructor, annotate the class `@Component` and use JavaBean-style binding.

Third-party components: put `@ConfigurationProperties` on a public `@Bean` method. Any JavaBean property under the given prefix (for example `another`) is mapped onto the returned bean.

Using `@ConfigurationProperties` also lets you generate configuration metadata that IDEs use for auto-completion of your keys.

Inspect bound values at runtime with the `configprops` actuator endpoint.

## Checked

2026-11-07

Read the Enabling @ConfigurationProperties-annotated Types, Using @ConfigurationProperties-annotated Types and Third-party Configuration sections of external-config.adoc (docs-repo source of the cited Externalized Configuration page). The include-code examples (MyConfiguration, SomeProperties, MyApplication, ThirdPartyConfiguration, MyService) were not opened; claims rest on page prose.
Confirmed: class-by-class versus scanning; @EnableConfigurationProperties on any @Configuration class for unsuitable-for-scanning cases (own auto-configuration, conditional enabling); @ConfigurationPropertiesScan usually on the @SpringBootApplication class, any @Configuration works, scanning from the declaring package with an option to name packages; bean name <prefix>-<fqn>, fqn only when no prefix, and the some.properties-com.example.app.SomeProperties example; environment-only recommendation, setter injection and *Aware interfaces, @Component plus JavaBean binding to inject beans via constructor; public @Bean method for third-party components with the another prefix; metadata generation for IDE completion; env and configprops endpoints TIP.
Nothing trimmed.

Method: documentation only; no commands were run.
