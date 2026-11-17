---
id: computing-software.software-engineering.ktor.ktor-server-testing
name: ktor-server-testing
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, testing, testapplication, kotlin-test, http-client, mock]
level: practitioner
status: docs-checked
description: "Test a Ktor server with testApplication: dependencies, loading modules, environment config, mocking external services, client setup, forms, JSON, cookies, HTTPS, WebSockets."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-testing.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/engine-main/src/test/kotlin/EngineMainTest.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-oauth-google/src/test/kotlin/ApplicationTest.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/json-kotlinx/src/test/kotlin/jsonkotlinx/ApplicationTest.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test a Ktor server with testApplication

Ktor's testing engine processes calls internally, without starting a real web server or binding sockets, so tests are faster and more reliable.

## Dependencies

`io.ktor:ktor-server-test-host` (the testing engine) and `org.jetbrains.kotlin:kotlin-test` (assertions). For Native server tests add them to the `nativeTest` source set.

## Basic test

```kotlin
class ApplicationTest {
    @Test
    fun testRoot() = testApplication {
        application {
            module()
        }
        val response = client.get("/")
        assertEquals(HttpStatusCode.OK, response.status)
        assertEquals("Hello, world!", response.bodyAsText())
    }
}
```

Workflow: define the test with `testApplication {}`, configure the app, optionally configure the client, make requests with `client`, assert with `kotlin.test`.

## Configure the test application

- Modules: explicitly with `application { module1(); module2() }`, or load them from a configuration file via `environment { config = ApplicationConfig("application-custom.conf") }`.
- `application {}` gives the `Application` being configured; the `application` property in the `testApplication` scope returns the same instance, but it may not be started yet if read before `startApplication()` or the first client call.
- The app starts on the first client call; call `startApplication()` to start it manually, useful for testing lifecycle events:

```kotlin
@Test
fun testAccessApplicationInstance() = testApplication {
    lateinit var configuredApplication: Application
    application {
        configuredApplication = this
    }
    startApplication()
    val app: Application = application
    assertSame(configuredApplication, app)
}
```

- Properties programmatically:

```kotlin
environment {
    config = MapApplicationConfig("ktor.environment" to "dev")
}
```

- Routes and mocked external services (from the OAuth test): add test-only endpoints with `routing {}`, and mock hosts with `externalServices`:

```kotlin
val testHttpClient = createClient {
    install(HttpCookies)
    install(ContentNegotiation) {
        json()
    }
}
application {
    main(testHttpClient)
}
routing {
    get("/login-test") {
        val session = UserSession("xyzABC123", "abc123")
        call.sessions.set(session)
    }
}
externalServices {
    hosts("https://www.googleapis.com") {
        install(io.ktor.server.plugins.contentnegotiation.ContentNegotiation) {
            json()
        }
        routing {
            get("oauth2/v2/userinfo") {
                val info = UserInfo("1", "JetBrains", "", "")
                call.respond(info)
            }
        }
    }
}
```

## Client and requests

`client` is preconfigured. Use `createClient { install(ContentNegotiation) { json() } }` for JSON; `install(HttpCookies)` in a new client to preserve cookies between requests.

- JSON:

```kotlin
client = createClient {
    install(ContentNegotiation) {
        json()
    }
}
val response = client.post("/customer") {
    contentType(ContentType.Application.Json)
    setBody(Customer(3, "Jet", "Brains"))
}
assertEquals("Customer stored correctly", response.bodyAsText())
assertEquals(HttpStatusCode.Created, response.status)
```

- Form data: set `Content-Type` `application/x-www-form-urlencoded` and encode with `formUrlEncode()`:

```kotlin
val response = client.post("/signup") {
    header(HttpHeaders.ContentType, ContentType.Application.FormUrlEncoded.toString())
    setBody(listOf("username" to "JetBrains", "email" to "example@jetbrains.com", "password" to "foobar", "confirmation" to "foobar").formUrlEncode())
}
```

- Multipart (`multipart/form-data`):

```kotlin
val boundary = "WebAppBoundary"
val response = client.post("/upload") {
    setBody(
        MultiPartFormDataContent(
            formData {
                append("description", "Ktor logo")
                append("image", File("ktor_logo.png").readBytes().toString(), Headers.build {
                    append(HttpHeaders.ContentType, "image/png")
                    append(HttpHeaders.ContentDisposition, "filename=\"ktor_logo.png\"")
                })
            },
            boundary,
            ContentType.MultiPart.FormData.withParameter("boundary", boundary)
        )
    )
}
```

- Cookies preserved between requests with a new client:

```kotlin
val client = createClient {
    install(HttpCookies)
}
```

- HTTPS: set the protocol in the request URL:

```kotlin
val response = client.get("/") {
    url {
        protocol = URLProtocol.HTTPS
    }
}
```

- WebSockets: create the client with the `WebSockets` client plugin:

```kotlin
val client = createClient {
    install(WebSockets)
}
client.webSocket("/echo") {
    val greetingText = (incoming.receive() as? Frame.Text)?.readText() ?: ""
    assertEquals("Please enter your name", greetingText)
    send(Frame.Text("JetBrains"))
    val responseText = (incoming.receive() as Frame.Text).readText()
    assertEquals("Hi, JetBrains!", responseText)
}
```

- End-to-end: use the Ktor `HttpClient` against a real running server (the page's example extends a `TestServer` base class and calls `HttpClient().get("http://localhost:8080/").body()`).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-testing.md, codeSnippets/snippets/engine-main/src/test/kotlin/EngineMainTest.kt, codeSnippets/snippets/auth-oauth-google/src/test/kotlin/ApplicationTest.kt, codeSnippets/snippets/json-kotlinx/src/test/kotlin/jsonkotlinx/ApplicationTest.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
