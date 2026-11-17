---
id: computing-software.software-engineering.swift.swift-key-paths
name: swift-key-paths
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, key-paths]
level: practitioner
status: docs-checked
description: "Use Swift key path expressions as typed property references and as functions in map, sorted and similar calls."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/expressions/#Key-Path-Expression", "https://github.com/swiftlang/swift-evolution/blob/main/proposals/0249-key-path-literal-function-expressions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key paths
A key-path expression refers to a property or subscript of a type, written `\Type.path`. At compile time it becomes an instance of the `KeyPath` class. Read through it with the `subscript(keyPath:)` subscript, which every type has.

```swift
struct Person { var name: String; var address: Address }
struct Address { var city: String }

let p = Person(name: "Ada", address: .init(city: "London"))
let cityPath = \Person.address.city      // multi-component path
print(p[keyPath: cityPath])              // "London"

var q = p
q[keyPath: \.name] = "Grace"             // type name omitted where inference supplies it

let names = people.map(\.name)           // key path literal used as a (Person) -> String function
```

- The path can contain property names, subscripts, optional-chaining and forced-unwrapping components, in any order and number: `\[String].first?.count`, `\[String: [Int]].["prime"]![0]`.
- A subscript in a path needs a parameter type that conforms to `Hashable`. Values used in it are captured with value semantics, so changing a variable afterwards does not change the key path (unlike a closure).
- `\.self` is the identity key path: `compoundValue[keyPath: \.self] = (a: 10, b: 20)` changes the whole value.
- A key path expression with root `SomeType` and value type `Value` can stand where a function or closure of type `(SomeType) -> Value` is expected: `toDoList.filter(\.completed).map(\.description)`; `\.self` works with `compactMap`.
- Side effects in a key path (such as a function call inside a subscript) run once when the expression is evaluated, not on each use.

Gotcha: per SE-0249 (implemented in Swift 5.2), only key path literal expressions convert to functions. A stored `let kp = \User.email` cannot be passed to `map` directly; annotate it as a function type (`let f: (User) -> String = \.email`) or write `{ $0[keyPath: kp] }`.

Verify: compile a snippet using `people.map(\.name)`, and confirm that passing a stored key path variable to `map` is rejected.

## Checked
2026-11-08: read the Key-Path Expression section of the Expressions chapter of The Swift Programming Language (swift-book source on GitHub; rest of the large chapter not read) and all of SE-0249 (swift-evolution). Confirmed everything above. Removed: the `KeyPath` / `WritableKeyPath` / `ReferenceWritableKeyPath` / `PartialKeyPath` / `AnyKeyPath` hierarchy bullet, the Sendable key path gotcha, the claim that the standard library has no key-path `sorted` overload.
Method: documentation only; no commands were run.
