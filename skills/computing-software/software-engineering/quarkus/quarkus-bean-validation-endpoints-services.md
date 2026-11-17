---
id: computing-software.software-engineering.quarkus.quarkus-bean-validation-endpoints-services
name: quarkus-bean-validation-endpoints-services
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, hibernate-validator, bean-validation, rest, constraints, validation-groups]
level: intro
status: docs-checked
description: "Validate input in Quarkus with Hibernate Validator: constraints, @Valid on REST endpoints and service methods, manual Validator, 400 vs 500 behaviour, groups."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/validation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bean Validation in Quarkus REST services

Add the extension: `quarkus add extension hibernate-validator` (dependency `io.quarkus:quarkus-hibernate-validator`).

## Constraints

```java
public class Book {
    @NotBlank(message="Title may not be blank")
    public String title;
    @Min(message="Author has been very lazy", value=1)
    public double pages;
}
```

## Three ways to trigger validation

1. Manual: `@Inject Validator validator;` then `Set<ConstraintViolation<Book>> v = validator.validate(book);` An empty set means valid.
2. REST endpoint: put `@Valid` (cascades to the bean) or constraints such as `@NotNull` on the parameter: `public Result post(@Valid Book book)`. Failure returns a generated JSON report with `"title": "Constraint Violation"`, `"status": 400` and a `violations` list of `field` and `message`.
3. Service method: annotate a CDI bean method parameter, e.g. `public void validateBook(@Valid Book book)` on an `@ApplicationScoped` bean.

To customize the 400 body, provide a `jakarta.ws.rs.ext.ExceptionMapper<ValidationException>` annotated `@Provider`.

## Gotcha: 400 only for endpoint parameters

Only failing constraints on REST endpoint parameters produce a bad request with a report. Service-method violations (parameters or return values) and endpoint return-value violations become a 5xx internal error unless you catch `ConstraintViolationException` or add an `ExceptionMapper`. Do not expose the validated value from violation objects publicly.

## Validation groups

Use groups when one class has different rules per method (null id on POST, non-null on PUT).

```java
public interface ValidationGroups {
    interface Post extends Default {}
    interface Put extends Default {}
}
public class Book {
    @Null(groups = ValidationGroups.Post.class)
    @NotNull(groups = ValidationGroups.Put.class)
    public Long id;
    @NotBlank public String title;
}
public void post(@Valid @ConvertGroup(to = ValidationGroups.Post.class) Book book) {}
```

Extending `Default` keeps ungrouped constraints (like `title`) active in each group.

## Limitations

- `META-INF/validation.xml` cannot configure the `ValidatorFactory`; use configuration properties and CDI beans. Constraints declared in `validation.xml` are accepted.
- Never build your own `ValidatorFactory` for native executables (you get `NoProviderFoundException`); inject `ValidatorFactory` or `Validator`. `Validation.buildDefaultValidatorFactory()` returns the Quarkus-managed one.

## Checked

2026-11-07. Read in full: validation.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
