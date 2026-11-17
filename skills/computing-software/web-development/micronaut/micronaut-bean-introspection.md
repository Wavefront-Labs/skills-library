---
id: computing-software.web-development.micronaut.micronaut-bean-introspection
name: micronaut-bean-introspection
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, bean-introspection, introspected, beanwrapper, creator, reflection-free]
level: practitioner
status: docs-checked
description: "Generate compile-time bean introspections with @Introspected, then instantiate, read and write properties, choose constructors and use builders without reflection."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/makingABeanAvailableForIntrospection.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/atIntrospected.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectedAnnotationOnAConfigurationClass.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/beanWrapperApi.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/accessKind.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/atCreator.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/staticAtCreator.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectionBuilders.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectionIncludeInjected.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectionConstructors.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectionEnums.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/introspectedAccessorsStyle.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/introspection/kotlinAndBeanIntrospection.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a compile-time replacement for the JDK `Introspector`, with no reflection or cached reflective metadata.

## Setup

Classes are not introspectable automatically. Enable the annotation processor (`micronaut-inject-java` as `annotationProcessor`; Kotlin uses `kapt`; Groovy uses `micronaut-inject-groovy` in `compileOnly`) and have a runtime dependency on `micronaut-core`.

## Make a class introspectable

```java
@Introspected
public class Person {
    private String name;
    private int age = 18;
    public Person(String name) { this.name = name; }
    // getters and setters
}
```

Alternatives: a configuration class for already-compiled types, `@Introspected(classes = Person.class) public class PersonConfiguration {}`; a `package-info` annotated `@Introspected` (Java/Groovy only, direct classes only, package must contain only introspectable classes); the experimental `packages` member.

## Use it

```java
BeanIntrospection<Person> introspection = BeanIntrospection.getIntrospection(Person.class);
Person person = introspection.instantiate("John");
BeanProperty<Person, String> property = introspection.getRequiredProperty("name", String.class);
property.set(person, "Fred");
String name = property.get(person);
```

`BeanProperty` does no type conversion: values must match the property type or an exception occurs. For conversion use `BeanWrapper`:

```java
BeanWrapper<Person> wrapper = BeanWrapper.getWrapper(new Person("Fred"));
wrapper.setProperty("age", "20");
int newAge = wrapper.getRequiredProperty("age", int.class);
```

It throws `ConversionErrorException` when conversion fails; `getRequiredProperty` throws `IntrospectionException` for a missing property.

## Fields

`@Introspected(accessKind = Introspected.AccessKind.FIELD)` treats public or package-protected fields as properties (final = read-only). The array form lets you prefer one kind by order. Not possible in Kotlin or Python.

## Choosing the constructor

- Multiple constructors: mark one `@Creator`. With no default constructor, `instantiate()` without arguments throws `InstantiationException`.
- Static factory: put `@Creator` on a static method (`public static Business forName(String name)`). With several, a no-arg one is the default and the first with arguments is primary.
- `@Introspected(constructors = true)` describes every constructor (`introspection.getConstructors()`, each a `BeanConstructor` with `instantiate(...)`); `@Executable` on one constructor describes just that one. Neither changes how beans are built.

## Builders and others

- `@Introspected(builder = @Introspected.IntrospectionBuilder(builderClass = Person.Builder.class))` lets `introspection.builder().with("age", 25).with("name", "Fred").build()` construct it (not compatible with Groovy `@Builder`). `builder()` works for any type but is slower than `instantiate()`; check `hasBuilder()`.
- Enums can be introspected and built via `valueOf`.
- `@Introspected(includeInjected = true)` keeps `@Inject`, `@Value` and `@Property` points as bean properties, to populate instances not created by the context. `@PostConstruct`/`@PreDestroy` methods are never properties.
- Combine with `@AccessorsStyle(readPrefixes = "", writePrefixes = "")` for fluent accessors.
- Kotlin: data classes may be `@Introspected`; inline value classes are not yet supported.

## Checked
2026-11-07. Checked against the introspection pages. Added the constructors, enums, accessor-style and Kotlin pages to sources.

Method: documentation only; no commands were run.
