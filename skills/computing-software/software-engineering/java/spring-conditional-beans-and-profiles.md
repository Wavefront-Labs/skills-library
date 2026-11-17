---
id: computing-software.software-engineering.java.spring-conditional-beans-and-profiles
name: spring-conditional-beans-and-profiles
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot-core, conditional-beans, conditionalonproperty, conditionalonmissingbean, profile, spring-profiles]
level: practitioner
status: docs-checked
description: "Register Spring beans conditionally with @Profile, @ConditionalOnProperty, @ConditionalOnMissingBean and related conditions; ordering rules."
sources: ["https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html#features.developing-auto-configuration.condition-annotations", "https://docs.spring.io/spring-framework/reference/core/beans/environment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional beans and profiles

```java
@Configuration
class StorageConfig {
    @Bean @ConditionalOnProperty(name = "storage.type", havingValue = "s3")
    BlobStore s3() { return new S3Store(); }

    @Bean @ConditionalOnMissingBean(BlobStore.class)       // fallback when nothing else defined
    BlobStore local() { return new LocalStore(); }

    @Bean @Profile("!prod") DataSeeder seeder() { return new DataSeeder(); }
}
```
Common conditions in Spring Boot:
- `@ConditionalOnClass` and `@ConditionalOnMissingClass`: include configuration based on class presence.
- `@ConditionalOnBean` and `@ConditionalOnMissingBean`: `value` selects beans by type, `name` by name, `search` limits the context hierarchy searched. On a `@Bean` method the target type defaults to the return type.
- `@ConditionalOnProperty`: a property that exists and is not `false` matches by default; refine with `havingValue` and `matchIfMissing`; with several names all must pass.
- `@ConditionalOnWebApplication` and `@ConditionalOnNotWebApplication`, `@ConditionalOnResource`, and `@ConditionalOnExpression` (SpEL).

Profile expressions can combine names with operators such as `&` and `!`, for example `"prod & !eu"`.

## Gotchas
- `@ConditionalOnBean` and `@ConditionalOnMissingBean` are evaluated against what has been processed so far, so Spring Boot recommends them only on auto-configuration classes, which load after user-defined bean definitions.
- `@ConditionalOnClass` on a `@Bean` method does not work like on a class: the JVM loads the return type before the condition applies and fails if the class is absent. Put it on the configuration class.
- Referencing a bean inside a `@ConditionalOnExpression` expression initializes that bean very early in context refresh.
- When `@ConditionalOnClass` is part of a composed (meta) annotation, use the `name` attribute, not `value`.

## Checked

Method: docs-checked 2026-11-09 against the Spring Boot developing-auto-configuration page (condition annotations: class, bean, property, resource, web application, SpEL) and the Spring Framework environment abstraction page (@Profile, profile expressions). Dropped unconfirmed claims (ConditionalOnCloudPlatform, spring.profiles.group, custom Condition API, debug report, ApplicationContextRunner, advice on profiles versus properties).
