---
id: computing-software.software-engineering.ktor.ktor-server-modules
name: ktor-server-modules
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, modules, application, embeddedserver, configuration, kotlin]
level: practitioner
status: docs-checked
description: "Define Ktor modules as Application extension functions, load them via embeddedServer or ktor.application.modules, share dependencies, and enable concurrent module loading."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-modules.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/engine-main-modules/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/embedded-server-modules/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structure a Ktor server with modules

A module is an extension function on `Application` that sets up routes, installs plugins and configures services. Modules group related routes, keep features isolated and ease testing.

```kotlin
fun Application.module1() {
    routing {
        get("/module1") {
            call.respondText("Hello from 'module1'!")
        }
    }
}
```

Plugins installed in one module are in effect for the other loaded modules.

## Loading modules

- Embedded server: `embeddedServer` takes the module as a lambda, or pass a reference through the `module` parameter:

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module).start(wait = true)
}

fun Application.module() {
    module1()
    module2()
}
```

- Configuration file: list modules under `ktor.application.modules` in `application.conf` or `application.yaml`, each as a fully qualified name: the class's fully qualified name plus the extension function name (`ApplicationKt` for top-level functions in `Application.kt`, `SampleKt` for `Sample.kt`):

```
ktor {
    deployment {
        port = 8080
    }
    application {
        modules = [ com.example.ApplicationKt.module1,
                    com.example.ApplicationKt.module2,
                    org.sample.SampleKt.module3 ]
    }
}
```

with `fun main(args: Array<String>): Unit = io.ktor.server.netty.EngineMain.main(args)` as the entry point.

## Sharing dependencies between modules

1. Parameters: declare dependencies as module function parameters and create them once in `embeddedServer { ... }`, then call `routingModule(myService)`:

```kotlin
embeddedServer(CIO, port = 8080, host = "0.0.0.0") {
    val myService = MyService(property<MyServiceConfig>())
    routingModule(myService)
    schedulingModule(myService)
}.start(wait = true)
```

Simple, but modules are coupled at compile time and cannot be swapped at runtime.
2. Application attributes: put values in `Application.attributes` with an `AttributeKey<T>` and read them in another module. This gives loose coupling:

```kotlin
val customerServiceKey = AttributeKey<CustomerService>("CustomerService")

fun Application.servicesModule() {
    attributes[customerServiceKey] = CustomerService()
}

fun Application.customerModule() {
    val service = attributes[customerServiceKey]
    routing {
        get("/customers") { call.respond(service.all()) }
    }
}
```
3. The Ktor dependency injection plugin (see ktor-di-dependency-registration).

## Concurrent modules

Modules may be `suspend` functions. By default they load sequentially; to launch them independently so a suspended module does not block others, set in the configuration file:

```
ktor {
    application {
        startup = concurrent
    }
}
```

Properties: `ktor.application.startup` (`sequential` default, or `concurrent`) and `ktor.application.startupTimeoutMillis` (`Long`, default `10000`).

With DI, modules can then load in order of appearance:

```kotlin
suspend fun Application.installEvents() {
    // Suspends until provided
    val kubernetesConnection = dependencies.resolve<KubernetesConnection>()
}

suspend fun Application.loadEventsConnection() {
    dependencies.provide<KubernetesConnection> {
        connect(property<KubernetesConfig>("app.events"))
    }
}
```

Note: concurrent module loading is a single-threaded process, which avoids threading problems with unsafe collections in the application's shared internal state.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-modules.md, codeSnippets/snippets/engine-main-modules/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/embedded-server-modules/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
