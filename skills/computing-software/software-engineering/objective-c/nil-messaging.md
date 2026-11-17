---
id: computing-software.software-engineering.objective-c.nil-messaging
name: nil-messaging
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-messaging, nil-messaging]
level: practitioner
status: docs-checked
description: "Rely on nil-message semantics correctly: zero return values for scalars, nil for objects, and the struct-return caveat."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocObjectsClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messaging nil
**Goal:** use nil messaging deliberately instead of scattering nil checks, while avoiding its traps.

- Sending a message to `nil` is valid and has no effect at runtime; several Cocoa patterns take advantage of this.
- If the method returns an object, the result is `nil`: `[[aPerson spouse] mother]` returns `nil` when `spouse` is `nil`.
- If the method returns any pointer type, an integer scalar no larger than `sizeof(void*)`, a `float`, `double`, `long double` or `long long`, the result is `0`.
- If the method returns a struct that the OS X ABI Function Call Guide says is returned in registers, every field is `0.0`. Other struct types are not zero-filled.
- For any other return type the value returned from a message to `nil` is undefined.
```objc
id anObjectMaybeNil = nil;
if ([anObjectMaybeNil methodThatReturnsADouble] == 0.0) { /* valid */ }
```

## Gotchas
- Do not rely on a zeroed result for a large struct return.

## Self-check
Write a test that sends a message to a nil object and asserts the zero return for each return type you use.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on objects, classes and messaging (Sending Messages to nil): no-op semantics, object, pointer, scalar and struct return rules, undefined otherwise. Removed: `[nilString length]` idiom, `isEqual:` pitfall, `NSNull` collection placeholder, nullability remark, nil delegate and array-literal gotchas (not on the page). Page is marked a retired document.
Method: documentation only; no commands were run.
