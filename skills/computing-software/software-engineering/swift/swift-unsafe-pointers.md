---
id: computing-software.software-engineering.swift.swift-unsafe-pointers
name: swift-unsafe-pointers
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-memory, unsafe-pointers]
level: advanced
status: draft
description: "Use Swift unsafe pointer and buffer types safely with scoped withUnsafe closures, correct lifetimes and bound memory."
sources: ["https://developer.apple.com/documentation/swift/unsafepointer", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unsafe pointers
Swift's unsafe types (`UnsafePointer<T>`, `UnsafeMutablePointer<T>`, `UnsafeBufferPointer<T>`, `UnsafeRawPointer`) bypass ARC and bounds checks. Use them for C interop and measured hot paths only.

```swift
var values = [1, 2, 3, 4]
values.withUnsafeMutableBufferPointer { buf in
    for i in buf.indices { buf[i] *= 2 }       // valid only inside the closure
}

let n = 8
let p = UnsafeMutablePointer<Int32>.allocate(capacity: n)
p.initialize(repeating: 0, count: n)
defer { p.deinitialize(count: n); p.deallocate() }

let raw = UnsafeRawPointer(p)
let bytes = raw.loadUnaligned(as: UInt32.self)   // Swift 5.7+
```

Rules:
- The pointer from `withUnsafe...` is valid only for the closure; never store or return it.
- Allocated memory has three states: uninitialised, initialised, deinitialised. Pair `allocate` with `deallocate`, and `initialize` with `deinitialize` for non-trivial types.
- Memory is bound to one type at a time; reinterpreting through a different typed pointer is undefined behaviour. Use `withMemoryRebound` or raw pointer `load`.
- `&array` passed to a C function parameter gives a temporary pointer, not a stable address.

Gotcha: undefined behaviour often "works" in debug and breaks under `-O`; Swift does not diagnose it.

Verify: run the code under the Address Sanitizer (`swift build -c debug -Xswiftc -sanitize=address`, or `swift test --sanitize=address`) and confirm no use-after-free or overflow reports.
