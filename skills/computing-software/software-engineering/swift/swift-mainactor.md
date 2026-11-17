---
id: computing-software.software-engineering.swift.swift-mainactor
name: swift-mainactor
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, mainactor]
level: practitioner
status: docs-checked
description: "Isolate UI-facing code to the main actor with @MainActor and global actors, and call it with await from elsewhere."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MainActor and global actors
The main actor protects the data used to show the UI. It is a global singleton instance of the `MainActor` type, so the type alone identifies the actor and isolation can be written as an attribute. You can define your own singleton global actors with `@globalActor`. The main actor is closely related to, but not the same as, the main thread; code on the main actor runs on the main thread.

```swift
@MainActor
func show(_: Data) {
    // ... UI code to display the photo ...
}

func downloadAndShowPhoto(named name: String) async {
    let photo = await downloadPhoto(named: name)
    await show(photo)          // await: switching to the main actor is a suspension point
}

let photo = await downloadPhoto(named: "Trees at Sunrise")
Task { @MainActor in           // closure isolated to the main actor
    show(photo)
}

struct PhotoGallery {
    @MainActor var photoNames: [String]   // fine-grained: only UI state
    var hasCachedPhotos = false
    @MainActor func drawUI() { }
    func cachePhotos() { }
}
```

- From code already on the main actor, call a `@MainActor` function synchronously; from elsewhere you must use `await`.
- Write `@MainActor` on a struct, class or enum to isolate all its methods and property access; write it on individual members for finer control.
- Annotating a protocol or base class with `@MainActor` implicitly marks conforming types and subclasses. Frameworks usually already do this for their UI protocols and base classes, so you do not repeat it on your own types.
- A property wrapper whose `wrappedValue` is `@MainActor` makes any property using it implicitly `@MainActor`.
- A common pattern is to do long-running work off the main actor and switch to it only to update the UI.

Verify: call a `@MainActor` function from a non-isolated async function and confirm the compiler requires `await`.

## Checked
2026-11-08: read the whole Concurrency chapter of The Swift Programming Language (swift-book source on GitHub); The Main Actor and Global Actors sections confirm every statement above. Removed: SE numbers and the SE-0316 source (not read), `nonisolated`, `assumeIsolated`, `MainActor.run`, Swift 6 mode error behaviour, Swift 6.2 default isolation, and the dispatchPrecondition / assertIsolated verification (none are on the page). The description no longer mentions MainActor.run and nonisolated.
Method: documentation only; no commands were run.
