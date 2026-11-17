---
id: computing-software.software-engineering.java.spring-mvc-controllers-validation-and-errors
name: spring-mvc-controllers-validation-and-errors
category: computing-software
field: software-engineering
product: java
tags: [java, spring-mvc, controlleradvice, bean-validation, problemdetail, rest-controller, spring-boot, spring-web]
level: practitioner
status: docs-checked
description: "Build Spring MVC REST endpoints: @RestController mapping, DTOs with Bean Validation, ResponseEntity status codes, and RFC 9457 ProblemDetail errors via @RestControllerAdvice."
sources: ["https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller.html", "https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html", "https://docs.spring.io/spring-boot/reference/io/validation.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Spring MVC controllers, validation and errors

**Goal:** thin controllers that validate input, return precise status codes and a
consistent error format.

## Controller
```java
@RestController
@RequestMapping("/api/v1/orders")
class OrderController {
    private final OrderService service;
    OrderController(OrderService service) { this.service = service; }

    @GetMapping("/{id}")
    OrderDto get(@PathVariable UUID id) { return service.get(id); }   // 200

    @PostMapping
    ResponseEntity<OrderDto> create(@Valid @RequestBody CreateOrder req, UriComponentsBuilder uri) {
        OrderDto o = service.create(req);
        return ResponseEntity.created(uri.path("/api/v1/orders/{id}").build(o.id())).body(o);  // 201 + Location
    }

    @GetMapping
    Page<OrderDto> list(@RequestParam(defaultValue = "0") int page,
                        @RequestParam(defaultValue = "20") @Max(100) int size) { ... }
}
```
Never expose JPA entities directly: DTO records decouple the API from the schema and avoid
lazy-loading serialisation errors.

## Validation
```java
record CreateOrder(@NotNull UUID customerId,
                   @NotEmpty List<@Valid Line> lines,
                   @Size(max = 500) String note) {}
record Line(@NotBlank String sku, @Positive int qty) {}
```
Needs a Bean Validation provider, typically via `spring-boot-starter-validation`. `@Valid` on a `@RequestBody` command object is validated individually and raises `MethodArgumentNotValidException`. When constraint annotations (`@Max`, `@NotBlank`, ...) sit directly on controller method parameters, Spring MVC applies method validation and raises `HandlerMethodValidationException` instead. Handle both exceptions.

## Errors as ProblemDetail (RFC 9457)
```properties
spring.mvc.problemdetails.enabled=true
```
```java
@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(OrderNotFound.class)
    ProblemDetail notFound(OrderNotFound e) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
        pd.setType(URI.create("https://api.acme.dev/problems/order-not-found"));
        pd.setProperty("orderId", e.id());
        return pd;
    }
}
```
With `spring.mvc.problemdetails.enabled=true` Boot auto-configures a `ResponseEntityExceptionHandler` that renders built-in exceptions as problem details; extend `ResponseEntityExceptionHandler` yourself to customise that handling (e.g. add a field-errors list). Never return stack traces or exception
messages from unexpected errors; log them with a correlation id and return a generic 500.

## Gotchas
- Boot 4 uses Jackson 3 (`JsonMapper`); tune it with `spring.jackson.*` properties (for example `spring.jackson.deserialization.<feature>`) or a `JsonMapperBuilderCustomizer` bean.
- Validation errors can be raised as two different exception types (see Validation); a handler for only one leaves the other on the default path.

## Verify
- [ ] `@WebMvcTest` tests cover 400 (validation), 404 (ProblemDetail body) and 201 + Location.
- [ ] Error responses have `Content-Type: application/problem+json`.

## Checked

Date: 2026-10-25. Documentation release: Spring Boot 4.1.2 and Spring Framework 7.0.10 (GitHub main documentation sources; releases of 2026-10-22).

Confirmed: `MethodArgumentNotValidException` versus `HandlerMethodValidationException` rules; `spring.mvc.problemdetails.enabled` and the `ResponseEntityExceptionHandler` it configures; `ProblemDetail.forStatusAndDetail`, `setType`, `setProperty`; `application/problem+json` media type; `ResponseEntity.created(URI)`; Boot 4 Jackson 3 `JsonMapper` and `JsonMapperBuilderCustomizer`; Bean Validation starter.

Removed as unconfirmed: the `@Validated`-on-class requirement for parameter constraints, the `-parameters` note, the FAIL_ON_UNKNOWN_PROPERTIES default claim and the trailing-slash default claim (none appear in the current docs).

Method: documentation only; no commands were run.
