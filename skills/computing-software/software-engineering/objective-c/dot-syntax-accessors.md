---
id: computing-software.software-engineering.objective-c.dot-syntax-accessors
name: dot-syntax-accessors
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-properties, dot-syntax-accessors]
level: intro
status: docs-checked
description: "Use dot syntax for declared properties as a wrapper over accessor calls, with the is-prefixed boolean getter, and access ivars directly only in init methods."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dot syntax and accessors
**Goal:** keep accessor naming and dot-syntax usage consistent.

```objc
@property (readonly, getter=isFinished) BOOL finished;
// somePerson.firstName is the same as [somePerson firstName]
// somePerson.firstName = @"Johnny" is the same as [somePerson setFirstName:@"Johnny"]
```
- Dot syntax is purely a convenient wrapper around accessor method calls, so property attributes still apply: setting a `readonly` property with dot syntax is a compiler error.
- By default the getter has the same name as the property (`firstName`) and the setter is `setFirstName:`.
- For Boolean properties it is customary for the getter to start with `is`; set it with the `getter=` attribute (`@property (getter=isFinished) BOOL finished;`).
- A property whose getter you write yourself and that has no setter (for example a readonly `fullName`) needs no instance variable; the compiler does not synthesize an ivar when you supply the accessors that would use it.
- Instance variables use an underscore prefix by default (`_firstName`). Best practice is to use accessors or dot syntax through `self` inside a class's own methods, except in initializer methods and custom accessors, where you access the ivar directly: setters can have side effects (such as KVC notifications) and the object may not be fully initialized.

## Gotchas
- A custom accessor for a property backed by an ivar must read or write the ivar (`_someImportantObject`) rather than calling the property again.
- Dot syntax calls the real accessors, so overridden accessors and KVO side effects run.

## Self-check
Search for `self.<prop>` inside that property's own accessors and inside `init` methods, and replace it with the ivar.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Encapsulating Data" (dot syntax as accessor wrapper, readonly error, `getter=isFinished`, underscore ivars, direct ivar access in init methods and custom accessors, synthesis rules). Removed: `get` prefix advice, `removeFromSuperview` advice, compound-assignment, nil dot access, struct-member write error, `setIsReady:` KVC claim (not on the page).
Method: documentation only; no commands were run.
