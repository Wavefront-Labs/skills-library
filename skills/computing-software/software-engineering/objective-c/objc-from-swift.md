---
id: computing-software.software-engineering.objective-c.objc-from-swift
name: objc-from-swift
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-swift-interop, objc-from-swift]
level: practitioner
status: draft
description: "Make Swift types visible to Objective-C with @objc and @objcMembers, subclass NSObject, and know unsupported features."
sources:
  - https://developer.apple.com/documentation/swift
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# @objc from Swift
**Goal:** call Swift code from Objective-C.

```swift
@objc(ABCUser)                          // Objective-C name
@objcMembers
public class User: NSObject {
    public var name: String
    public init(name: String) { self.name = name }
    @objc(greetWithPrefix:) public func greet(prefix: String) -> String { "\(prefix) \(name)" }
}
```
- A class must inherit NSObject (directly or indirectly) to be usable from Objective-C.
- `@objc` on individual members or `@objcMembers` on the class exposes all members; `@objc` also enables selectors and KVC/KVO (with `dynamic`).
- Not available to Objective-C: generics, tuples, structs, enums with associated values, global functions, nested types (as such).
- Swift optionals of class type become `nullable` pointers; non-optional become `nonnull`.
- Swift `throws` methods appear with `NSError **`.
- Include the generated header only in .m files (see bridging-header).

## Gotchas
- Swift 4+ no longer infers `@objc` for NSObject subclasses automatically (only in specific cases like overrides/protocol requirements).
- Runtime dispatch requires `dynamic` for KVO and swizzling.

## Self-check
Build and confirm the method shows up in `<Module>-Swift.h`.
