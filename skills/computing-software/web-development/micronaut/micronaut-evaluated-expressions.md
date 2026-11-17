---
id: computing-software.web-development.micronaut.micronaut-evaluated-expressions
name: micronaut-evaluated-expressions
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, expression-language, evaluated-expressions, annotations, compile-time, scheduled]
level: advanced
status: docs-checked
description: "Write #{...} evaluated expressions in Micronaut annotations and extend their evaluation context with custom beans or per-annotation contexts."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/config/evaluatedExpressions.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use `#{...}` expressions (since Micronaut 4) in annotation string members.

Expressions are validated and compiled at build time, evaluated reflection-free, and cannot be compiled from untrusted input at runtime; errors are compile failures. Not supported on `TYPE_USE` annotations. They work wherever a member takes a string or string array, and can be embedded in templates:

```java
@Value("#{ T(Math).random() }") double injectedValue;
@Requires(env = {"dev", "#{ 'test' }"})
@Value("http://#{'hostname'}/#{'path'}") String url;
```

Typical use, scheduled job control:

```java
@Scheduled(fixedRate = "1s", condition = "#{!this.paused}")
void run() { ... }
public boolean isPaused() { return paused; }
```

`@RouteCondition` accepts expressions for conditional routing too.

## Syntax

- Literals: `null`, `true`, `'string'`, `10`, `0xFFL`, `10L`, `.123f`, `1E+1d`.
- Math: `+ - * / % ^` (`^` is exponentiation; `div`, `mod` aliases; `+` concatenates strings).
- Comparison: `== != > < >= <= matches` (regex must be a literal and is checked at compile time).
- Logic: `&& ||` `!` (aliases `and`, `or`, `not`), `empty` / `not empty`.
- Ternary: `cond ? a : b`.
- Navigation: `a.b.c`, null-safe `foo?.bar?.name` (unwraps `Optional`).
- Types: `T(java.lang.String)`; `java.lang` classes by simple name; `'abc' instanceof T(String)`; static calls `T(Math).random()`. No primitives.
- Beans: `ctx[T(io.micronaut.example.ContextBean)]` (`T(...)` optional).
- Environment: `env['test.property']` (key must resolve to a string; absent value yields `null`).
- Context members referenced with `#`: methods `#stringValue().length()`, varargs `#countIntegers(1, 2, 3)`, properties `#name` (JavaBean getter).

## Extending the evaluation context

By default only static methods via `T(...)` are callable. To add methods globally:

1. Write a bean class, e.g. `@Singleton public class CustomEvaluationContext { public int generateRandom(int min, int max) {...} }` (effectively a singleton whatever its scope).
2. Register it with an `ExpressionEvaluationContextRegistrar` returning the class name from `getContextClassName()`, listed in `META-INF/services/io.micronaut.inject.visitor.TypeElementVisitor` in a module on the annotation processor classpath.
3. Use it: `@Value("#{ generateRandom(1, 10) }") public int randomField;`

An unmatched method, or one matching several overloads/registrars, fails compilation.

Per-annotation scope uses `@AnnotationExpressionContext`:

```java
@Singleton
@CustomAnnotation(value = "#{firstValue() + secondValue()}")
class Example {}

@AnnotationExpressionContext(AnnotationContext.class)   // all members
@interface CustomAnnotation {
    @AnnotationExpressionContext(AnnotationMemberContext.class)  // this member only
    String value();
}
```

Context classes must still be beans. On an annotated method, parameters can be referenced by name; a parameter named like a context property makes the reference ambiguous (compile failure). `methodArguments = false` on `@AnnotationExpressionContext` excludes them.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
