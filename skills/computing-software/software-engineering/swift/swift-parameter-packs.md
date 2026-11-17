---
id: computing-software.software-engineering.swift.swift-parameter-packs
name: swift-parameter-packs
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-protocols, parameter-packs]
level: advanced
status: draft
description: "Write variadic generics with parameter packs (each/repeat) in Swift 5.9 and later, and know their limits."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/#Variadic-Generics", "https://github.com/swiftlang/swift-evolution/blob/main/proposals/0393-parameter-packs.md"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameter packs (variadic generics)
Introduced in Swift 5.9 (SE-0393, SE-0398, SE-0399). A pack abstracts over a list of types so a function can accept any number of differently typed arguments.

```swift
func allEqual<each T: Equatable>(_ lhs: repeat each T, to rhs: repeat each T) -> Bool {
    for (l, r) in repeat (each lhs, each rhs) {   // for-in over a pack expression: Swift 6.0
        if l != r { return false }
    }
    return true
}

func tuple<each T>(_ items: repeat each T) -> (repeat each T) {
    (repeat each items)
}
let t = tuple(1, "a", 2.0)   // (Int, String, Double)
```

- `each T` declares a type pack; `repeat each x` expands it at the use site.
- Two packs expanded together in one `repeat` must have the same length; the compiler checks this at the call.
- Requirements apply to every element: `<each T: Equatable>`.

Gotchas:
- Iterating a pack with `for ... in repeat` needs Swift 6.0; in 5.9/5.10 use a `repeat` expression inside a call or tuple construction.
- Packs cannot be stored in an array without erasing types; they are not a replacement for `[Any]`.
- Old code that wrote overloads for 2, 3, 4... arguments (the SwiftUI `buildBlock` pattern) can be collapsed to one pack declaration.

Verify: call the function with an empty list, one element and three mixed types, and confirm mismatched lengths in `allEqual` are rejected at compile time.
