---
id: computing-software.web-development.micronaut.micronaut-import-classes-and-mixins
name: micronaut-import-classes-and-mixins
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, class-import, mixin, bean-import, external-libraries, annotations]
level: advanced
status: docs-checked
description: "Use @Import, @ClassImport and @Mixin to make beans of compiled libraries, add Micronaut annotations to classes you cannot edit, and filter copied annotations."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/beanImport.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/classImport.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/mixin.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use classes from compiled libraries as beans, or add annotations to them, when you cannot edit the source. All three features are Java-only.

## @Import: JSR-330 libraries

```java
@Import(
        packages = {
                "org.atinject.tck.auto",
                "org.atinject.tck.auto.accessories"},
        annotated = "*")
public class Application {
}
```

- `packages` are not recursed, so list sub-packages explicitly.
- By default only classes with a scope or qualifier are imported; `annotated = "*"` makes every type a bean.
- Prefer it in applications. If two libraries import the same beans you will likely get `NonUniqueBeanException`.

## @ClassImport: process compiled classes as source

The annotation processors run on the imported classes, generating the needed metadata. `annotate` adds an annotation to every class in the packages:

```java
@ClassImport(
        packages = {
                "org.atinject.tck.auto",
                "org.atinject.tck.auto.accessories"},
        annotate = Bean.class)
public class Application {
}
```

It also prepares libraries for other modules, e.g. `@ClassImport(packages = "my.external.library", annotate = Serdeable.class)`. Classes already processed by the Micronaut annotation processor cannot be re-imported.

## @Mixin: patch annotations

A mixin copies its own annotations, and those of matching constructor, field and method members (same name and matching parameters), onto the referenced class:

```java
@Mixin(my.external.library.MyBean.class)
@Introspected(accessKind = Introspected.AccessKind.FIELD)
class MyBeanMixin {
    @JsonProperty("hello")
    String name;   // field name must match the original
}
```

Fix an unannotated library class (the TCK `FuelTank`) so it becomes a bean:

```java
@Mixin(FuelTank.class)
@Bean
class FuelTankMixin {
}

@ClassImport(packages = {"org.atinject.tck.auto", "org.atinject.tck.auto.accessories"})
class BeanImportTest {
}
```

## Filtering

- `includeAnnotations` limits copying to the listed annotations or packages; `excludeAnnotation` copies everything else.
- `@Mixin.Filter` sets rules for one constructor, method, field or parameter, and can remove annotations from the original:

```java
@Executable
@JsonProperty("hello")
@Mixin.Filter(removeAnnotations = "jakarta.validation")
public String getXyz() {
    return name;
}
```

This removes every annotation whose full name starts with `jakarta.validation` from that method.

Mixins change only Micronaut's annotation metadata model; the original classes are not modified.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
