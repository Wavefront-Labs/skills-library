---
id: computing-software.software-engineering.ktor.ktor-client-response-validation
name: ktor-client-response-validation
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, validation, expectsuccess, exceptions]
level: practitioner
status: docs-checked
description: "Validate Ktor client responses: expectSuccess exceptions for 3xx/4xx/5xx, plus HttpResponseValidator with validateResponse and handleResponseExceptionWithRequest."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-response-validation.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/client-validate-2xx-response/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/client-validate-non-2xx-response/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response validation in the Ktor client

By default the client does not validate responses by HTTP status code. Three strategies are available.

## 1. expectSuccess

Set `expectSuccess = true` in the client configuration (global) or on a single request. A non-successful status then throws:

- `RedirectResponseException` for 3xx responses.
- `ClientRequestException` for 4xx responses.
- `ServerResponseException` for 5xx responses.

```kotlin
val client = HttpClient(CIO) {
    expectSuccess = true
}
```

## 2. Custom validation with HttpCallValidator

Install it by calling `HttpResponseValidator { ... }` inside the client configuration block:

```kotlin
val client = HttpClient(CIO) {
    HttpResponseValidator {
        // ...
    }
}
```

### Stricter checks on 2xx responses

Default validation throws only for non-2xx. Use `validateResponse { response -> ... }` to inspect a successful response and throw your own exception. The example client (with `ContentNegotiation` and `json()`) reads the body as an `Error(code, message)` and throws a custom `ResponseException` subclass when `code != 0`:

```kotlin
class CustomResponseException(response: HttpResponse, cachedResponseText: String) :
    ResponseException(response, cachedResponseText) {
    override val message: String = "Custom server error: ${response.call.request.url}. " +
            "Status: ${response.status}. Text: \"$cachedResponseText\""
}

val client = HttpClient(CIO) {
    install(ContentNegotiation) { json() }
    HttpResponseValidator {
        validateResponse { response ->
            val error: Error = response.body()
            if (error.code != 0) {
                throw CustomResponseException(response, "Code: ${error.code}, message: ${error.message}")
            }
        }
    }
}
```

### Custom handling of non-2xx

Use `handleResponseExceptionWithRequest { exception, request -> ... }` to change which exception surfaces. The example throws a custom `MissingPageException` for `404 Not Found` instead of the default `ClientRequestException`:

```kotlin
class MissingPageException(response: HttpResponse, cachedResponseText: String) :
    ResponseException(response, cachedResponseText) {
    override val message: String = "Missing page: ${response.call.request.url}. " +
            "Status: ${response.status}."
}

val client = HttpClient(CIO) {
    expectSuccess = true
    HttpResponseValidator {
        handleResponseExceptionWithRequest { exception, request ->
            val clientException = exception as? ClientRequestException ?: return@handleResponseExceptionWithRequest
            val exceptionResponse = clientException.response
            if (exceptionResponse.status == HttpStatusCode.NotFound) {
                val exceptionResponseText = exceptionResponse.bodyAsText()
                throw MissingPageException(exceptionResponse, exceptionResponseText)
            }
        }
    }
}
```

Runnable examples: `client-validate-2xx-response` and `client-validate-non-2xx-response` in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-response-validation.md, codeSnippets/snippets/client-validate-2xx-response/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/client-validate-non-2xx-response/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
