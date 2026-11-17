---
id: computing-software.software-engineering.swift.swift-class-inheritance
name: swift-class-inheritance
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, class-inheritance]
level: practitioner
status: docs-checked
description: "Subclass, override, call super and prevent overriding with final in Swift classes; know when inheritance is the wrong tool."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/inheritance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance and overriding
Inheritance is what differentiates classes from other types in Swift. A subclass lists its superclass after a colon. Swift classes do not inherit from a universal base class: a class with no superclass is a base class.

```swift
class Vehicle {
    var speed = 0.0
    func describe() -> String { "travelling at \(speed) km/h" }
}
class Bicycle: Vehicle {
    var hasBasket = false
    override func describe() -> String { super.describe() + (hasBasket ? " with basket" : "") }
}
final class Tandem: Bicycle { }   // cannot be subclassed
```

Rules:
- Every override needs the `override` keyword. Without it the compiler reports an error, and with it the compiler checks that a matching declaration exists in a superclass.
- Reach the superclass version with `super.someMethod()`, `super.someProperty` or `super[someIndex]`.
- Any inherited property can be overridden with a custom getter (and setter), whether it is stored or computed in the superclass; you must state its name and type. A read-only inherited property can become read-write but not the reverse. A setter override needs a getter too; return `super.someProperty` to pass the value through.
- Property observers can be added to an inherited property, but not to an inherited constant stored property or read-only computed property, and not alongside an overriding setter for the same property.
- Mark a member `final` (`final var`, `final func`, `final subscript`) or a class `final` to forbid overriding or subclassing; breaking this is a compile-time error.

Gotcha: prefer protocols plus composition over deep hierarchies, since a type that is not a class cannot join a class hierarchy.

Verify: compile a deliberate typo in an override (without `override`) and confirm the error; call `describe()` through a `Vehicle`-typed variable holding a `Bicycle` and check the subclass version runs.

## Checked
2026-11-08: read the whole Inheritance chapter of The Swift Programming Language (swift-book source on GitHub). Confirmed: override keyword and compiler checks, super access, property getter/setter and observer override rules, `final`. Removed: the claims that final enables optimiser devirtualisation, the initialiser ordering rule before `super.init`, and `open` vs `public` for cross-module subclassing (not on this page).
Method: documentation only; no commands were run.
