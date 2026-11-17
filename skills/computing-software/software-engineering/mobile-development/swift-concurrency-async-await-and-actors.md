---
id: computing-software.software-engineering.mobile-development.swift-concurrency-async-await-and-actors
name: swift-concurrency-async-await-and-actors
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, swift, swift-concurrency, async-await, actors, mainactor, sendable, task-groups]
level: practitioner
status: draft
description: "Use Swift concurrency on iOS: async/await, Task and task groups, actors for shared state, @MainActor for UI, Sendable checks and cancellation."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/", "https://developer.apple.com/documentation/swift/concurrency", "https://www.swift.org/migration/documentation/migrationguide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swift concurrency: async/await, actors, @MainActor

```swift
actor ImageCache {
    private var store: [URL: Data] = [:]
    func data(for url: URL) async throws -> Data {
        if let hit = store[url] { return hit }
        let (d, _) = try await URLSession.shared.data(from: url)
        store[url] = d            // re-check after await: state may have changed
        return d
    }
}

@MainActor final class FeedModel: ObservableObject {
    @Published var items: [Item] = []
    func load() async {
        do { items = try await api.fetchItems() } catch { /* surface error */ }
    }
}

func thumbnails(_ urls: [URL]) async throws -> [Data] {
    try await withThrowingTaskGroup(of: Data.self) { group in
        for u in urls { group.addTask { try await cache.data(for: u) } }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

## Key points
- An actor serialises access to its mutable state; calls from outside are `await`ed. Actor methods are reentrant at each `await`, so re-validate assumptions after suspension.
- `@MainActor` isolates a type or function to the main thread; UI view models should carry it.
- `Task { }` inherits actor context; `Task.detached` does not. Use `try Task.checkCancellation()` or `Task.isCancelled` in long loops; structured child tasks cancel with their parent (SwiftUI `.task {}` cancels when the view disappears).
- Types crossing isolation boundaries must be `Sendable`; value types with Sendable members qualify automatically.

## Gotchas
- Strict concurrency checking is opt-in via the `SWIFT_STRICT_CONCURRENCY` build setting (Swift 5.x) and default in Swift 6 language mode; migrate module by module.
- Blocking calls (semaphores, `Thread.sleep`) inside async code can starve the cooperative pool.

Verify: build with strict concurrency set to `complete` and fix warnings; add a test that cancels a task mid-flight and asserts no further state mutation.
