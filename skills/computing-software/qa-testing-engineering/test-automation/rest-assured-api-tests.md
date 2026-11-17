---
id: computing-software.qa-testing-engineering.test-automation.rest-assured-api-tests
name: rest-assured-api-tests
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [rest-assured, api-testing, java, junit5, json-schema-validation]
level: practitioner
status: docs-checked
description: "Write REST Assured API tests in Java: given/when/then, request and response specifications, JSON path and Hamcrest assertions, schema validation, auth and logging on failure."
sources:
  - https://rest-assured.io/
  - https://github.com/rest-assured/rest-assured/wiki/Usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST Assured API tests in Java

**Goal:** readable, maintainable HTTP API tests in the JVM stack, run from a unit test framework such as JUnit.

## Basics
```java
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

RequestSpecBuilder builder = new RequestSpecBuilder();
// set base URI, content type, headers and auth on the builder; read the base URL from configuration
RequestSpecification spec = builder.build();
RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();

int id =
  given().spec(spec).body(Map.of("sku", "SKU-1", "qty", 2))
  .when().post("/orders")
  .then().statusCode(201)
    .body("status", equalTo("PENDING"))
    .body("items.sku", hasItem("SKU-1"))
    .time(lessThan(800L))
  .extract().path("id");

given().spec(spec).pathParam("id", id)
  .when().get("/orders/{id}")
  .then().statusCode(200).body("id", equalTo(id));
```
A specification built by `RequestSpecBuilder.build()` cannot send a request itself; pass it with
`given().spec(requestSpec)`. `ResponseSpecBuilder` holds shared expectations (for example `expectStatusCode`).
Merging a specification only overwrites values it sets itself (REST Assured 6.2.0 behaviour per the wiki).

## Useful features
- GPath (Groovy closures) in body paths: `body("store.book.findAll { it.price < 10 }.title", hasItems(...))`.
- JSON schema: `body(matchesJsonSchemaInClasspath("<schema>.json"))`, from the `json-schema-validator` module
  (a separate dependency). From REST Assured 6.1.0 it supports draft-03/04/06/07, 2019-09 and 2020-12 and reads
  the schema's `$schema` keyword.
- Deserialise: `.as(Message.class)` (or a `TypeRef` for generics), then assert with your assertion library.
- Auth: `auth().preemptive().basic("user", "password")`, `auth().oauth2(accessToken)`.
- Logging: `RestAssured.enableLoggingOfRequestAndResponseIfValidationFails()` and
  `io.restassured.filter.log.ErrorLoggingFilter` (prints the response body for error status codes).
- Spring MVC: the `spring-mock-mvc` module's `RestAssuredMockMvc` unit-tests controllers with the same DSL.
- Response time: `time(lessThan(2000L))` (milliseconds) or `time(lessThan(2L), SECONDS)`.

## Gotchas
- Floating point numbers in JSON must be compared with a Java `float` (a `double` comparison fails); to get
  `BigDecimal` instead, configure `jsonConfig().numberReturnType(BIG_DECIMAL)`.
- Statics such as `RestAssured.baseURI` apply globally and can be reset with `RestAssured.reset()`; prefer
  per-test specifications.

## Verify
Tests run in CI via your build tool with failure logs showing request and response, and the base URL is
configurable per environment.

## Checked
2026-11-01. Confirmed in the REST Assured Usage wiki: specification builders and merging, GPath `findAll`,
`matchesJsonSchemaInClasspath` and the schema-validator module and draft support, `as`, preemptive basic and
OAuth2 auth, logging if validation fails, `ErrorLoggingFilter`, `RestAssuredMockMvc`, `time(lessThan(...))`,
float and BigDecimal handling, static `baseURI`. Removed: the full JUnit 5 class and fixed token/header
helpers, `setBaseUri` and `setContentType` builder calls, and the sample order assertions as documented behaviour.
Method: documentation only; no commands were run.
