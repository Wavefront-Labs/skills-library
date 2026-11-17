---
id: computing-software.software-engineering.objective-c.instancetype
name: instancetype
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-types, instancetype]
level: practitioner
status: draft
description: "Use instancetype for initializers and factory methods so subclasses get correct static types, and know related-result-type rules."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# instancetype
**Goal:** let the compiler infer the receiver's type for init-like methods.

```objc
+ (instancetype)personNamed:(NSString *)n;
- (instancetype)initWithName:(NSString *)n;
```
- `instancetype` is only valid as a method return type; it means "the receiver's class".
- Methods in the `alloc`, `init`, `new`, `self` families return related result type automatically even when written `id`; others need an explicit `instancetype` to get subclass-correct typing.
- With `id` returns, `Sub *s = [Sub factory]` compiles without a check; with `instancetype` the compiler gives a type error for mismatches.
- Always `return self` (or nil) from `init...` typed `instancetype`.
- Convenience constructors: `+ (instancetype)foo { return [[self alloc] init]; }` using `self` not the class name so subclasses work.

## Gotchas
- Using `[[Person alloc] init]` inside a class method hard-codes the class and breaks subclassing.
- `instancetype` cannot be used for variables or parameters.

## Self-check
Call a factory on a subclass and check `[result isKindOfClass:[Sub class]]`.
