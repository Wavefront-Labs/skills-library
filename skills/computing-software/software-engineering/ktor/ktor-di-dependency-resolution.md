---
id: computing-software.software-engineering.ktor.ktor-di-dependency-resolution
name: ktor-di-dependency-resolution
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, dependency-injection, di, resolution, named, kotlin]
level: advanced
status: docs-checked
description: "Resolve Ktor DI dependencies by property delegation or resolve(), use @Named and @Property, async resolution, module parameter injection, nullable types and covariance limits."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-di-dependency-resolution.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/server-di/src/main/kotlin/com.example/Repositories.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/server-di/src/main/kotlin/com.example/AsyncDependencies.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/server-di/src/main/kotlin/com.example/Logging.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/server-di/src/main/resources/application.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolve dependencies from Ktor DI

Requires `io.ktor:ktor-server-di`, after dependencies are registered (see ktor-di-dependency-registration).

## Explicit resolution

```kotlin
val service: GreetingService by dependencies          // property delegation
val service = dependencies.resolve<GreetingService>() // direct resolution
```

Property delegation resolves only during the startup validation phase. Direct resolution returns the dependency immediately or suspends until it becomes available.

## Parameter resolution

Constructor and function parameters are resolved by type by default. Use annotations when that is not enough:

- `@Named` selects a dependency registered with that name:

```kotlin
fun Application.userRepository(@Named("mongo") database: Database) {
    // Uses the dependency named "mongo"
}
```

- `@Property` (`io.ktor.server.plugins.di.annotations.Property`) injects a value from the application configuration:

```kotlin
fun provideDatabase(
    @Property("database.connectionUrl") connectionUrl: String
): Database = PostgresDatabase(connectionUrl)
```

```yaml
database:
  connectionUrl: postgres://localhost:5432/admin
```

## Async and module injection

Use suspending functions for asynchronous loading; the DI plugin automatically suspends `resolve()` calls until all dependencies are ready:

```kotlin
suspend fun Application.installEvents() {
    val conn: EventsConnection = dependencies.resolve()
    log.info("Events connection ready: $conn")
}

suspend fun Application.loadEventsConnection() {
    dependencies.provide {
        delay(200) // simulate async work
        EventsConnection(true)
    }
}
```

Module functions can take dependencies as parameters, matched by type. Register providers under `ktor.application.dependencies` in the configuration file, then declare the module function with parameters for what you want injected:

```yaml
ktor:
  application:
    dependencies:
      - com.example.PrintStreamProviderKt.stdout
    modules:
      - com.example.LoggingKt.logging
```

```kotlin
fun stdout(): () -> PrintStream = { System.out }

fun Application.logging(printStreamProvider: () -> PrintStream) {
    dependencies {
        provide<Logger> {
            Logger(printStreamProvider())
        }
    }
}
```

## Optional dependencies

```kotlin
val config: Config? by dependencies
val config = dependencies.resolve<Config?>()
```

## Covariance and its limit

Covariant type parameters let a value be injected as a supertype:

```kotlin
dependencies { provide<List<String>> { listOf("one", "two") } }
val stringList: List<CharSequence> by dependencies       // works
val stringCollection: Collection<CharSequence> by dependencies // works
```

A non-generic subtype also resolves as its supertype (a registered `BufferedOutputStream` resolves as `OutputStream`).

Limitation: resolving parameterized types across type-argument subtypes is not supported. With `provide<Sink<CharSequence>> { CsqSink() }`, `val s: Sink<String> by dependencies` will not resolve.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-di-dependency-resolution.md, codeSnippets/snippets/server-di/src/main/kotlin/com.example/Repositories.kt, codeSnippets/snippets/server-di/src/main/kotlin/com.example/AsyncDependencies.kt, codeSnippets/snippets/server-di/src/main/kotlin/com.example/Logging.kt, codeSnippets/snippets/server-di/src/main/resources/application.yaml.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
