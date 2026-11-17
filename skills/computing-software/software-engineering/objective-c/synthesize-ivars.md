---
id: computing-software.software-engineering.objective-c.synthesize-ivars
name: synthesize-ivars
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-properties, synthesize-ivars]
level: practitioner
status: docs-checked
description: "Know when the compiler auto-synthesizes the _name ivar and when you must write @synthesize or @dynamic."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthesis and instance variables
**Goal:** understand the backing ivar generated for each property.

- By default a property gets synthesized accessors, and a readwrite property is backed by a synthesized instance variable named with an underscore prefix (`firstName` gives `_firstName`).
- The compiler synthesizes an ivar whenever it synthesizes at least one accessor. If you implement both the getter and the setter of a readwrite property, or the getter of a readonly one, it assumes you control the implementation and does not synthesize the ivar; request one with `@synthesize property = _property;`.
- `@synthesize propertyName = instanceVariableName;` picks the ivar name; `@synthesize firstName;` with no name makes the ivar `firstName`, without an underscore.
```objc
@implementation Foo
@synthesize title = _title;   // needed when both accessors are hand-written
- (void)setTitle:(NSString *)t { _title = [t copy]; [self refresh]; }
- (NSString *)title { return _title; }
@end
```
- Access ivars directly in initializer methods: when a property is set there the object may not be fully initialized, and a subclass may override the accessor.
- Ivars without a property can be declared in braces at the top of the class interface, implementation or class extension.
- A custom accessor for a property that uses an ivar must access that ivar directly (for example a lazy accessor).

## Gotchas
- With the atomic default you cannot mix a synthesized accessor with your own for the same property; the compiler warns (for example, a custom setter for an atomic readwrite property with a synthesized getter). `nonatomic` allows the mix.
- If a custom pair of accessors uses `_title` without `@synthesize`, the ivar does not exist.

## Self-check
Implement both accessors without `@synthesize`, check that `_title` is not available, then add the `@synthesize` line.

## Checked
2026-11-08. Confirmed against Apple's archive Programming with Objective-C chapter Encapsulating Data (synthesized accessors and ivars, underscore naming, custom ivar names, braces for non-property ivars, direct ivar access in initializers, no automatic ivar when both accessors are written, atomic mixing warning). Removed the `@dynamic` and protocol-only-property statements, the subclass-visibility remark and the quoted compiler error, which that chapter does not state.
Method: documentation only; no commands were run.
