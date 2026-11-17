---
id: computing-software.web-development.vapor.vapor-services-lifecycle-locks
name: vapor-services-lifecycle-locks
category: computing-software
field: web-development
product: vapor
tags: [vapor,vapor-services,lifecyclehandler,storagekey,locks,application,swift]
level: advanced
status: docs-checked
description: "Extend Vapor's Application and Request with read-only or stateful services, register LifecycleHandlers, and synchronise with LockKey locks."
sources:
  - https://docs.vapor.codes/advanced/services/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add your own services to `Application`/`Request`, hook boot and shutdown, and guard shared state.

**Read-only service**: a computed property on `Request` (or `Application`) that can use existing services.

```swift
extension Request {
    var myAPI: MyAPI {
        .init(client: self.client)
    }
}
// req.myAPI.foos()
```

**Writable service**: store state in `storage` under a `StorageKey`. An empty key type with a `Value` typealias controls who can access the value; an internal or private key keeps it to your code.

```swift
struct MyConfigurationKey: StorageKey {
    typealias Value = MyConfiguration
}

extension Application {
    var myConfiguration: MyConfiguration? {
        get { self.storage[MyConfigurationKey.self] }
        set { self.storage[MyConfigurationKey.self] = newValue }
    }
}
```

**Lifecycle.** Conform to `LifecycleHandler` (`willBoot`, `didBoot`, `shutdown`) and register it:

```swift
app.lifecycle.use(Hello())
```

**Locks.** Declare `struct TestKey: LockKey { }`, then `app.locks.lock(for: TestKey.self).withLock { ... }`. The same key always returns the same lock; the call is thread-safe. For an application-wide lock use `app.sync.withLock { ... }`.

**Request services.** Use the request's logger and event loop. A request must stay on the same event loop or an assertion is hit when the response returns; if a service leaves the loop, return with `hop(to:)` on the `EventLoopFuture`. Access application services through `req.application`; generally only read from requests, and protect writes with locks.

## Checked
Read the whole Services page (vapor/docs, docs/4.0/advanced/services.md, source of the cited page) on 2026-11-08. Confirmed read-only and writable services, StorageKey, LifecycleHandler methods and registration, LockKey locks, `app.sync`, and the request event-loop and `hop(to:)` guidance. No claims removed.
Method: docs-only read of cited pages, 2026-11-08
