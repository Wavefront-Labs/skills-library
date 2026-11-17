---
id: computing-software.web-development.micronaut.micronaut-validate-controller-input
name: micronaut-validate-controller-input
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, data-validation, validated, jakarta-validation, validation-groups, constraint-violation]
level: practitioner
status: docs-checked
description: "Validate Micronaut controller parameters and POJO bodies with jakarta.validation, @Validated, @Valid, validation groups and a custom constraint handler."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/datavalidation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/datavalidation/validationGroups.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate controller input

Goal: reject invalid parameters and bodies with `jakarta.validation` constraints.

## Dependencies

Native support: `io.micronaut.validation:micronaut-validation-processor` (annotationProcessor) and `io.micronaut.validation:micronaut-validation`. For full JSR 380 compliance use `io.micronaut.beanvalidation:micronaut-hibernate-validator`. Bean injection in custom constraints is supported with the Hibernate Validator configuration.

## Parameters

```java
@Validated
@Controller("/email")
public class EmailController {
    @Get("/send")
    public HttpResponse send(@NotBlank String recipient, @NotBlank String subject) {
        return HttpResponse.ok(Collections.singletonMap("msg", "OK"));
    }
}
```

A violation throws `jakarta.validation.ConstraintViolationException`, handled by default by `io.micronaut.validation.exception.ConstraintExceptionHandler`. To use your own handler, annotate it `@Replaces(ConstraintExceptionHandler.class)`.

## POJO bodies

Annotate the controller with `@Validated`, the body parameter with `@Valid`, and the class with `@Introspected` plus constraints on fields:

```java
@Introspected
public class Email {
    @NotBlank String subject;
    @NotBlank String recipient;
    // getters and setters
}

@Validated
@Controller("/email")
public class EmailController {
    @Post("/send")
    public HttpResponse send(@Body @Valid Email email) { ... }
}
```

## Validation groups

Enforce a subset of constraints with `groups` on `@Validated`. Define a group that extends `Default` so it includes `Default` constraints:

```java
public interface FinalValidation extends Default {}

@Introspected
public class Email {
    @NotBlank String subject;                                   // Default group
    @NotBlank(groups = FinalValidation.class) String recipient; // only when FinalValidation is active
}

@Validated                      // class level: Default group active
@Controller("/email")
public class EmailController {
    @Post("/createDraft")
    public HttpResponse createDraft(@Body @Valid Email email) { ... }   // recipient not enforced

    @Post("/send")
    @Validated(groups = FinalValidation.class)
    public HttpResponse send(@Body @Valid Email email) { ... }          // both enforced
}
```

`@Validated` without groups means `Default`; a method-level `groups` setting overrides the class-level one for that method.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
