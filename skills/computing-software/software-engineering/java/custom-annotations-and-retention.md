---
id: computing-software.software-engineering.java.custom-annotations-and-retention
name: custom-annotations-and-retention
category: computing-software
field: software-engineering
product: java
tags: [java, java-reflection, custom-annotations, retention-policy, annotation-target, repeatable-annotations, meta-annotations, getannotation]
level: practitioner
status: docs-checked
description: "Define custom Java annotations with correct @Retention, @Target, @Inherited and @Repeatable, read them by reflection, and know the limits of element types."
sources:
  - https://docs.oracle.com/javase/specs/jls/se21/html/jls-9.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/annotation/Retention.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/annotation/RetentionPolicy.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/annotation/Inherited.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/annotation/Repeatable.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/AnnotatedElement.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom annotations

## Declaration
```java
@Retention(RetentionPolicy.RUNTIME)           // SOURCE, CLASS (default), or RUNTIME
@Target({ElementType.METHOD, ElementType.TYPE})
public @interface Audited {
    String action();
    Level level() default Level.INFO;
    String[] tags() default {};
}
```
- `RetentionPolicy.RUNTIME`: recorded in the class file and retained by the VM, so readable reflectively. `CLASS`: recorded in the class file but need not be retained at run time; this is the default when no `@Retention` is present. `SOURCE`: discarded by the compiler.
- `@Retention` only has effect when the meta-annotated interface is used directly to annotate; not when it is used as a member interface inside another annotation.
- `@Target` lists the declaration contexts. With no `@Target`, the annotation is applicable in all declaration contexts and in no type contexts. All type contexts are covered by the single constant `ElementType.TYPE_USE`. The same constant may not appear twice in the `value`.
- `@Inherited` makes a class query fall back to the superclass chain until an annotation is found or `Object` is reached. It has no effect on anything other than a class, and annotations on implemented interfaces are not inherited.
- Element return types may be only: a primitive, `String`, `Class` (or a parameterised `Class`), an enum type, an annotation type, or a one-dimensional array of those. Nested arrays such as `String[][]` are a compile error.
- Element values must be constants (for primitives and `String`), class literals, or enum constants; `null` is not allowed.

## Reading
```java
Method m = svc.getClass().getMethod("pay", Order.class);
Audited a = m.getAnnotation(Audited.class);          // null if not present
```
- `AnnotatedElement.getAnnotation` returns the annotation if present, else `null`. `getDeclaredAnnotation` returns it only if directly present on the element.
- For repeatable annotations use `getAnnotationsByType`, which returns annotations associated with the element, whether directly or indirectly (via a container) present.
```java
@Repeatable(Roles.class) @interface Role { String value(); }
@interface Roles { Role[] value(); }
```
- `@Repeatable`'s `value` names the containing annotation interface.

## Verify
- [ ] A unit test asserts `getAnnotation(...)` returns the value on an annotated class, and is `null` when retention is not `RUNTIME`.
- [ ] A subclass of an annotated class sees the annotation only if the annotation type is `@Inherited`.

## Checked
Method: docs-checked 2026-11-09 against JLS 21 chapter 9 and the Javadoc for Retention, RetentionPolicy, Inherited, Repeatable and AnnotatedElement. Dropped the dev.java source (page not readable) and unconfirmed claims about Spring merged-annotation utilities, proxies, annotation caching, -parameters and missing annotation classes.
