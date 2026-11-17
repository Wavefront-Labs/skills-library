---
id: computing-software.web-development.micronaut.micronaut-annotation-metadata
name: micronaut-annotation-metadata
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, annotation-metadata, stereotypes, aliasfor, inherited, retainable, meta-annotations]
level: advanced
status: docs-checked
description: "Read compile-time annotation metadata and stereotypes, build inheritable meta-annotations, alias members with @AliasFor and retain composed annotations."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/annotationMetadata.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: work with annotations and stereotypes (meta-annotations) without runtime reflection. Micronaut computes metadata at compile time; `BeanDefinition` implements `AnnotationMetadata`.

## Reading

```java
Collection<BeanDefinition> definitions =
    beanContext.getBeanDefinitions(Qualifiers.byStereotype(Controller.class));
for (BeanDefinition definition : definitions) {
    AnnotationValue<Controller> controllerAnn = definition.getAnnotation(Controller.class);
}
```

This finds beans with `@Controller` directly or via a stereotype. `getAnnotation*` returns `AnnotationValue`, not a Java annotation (cheaper). `definition.synthesize(Controller.class)` makes a runtime proxy; it needs reflection and memory, so use it only as a last resort (e.g. a third-party library needs an instance).

## Inheritance

Only annotations meta-annotated with `@Inherited` are inherited (declared ones come from `getDeclaredAnnotation*`). Micronaut extends this to overridden methods and their parameters. Scopes, qualifiers, conditions and validation are not inherited by default, so bundle them in an `@Inherited` annotation:

```java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Requires(property = "datasource.url")
@Named
@Singleton
public @interface SqlRepository {
    @AliasFor(annotation = Named.class, member = AnnotationMetadata.VALUE_MEMBER)
    String value() default "";
}

@SqlRepository
public abstract class BaseSqlRepository {}

@Named("bookRepository")
public class BookRepository extends BaseSqlRepository { /* ... */ }
```

A child class must still have at least one bean-definition annotation such as a scope or qualifier.

## Aliasing

`@AliasFor` links members, e.g. `value` and `id` on `@Client` so `@Client("foo")` and `@Client(id="foo")` set both. Setting `annotation()` (or `annotationName()`) aliases a member of a stereotype, overriding its declared value. Options: `applyDefault = true` also applies the member default; `index()` picks which occurrence of a repeatable stereotype (default `-1` = all; `index` is computed for Java/Groovy sources only).

```java
@Retention(RetentionPolicy.RUNTIME)
@Size(min = 5, max = 5)
public @interface ComposedZip {
    @AliasFor(annotation = Size.class, member = "max", applyDefault = true)
    int max() default 10;
}
```

`@ComposedZip` yields `@Size(min = 5, max = 10)`; `@ComposedZip(max = 20)` yields `@Size(min = 5, max = 20)`.

For annotations you do not own, implement `AnnotationMapper` (use `NamedAnnotationMapper` if the annotation class is not on the processor classpath), register it in `META-INF/services/io.micronaut.inject.annotation.AnnotationMapper`, and put it on the `annotationProcessor` classpath (`kapt` in Kotlin). `AnnotationTransformer` can remap annotations such as `jakarta.validation.OverridesAttribute` to `@AliasFor`.

## Retaining composed annotations

Metadata is indexed by name, so two annotations composing the same stereotype with different members lose which came from which. Annotate the composed annotation with `@Retainable` (runtime retention required):

```java
@Retainable
@Retention(RetentionPolicy.RUNTIME)
public @interface Limit { int min() default 0; int max() default 100; }

@Limit(min = 5)
@Retention(RetentionPolicy.RUNTIME)
public @interface MinLength {
    @AliasFor(annotation = Limit.class, member = "min", applyDefault = true)
    int value() default 5;
}
```

With `@MinLength(3) @MaxLength(9)` on a bean, `definition.getAnnotation(MinLength.class).getStereotypes().get(0)` has values `{min=3}`, and the one from `MaxLength` has `{max=9}`. Retention costs generated code per occurrence, so opt in only when occurrence identity matters (composed constraints, interceptor bindings, diagnostics). Presence checks (`hasStereotype`, `getAnnotationValuesByName`, `getAnnotationNamesByStereotype`) do not need it.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
