---
id: computing-software.software-engineering.ktor.ktor-server-events
name: ktor-server-events
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, events, monitoring, lifecycle, eventdefinition, kotlin]
level: practitioner
status: docs-checked
description: "Handle Ktor server lifecycle events with monitor.subscribe, raise custom EventDefinition events such as a 404 NotFoundEvent, and use MonitoringEvent inside plugins."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-events.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/events/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/events/src/main/kotlin/com/example/plugins/ApplicationMonitoringPlugin.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor a Ktor application with events

Each event is an `EventDefinition<T>` instance; `T` is the value passed to handlers. Most predefined events pass `Application`.

## Predefined lifecycle events

`ApplicationStarting`, `ApplicationStarted`, `ServerReady`, `ApplicationStopPreparing`, `ApplicationStopping`, `ApplicationStopped`. A typical use is subscribing to `ApplicationStopped` to release resources.

## Handle events in the application

The `monitor` property of `Application` exposes an `Events` instance with:

- `subscribe(definition) { value -> ... }`
- `unsubscribe(definition) { ... }`
- `raise(definition, value)`

```kotlin
fun Application.module() {
    install(ApplicationMonitoringPlugin)
    monitor.subscribe(ApplicationStarted) { application ->
        application.environment.log.info("Server is started")
    }
    monitor.subscribe(ApplicationStopped) { application ->
        application.environment.log.info("Server is stopped")
        // Release resources and unsubscribe from events
        monitor.unsubscribe(ApplicationStarted) {}
        monitor.unsubscribe(ApplicationStopped) {}
    }
    monitor.subscribe(NotFoundEvent) { call ->
        log.info("No page was found for the URI: ${call.request.uri}")
    }
}
```

## Handle events in a custom plugin

Use the `MonitoringEvent` hook through `on()`:

```kotlin
val ApplicationMonitoringPlugin = createApplicationPlugin(name = "ApplicationMonitoringPlugin") {
    on(MonitoringEvent(ApplicationStarted)) { application ->
        application.log.info("Server is started")
    }
    on(MonitoringEvent(ApplicationStopped)) { application ->
        application.log.info("Server is stopped")
        // Release resources and unsubscribe from events
        application.monitor.unsubscribe(ApplicationStarted) {}
        application.monitor.unsubscribe(ApplicationStopped) {}
    }
    on(ResponseSent) { call ->
        if (call.response.status() == HttpStatusCode.NotFound) {
            this@createApplicationPlugin.application.monitor.raise(NotFoundEvent, call)
        }
    }
}

val NotFoundEvent: EventDefinition<ApplicationCall> = EventDefinition()
```

## Custom events (example: 404)

1. Define the event: `val NotFoundEvent: EventDefinition<ApplicationCall> = EventDefinition()`.
2. Raise it from a plugin: in an `on(ResponseSent)` handler, if the call's response status is `404 Not Found`, call `monitor.raise(NotFoundEvent, call)` (shown above).
3. Install the plugin in the application: `install(ApplicationMonitoringPlugin)`.
4. Subscribe: `monitor.subscribe(NotFoundEvent) { call -> ... }` (shown above).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-events.md, codeSnippets/snippets/events/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/events/src/main/kotlin/com/example/plugins/ApplicationMonitoringPlugin.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
