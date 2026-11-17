---
id: computing-software.web-development.micronaut.micronaut-custom-argument-binders
name: micronaut-custom-argument-binders
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, custom-argument-binding, argument-binder, bindable, typed-binder, binding-result]
level: advanced
status: docs-checked
description: "Write annotation-based and type-based Micronaut request argument binders and understand BindingResult satisfied, unsatisfied and empty semantics."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/customArgumentBinding.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom argument binders

Goal: bind a controller argument from request data Micronaut does not handle itself.

## How lookup works

The `ArgumentBinderRegistry` finds `ArgumentBinder` beans. The default implementation first looks for an argument annotation meta-annotated with `@Bindable` and a binder for it; if none, it looks for a binder for the argument type.

## Annotation-based binder

1. Create the annotation, itself marked `@Bindable`:

```java
@Target({FIELD, PARAMETER, ANNOTATION_TYPE})
@Retention(RUNTIME)
@Bindable
public @interface ShoppingCart {
    @AliasFor(annotation = Bindable.class, member = "value")
    String value() default "";
}
```

2. Implement `AnnotatedRequestArgumentBinder<ShoppingCart, Object>` as a `@Singleton`. Override `getAnnotationType()` and `bind(ArgumentConversionContext<Object> context, HttpRequest<?> source)`. The example reads the `shoppingCart` cookie, deserializes it to a map, picks the entry named by the annotation value (or the argument name) and converts it with `ConversionService`; it returns `BindingResult.EMPTY` when the cookie is absent.
3. Use it: `HttpResponse<String> checkSession(@ShoppingCart Long sessionId)`. It takes precedence over a type-based binder.

## Type-based binder

Implement `TypedRequestArgumentBinder<ShoppingCart>`: override `bind(...)` (returning a `BindingResult`, e.g. a lambda that deserializes the cookie JSON) and `argumentType()` returning `Argument.of(ShoppingCart.class)` (used by the registry). Any controller argument of that type then uses it: `loadCart(ShoppingCart shoppingCart)`.

## BindingResult rules

- Results are satisfied or unsatisfied, and empty or not empty.
- Binders are initially called before the body is read and before any filters run; an unsatisfied result may be retried at different times in request processing. If you depend on data not yet present, return `ArgumentBinder.BindingResult#UNSATISFIED`; the binder may be called again later.
- Returning `EMPTY` or a satisfied result is final: the binder is not called again for that request.
- If the result is still `UNSATISFIED` at the end of processing, it is treated as `EMPTY`.
- Tip: use `ConversionService` to convert data to the argument type.

## Checked
2026-11-07. Checked against the custom argument binding page and its snippets. Reworded the binder call timing to match the page (initially called before the body is read; unsatisfied results may be retried).

Method: documentation only; no commands were run.
