---
id: computing-software.software-engineering.ktor.ktor-di-resource-lifecycle-management
name: ktor-di-resource-lifecycle-management
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, dependency-injection, di, cleanup, autocloseable, lifecycle]
level: intro
status: docs-checked
description: "Clean up Ktor DI resources on shutdown: AutoCloseable auto-close, a custom cleanup function after provide, and key-scoped cleanup, with reverse-order teardown."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-di-resource-lifecycle-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manage resource lifecycle in Ktor DI

The Ktor DI plugin (`io.ktor:ktor-server-di`) handles lifecycle and cleanup automatically when the application shuts down. There are three ways to get cleanup.

## 1. AutoCloseable

Any dependency implementing `AutoCloseable` is closed automatically when the application stops, by default:

```kotlin
class DatabaseConnection : AutoCloseable {
    override fun close() {
        // Close connections, release resources
    }
}

dependencies {
    provide<DatabaseConnection> { DatabaseConnection() }
}
```

## 2. Custom cleanup function

For types that are not `AutoCloseable`, attach a `cleanup` function after the provider:

```kotlin
dependencies {
    provide<ResourceManager> { ResourceManagerImpl() } cleanup { manager ->
        manager.releaseResources()
    }
}
```

## 3. Scoped cleanup with key

Use `key` to manage named resources and their cleanup together:

```kotlin
dependencies {
    key<Closer>("second") {
        provide { CustomCloser() }
        cleanup { it.closeMe() }
    }
}
```

## Ordering

Dependencies are cleaned up in reverse order of declaration to ensure proper teardown.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-di-resource-lifecycle-management.md.

Removed or changed: dropped the extrapolated advice on declaring dependencies in build order; kept only the page's reverse-order cleanup statement.

Method: documentation only; no commands were run.
