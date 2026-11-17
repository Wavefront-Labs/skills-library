---
id: computing-software.software-engineering.objective-c.designated-initializers
name: designated-initializers
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-initialization, designated-initializers]
level: practitioner
status: docs-checked
description: "Choose a designated initializer, have convenience initializers and init call it, call the superclass designated initializer, and use the self = [super init] pattern."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designated initializers
**Goal:** a consistent init chain that never leaves ivars half-set.

```objc
- (id)initWithFirstName:(NSString *)aFirstName lastName:(NSString *)aLastName
                                    dateOfBirth:(NSDate *)aDOB;      // designated
- (id)initWithFirstName:(NSString *)aFirstName lastName:(NSString *)aLastName {
    return [self initWithFirstName:aFirstName lastName:aLastName dateOfBirth:nil];
}
- (id)init {
    return [self initWithFirstName:@"John" lastName:@"Doe" dateOfBirth:nil];
}
```
- If a class declares several initializers, decide which is the designated initializer: often the one with the most options, called by the convenience initializers you write. Typically override `init` to call it with suitable defaults.
- When subclassing a class with multiple init methods, either override the superclass's designated initializer or add your own; either way call the superclass's designated initializer (in place of `[super init]`) before your own initialization.
- A typical init method assigns `self = [super init];` and then initializes inside `if (self) { ... }`.
- Access instance variables directly inside initializers: when a property setter runs the object may not be fully initialized, and a subclass may override the setter.
- When setting a `copy` property's ivar directly in an initializer, set a copy of the original object.

## Gotchas
- `init` can return a different object than the one `alloc` returned, so always assign the result to `self` and use it.

## Self-check
Trace every initializer to the designated one and check it calls the superclass's designated initializer exactly once.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Encapsulating Data" (designated initializer section, init pattern, direct ivar access in init, copy properties) and "Working with Objects" (init may return another object). Removed: `NS_DESIGNATED_INITIALIZER`, `NS_UNAVAILABLE`, `-Wobjc-designated-initializers` and the nil-return cleanup claims (not on those pages).
Method: documentation only; no commands were run.
