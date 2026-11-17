---
id: computing-software.software-engineering.ktor.ktor-request-validation
name: ktor-request-validation
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, request-validation, validation, statuspages, content-negotiation, kotlin-server]
level: practitioner
status: docs-checked
description: "Validate incoming Ktor request bodies with the RequestValidation plugin: validate overloads, ValidationResult, ValidatorBuilder and handling RequestValidationException."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-request-validation.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/request-validation/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate request bodies in Ktor

The `RequestValidation` plugin (artifact `io.ktor:ktor-server-request-validation`, package `io.ktor.server.plugins.requestvalidation`) validates a raw body or, when `ContentNegotiation` with a serializer is installed, properties of a received object. Failure raises `RequestValidationException`.

## Three steps

1. Receive the body with a type parameter. Validation only runs when you call `call.receive<T>()`, for example `receive<String>()`.
2. Configure a `validate` function inside `install(RequestValidation) { ... }`. It returns a `ValidationResult`, success or failure. Two overloads exist:
   - One gives you the body as the specified type, such as `String`, or a data class like `Customer`. With ContentNegotiation installed you can check properties; the docs example validates that `id` falls in a range and fails when `id` is less than or equal to `0`.
   - One accepts a `ValidatorBuilder` for custom rules, used in the docs for validating a body received as a byte array (`receive<ByteArray>()`).
3. Handle `RequestValidationException` with the StatusPages plugin. The exception exposes the request body and the reasons for all validation failures, so your `exception` handler can build the error response from them.

## Object properties recipe

1. Define the data class (the docs use `Customer`).
2. Install `ContentNegotiation` with the JSON serializer.
3. Call `receive<Customer>()` in the route.
4. Add `validate<Customer> { ... }` checking the property and returning a `ValidationResult`.

## Docs example code

```kotlin
@Serializable
data class Customer(val id: Int, val firstName: String, val lastName: String)

fun Application.module() {
    install(RequestValidation) {
        validate<String> { bodyText ->
            if (!bodyText.startsWith("Hello"))
                ValidationResult.Invalid("Body text should start with 'Hello'")
            else ValidationResult.Valid
        }
        validate<Customer> { customer ->
            if (customer.id <= 0)
                ValidationResult.Invalid("A customer ID should be greater than 0")
            else ValidationResult.Valid
        }
        validate {
            filter { body ->
                body is ByteArray
            }
            validation { body ->
                check(body is ByteArray)
                val intValue = String(body).toInt()
                if (intValue <= 0)
                    ValidationResult.Invalid("A value should be greater than 0")
                else ValidationResult.Valid
            }
        }
    }
    install(StatusPages) {
        exception<RequestValidationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, cause.reasons.joinToString())
        }
    }
    install(ContentNegotiation) {
        json()
    }
    routing {
        post("/text") {
            val body = call.receive<String>()
            call.respond(body)
        }
        post("/json") {
            val customer = call.receive<Customer>()
            call.respond(customer)
        }
        post("/array") {
            val body = call.receive<ByteArray>()
            call.respond(String(body))
        }
    }
}
```

The plugin can also be installed on a specific route.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-request-validation.md, codeSnippets/snippets/request-validation/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
