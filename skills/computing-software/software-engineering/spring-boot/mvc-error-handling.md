---
id: computing-software.software-engineering.spring-boot.mvc-error-handling
name: mvc-error-handling
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, error-handling, errorcontroller, errorattributes, problem-details, controlleradvice, error-pages, whitelabel]
level: practitioner
status: docs-checked
description: "Customize Spring Boot servlet error handling: /error mapping, ErrorController, ErrorAttributes, RFC 9457 problem details, custom error pages and ErrorViewResolver."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot provides an `/error` mapping registered as a global error page in the servlet container. Machine clients get JSON (details, HTTP status, exception message); browsers get a "whitelabel" HTML view (customize by adding a `View` that resolves to `error`). Tune with `spring.web.error.*` properties.

Replace the behaviour: implement `ErrorController` and register a bean, or add an `ErrorAttributes` bean to keep the mechanism but change contents. `BasicErrorController` can be a base class, for example to add a handler for a new content type: extend it, add a public `@RequestMapping` method with a `produces` attribute, and create a bean of your type.

Problem Details (RFC 9457, Spring Framework 6.0+): set `spring.mvc.problemdetails.enabled` to `true` to produce `application/problem+json` with fields `type`, `title`, `status`, `detail`, `instance`.

`@ControllerAdvice` can return your own error body POJO for particular controllers or exceptions, instead of `ErrorAttributes`. Errors handled at controller level may not be recorded by web observations or metrics; set the handled exception on the observation context to record them.

Custom error pages: add a file under an `/error` directory, static HTML in any static resource directory or a template. The file name is the exact status code or a series mask:
- `src/main/resources/public/error/404.html`
- `src/main/resources/templates/error/5xx.ftlh` (FreeMarker)

For complex mappings implement `ErrorViewResolver` beans. `@ExceptionHandler` and `@ControllerAdvice` work as usual, and `ErrorController` picks up unhandled exceptions.

Outside Spring MVC: register `ErrorPage` instances through an `ErrorPageRegistrar`. If the error path is handled by a `Filter` (common with Jersey and Wicket), register the filter for the `ERROR` dispatcher type; the default `FilterRegistrationBean` does not include it.

WAR deployments: Boot's error page filter forwards error responses only if the response is not yet committed. WebSphere Application Server 8.0+ commits by default; set `com.ibm.ws.webcontainer.invokeFlushAfterService` to `false`.

## Checked

2026-11-07. Read web/servlet.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
