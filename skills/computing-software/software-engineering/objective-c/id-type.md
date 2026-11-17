---
id: computing-software.software-engineering.objective-c.id-type
name: id-type
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-types, id-type]
level: intro
status: docs-checked
description: "Use id, Class and static typing correctly, including isKindOfClass checks and class objects."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocObjectsClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# id and dynamic typing
**Goal:** know when `id` is appropriate and how to narrow it safely.

- `id` is the general type for any kind of object, including class objects. It is defined as a pointer to an object structure, so no `*` is used: `id anObject;`.
- `id` yields no information beyond "this is an object"; each object's `isa` variable lets the runtime find its class, so objects are dynamically typed at runtime.
- Static typing (`Rectangle *myRectangle;`) tells the compiler the object's class so it can type check, for example warn if the object appears unable to respond to a message. It does not defeat dynamic binding. An object may be statically typed to its own class or any class it inherits from.
- Narrowing at runtime:
```objc
if ([anObject isKindOfClass:[Rectangle class]]) { ... }
```
- `isMemberOfClass:` is true only for an instance of exactly that class; `isKindOfClass:` is true for the class or any class in its inheritance path.
- Class objects have type `Class` (or can be typed `id`): `Class aClass = [anObject class];`.
- The class name stands for the class object only as a message receiver; elsewhere send `class`. `NSClassFromString(className)` returns the class object, or `nil` if the string is not a valid class name.

## Gotchas
- Class names share a namespace with global variables and functions; a class and a global variable cannot have the same name.

## Self-check
Given an `id`, test it with `isKindOfClass:` before casting to a class pointer.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on objects, classes and messaging: `id`, `Class`, dynamic and static typing, type introspection, class objects, `NSClassFromString`, class-name namespace. Removed: `SEL` and `Protocol *` types, `respondsToSelector:`, ARC bridge casts, `instancetype` advice, JSON `NSNull` gotchas and selector-warning claims (not on the page). Page is marked a retired document.
Method: documentation only; no commands were run.
