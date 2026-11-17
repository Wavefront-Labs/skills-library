---
id: computing-software.software-engineering.objective-c.protocol-conformance
name: protocol-conformance
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-protocols, protocol-conformance]
level: practitioner
status: docs-checked
description: "Adopt protocols in class or category declarations, test with conformsToProtocol:, and type variables as id<Protocol> for compile-time checking."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProtocols.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingWithProtocols/WorkingWithProtocols.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocol conformance
**Goal:** adopt and verify protocols correctly.

```objc
@interface Formatter : NSObject <Formatting, Prettifying>
@end
@interface ClassName (CategoryName) <Formatting>
@end

id <Formatting> anObject;
if ([anotherObject conformsToProtocol:@protocol(Paging)]) { /* ... */ }
```
- A class adopts a formal protocol by listing it in angle brackets after the superclass name, comma-separated for several. Categories adopt the same way: `@interface ClassName (CategoryName) <protocol list>`.
- A class or category that adopts a protocol must import the header where the protocol is declared, and must implement every required method or the compiler warns.
- A class conforms if it adopts the protocol or inherits from a class that does; instances conform to the same protocols as their class.
- `conformsToProtocol:` checks whether a protocol has been adopted (and presumably all its methods implemented), unlike `respondsToSelector:`, which tests a single method, and unlike `isKindOfClass:`, which tests the class hierarchy. Because it checks every method it can be more efficient than `respondsToSelector:`.
- Types can include protocols: `id <Formatting> anObject;` gives the compiler a more abstract level of type checking. Setting a property typed `id <Protocol>` to an object that does not conform yields a compiler warning.
- Only instances can be statically typed to a protocol, not class objects; at runtime classes and instances both respond to `conformsToProtocol:`.

## Gotchas
- Optional methods are not guaranteed by conformance; use `respondsToSelector:` for them.
- A protocol name only designates an object inside `@protocol()`.

## Self-check
Assign a non-conforming object to a property typed `id <Protocol>` and confirm the warning.

## Checked
2026-11-03. Confirmed against The Objective-C Programming Language, "Protocols" (adopting, conforming, conformsToProtocol:, type checking, categories adopting) and Apple's Programming with Objective-C, "Working with Protocols". Removed: `NSObject<P> *` constraint, generic `NSArray<id<P>>`, `@protocol()` link failure and duck-typing remarks (not on those pages).
Method: documentation only; no commands were run.
