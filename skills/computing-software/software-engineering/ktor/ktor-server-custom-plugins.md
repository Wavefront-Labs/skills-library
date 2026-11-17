---
id: computing-software.software-engineering.ktor.ktor-server-custom-plugins
name: ktor-server-custom-plugins
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, custom-plugin, createapplicationplugin, oncall, hooks, kotlin]
level: practitioner
status: docs-checked
description: "Build a custom Ktor server plugin with createApplicationPlugin: onCall, onCallReceive, onCallRespond, onCallValidators, on() hooks, config classes, call attributes, state."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-custom-plugins.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/custom-plugin/src/main/kotlin/com/example/plugins/CustomHeaderPlugin.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/custom-plugin/src/main/kotlin/com/example/plugins/CustomHeaderPluginConfigurable.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/events/src/main/kotlin/com/example/plugins/ApplicationMonitoringPlugin.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write a custom Ktor server plugin

The custom plugin API does not require knowledge of pipelines or phases. Call `createApplicationPlugin(name = "...")` to get an `ApplicationPlugin`, then `install()` it. Use `createRouteScopedPlugin()` for a plugin installable on a specific route.

```kotlin
val SimplePlugin = createApplicationPlugin(name = "SimplePlugin") {
    println("SimplePlugin is installed!")
}
```

A plugin with a configuration class (see Configuration below), installed with `install(CustomHeaderPlugin) { ... }`:

```kotlin
val CustomHeaderPlugin = createApplicationPlugin(
    name = "CustomHeaderPlugin",
    createConfiguration = ::PluginConfiguration
) {
    val headerName = pluginConfig.headerName
    val headerValue = pluginConfig.headerValue
    pluginConfig.apply {
        onCall { call ->
            call.response.headers.append(headerName, headerValue)
        }
    }
}

class PluginConfiguration {
    var headerName: String = "Custom-Header-Name"
    var headerValue: String = "Default value"
}

// in the module
install(CustomHeaderPlugin) {
    headerName = "X-Custom-Header"
    headerValue = "Hello, world!"
}
```

## Handlers

- `onCall()`: gets the `ApplicationCall`; read request info, modify response headers.
- `onCallReceive()`: call `transformBody()` to transform the request body before `call.receive()` returns it. `TransformBodyContext.requestedType` tells which type was requested; `data` is the current body (a `ByteReadChannel`).
- `onCallRespond()`: runs when a route calls `call.respond`; use `transformBody()` to change the outgoing body.
- `onCallValidators()`: per-call validation. For nested routes, parent validators run before child ones, so a validator can use an authenticated principal. Install the route-scoped plugin inside the authenticated route.
- `on(Hook)`: other stages: `CallSetup`, `ResponseBodyReadyForSend`, `ResponseSent`, `CallFailed`, `AuthenticationChecked` (after credentials are checked; usable for authorization).

Body transformation (`onCallReceive` / `onCallRespond`):

```kotlin
val DataTransformationPlugin = createApplicationPlugin(name = "DataTransformationPlugin") {
    onCallReceive { call ->
        transformBody { data ->
            if (requestedType?.type == Int::class) {
                val line = data.readLine() ?: "1"
                line.toInt() + 1
            } else {
                data
            }
        }
    }
    onCallRespond { call ->
        transformBody { data ->
            if (data is Int) {
                (data + 1).toString()
            } else {
                data
            }
        }
    }
}
```

Route-scoped validator, installed inside `authenticate("auth") { install(UserValidationPlugin) ... }`:

```kotlin
val UserValidationPlugin = createRouteScopedPlugin("UserValidationPlugin") {
    onCallValidators { call ->
        val principal = call.principal<UserIdPrincipal>()
        if (principal != null) {
            call.application.log.info("Validating request for ${principal.name}")
        }
    }
}
```

## Share call state

Store values in `call.attributes` under an `AttributeKey`, for example to record a time in `onCall` and read it in `onCallReceive`:

```kotlin
val DataTransformationBenchmarkPlugin = createApplicationPlugin(name = "DataTransformationBenchmarkPlugin") {
    val onCallTimeKey = AttributeKey<Long>("onCallTimeKey")
    onCall { call ->
        val onCallTime = System.currentTimeMillis()
        call.attributes.put(onCallTimeKey, onCallTime)
    }

    onCallReceive { call ->
        val onCallTime = call.attributes[onCallTimeKey]
        val onCallReceiveTime = System.currentTimeMillis()
        println("Read body delay (ms): ${onCallReceiveTime - onCallTime}")
    }
}
```

## Configuration

Define a config class, pass it to `createApplicationPlugin(name, createConfiguration = ::MyConfig)`, and configure in `install(...) { }`. Config properties are mutable during installation, so copy them into local variables in the plugin body before use in handlers.

To read from `application.conf`/`application.yaml`, give the config class an `ApplicationConfig` constructor parameter, read values with `tryGetString()`, and set `configurationPath` (for example `http.custom_header`):

```kotlin
val CustomHeaderPluginConfigurable = createApplicationPlugin(
    name = "CustomHeaderPluginConfigurable",
    configurationPath = "http.custom_header",
    createConfiguration = ::CustomHeaderConfiguration
) { /* same body as above */ }

class CustomHeaderConfiguration(config: ApplicationConfig) {
    var headerName: String = config.tryGetString("header_name") ?: "Custom-Header-Name"
    var headerValue: String = config.tryGetString("header_value") ?: "Default value"
}
```

```yaml
http:
  custom_header:
    header_name: X-Another-Custom-Header
    header_value: Some value
```

## Application settings and state

- `applicationConfig?.host` / `.port` and `environment?.developmentMode` are available in the plugin body.
- Handlers can run concurrently: keep shared mutable state in thread-safe types such as `AtomicInteger`.
- All handlers are suspending. Blocking database calls should be wrapped in `withContext(Dispatchers.IO)`; clean per-call resources with `on(ResponseSent)`.
- Lifecycle events (for example `ApplicationStopped`) are handled via `on(MonitoringEvent(...))` to release plugin-owned resources:

```kotlin
on(MonitoringEvent(ApplicationStopped)) { application ->
    application.log.info("Server is stopped")
    // Release resources and unsubscribe from events
    application.monitor.unsubscribe(ApplicationStarted) {}
    application.monitor.unsubscribe(ApplicationStopped) {}
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-custom-plugins.md, codeSnippets/snippets/custom-plugin/src/main/kotlin/com/example/plugins/CustomHeaderPlugin.kt, codeSnippets/snippets/custom-plugin/src/main/kotlin/com/example/plugins/CustomHeaderPluginConfigurable.kt, codeSnippets/snippets/events/src/main/kotlin/com/example/plugins/ApplicationMonitoringPlugin.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
