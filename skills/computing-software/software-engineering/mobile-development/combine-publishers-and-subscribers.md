---
id: computing-software.software-engineering.mobile-development.combine-publishers-and-subscribers
name: combine-publishers-and-subscribers
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, swift, combine, publishers, subscribers, anycancellable, debounce, asyncsequence]
level: practitioner
status: draft
description: "Use Combine in iOS apps: publishers and operators, sink/assign, AnyCancellable storage, debounce for search, schedulers, and bridging to async/await."
sources: ["https://developer.apple.com/documentation/combine", "https://developer.apple.com/documentation/combine/receiving-and-handling-events-with-combine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combine publishers and subscribers

```swift
final class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published private(set) var results: [Item] = []
    private var bag = Set<AnyCancellable>()

    init(api: API) {
        $query
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .filter { $0.count >= 2 }
            .map { api.searchPublisher(term: $0).catch { _ in Just([]) } }
            .switchToLatest()                       // cancel the previous request
            .receive(on: DispatchQueue.main)
            .assign(to: &$results)                  // no AnyCancellable, tied to the object
    }
}
```

## Essentials
- Subscribing returns an `AnyCancellable`; if you drop it, the subscription is cancelled immediately. Store in a `Set<AnyCancellable>` or use `assign(to: &$property)`.
- `sink(receiveCompletion:receiveValue:)` for side effects; `assign(to:on:)` with `self` retains it (cycle), so prefer `assign(to: &$prop)` or `[weak self]` in sink.
- A failure completes the pipeline; recover with `catch`/`replaceError` inside `flatMap`/`map` so the outer stream survives.
- `receive(on:)` changes downstream delivery; `subscribe(on:)` changes upstream work.
- `@Published` is a publisher of the property's value, emitting in `willSet` (the property still has the old value inside the sink).

## Async bridge
Publishers expose `.values` as an `AsyncSequence`: `for await value in publisher.values { ... }`. For new code on iOS 17+/Swift 5.9, async sequences and the Observation framework replace many Combine uses; Combine is not deprecated.

## Gotchas
- Unbounded buffering: `.collect()` or slow subscribers can grow memory; use `.buffer` or `.throttle`.
- `Future` runs eagerly on creation; wrap in `Deferred`.

Verify: unit-test the pipeline with a `PassthroughSubject`, send "a", "ab", "abc" quickly and assert one request fires after the debounce.
