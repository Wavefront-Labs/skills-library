---
id: computing-software.software-engineering.swift.swift-extensions
name: swift-extensions
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, extensions]
level: intro
status: docs-checked
description: "Add computed properties, methods, initialisers and conformances to existing types with extensions, and know what they cannot add."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/extensions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extensions
Extensions add behaviour to a class, struct, enum or protocol type you may not own (including standard library types) without subclassing. This is called retroactive modeling.

```swift
extension Double {
    var km: Double { self * 1_000 }          // computed property
    func rounded(toPlaces p: Int) -> Double {  // method
        let m = pow(10, Double(p)); return (self * m).rounded() / m
    }
}

struct Size { var w = 0.0, h = 0.0 }
extension Size {
    init(square: Double) { self.init(w: square, h: square) }  // keeps memberwise init
}

extension Array: Describable where Element: CustomStringConvertible { }  // extension with a generic where clause
```

What extensions can add: computed instance and type properties, instance and type methods, initialisers, subscripts, nested types, protocol conformances.
What they cannot add: stored properties, property observers on existing properties, or overrides of existing functionality.

Gotchas:
- If a value type provides defaults for all stored properties and defines no custom initialisers, an initialiser in an extension can call the default and memberwise initialisers. One written in the original body could not.
- For classes, extensions can add convenience initialisers but not designated initialisers or deinitialisers.
- For a struct declared in another module, an extension initialiser cannot access `self` until it calls an initialiser from the defining module.
- An extension initialiser must still fully initialise the instance.
- New functionality is available on all existing instances, even ones created before the extension.
- A `mutating` method added in an extension is marked `mutating` like any other.

Verify: compile the extension in a separate file and call each added member.

## Checked
2026-11-08: read the whole Extensions chapter of The Swift Programming Language (swift-book source on GitHub). Confirmed: the list of what extensions add and cannot add, the initialiser rules for value types, classes and other-module structs, availability on existing instances, mutating methods. Removed: the protocol-extension static dispatch gotcha and the name-collision gotcha (the Protocols chapter was not read), and the claim about conditional conformance verification.
Method: documentation only; no commands were run.
