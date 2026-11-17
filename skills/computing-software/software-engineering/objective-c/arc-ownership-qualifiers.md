---
id: computing-software.software-engineering.objective-c.arc-ownership-qualifiers
name: arc-ownership-qualifiers
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-arc, arc-ownership-qualifiers]
level: practitioner
status: docs-checked
description: "Apply __strong, __weak, __unsafe_unretained and __autoreleasing qualifiers and understand ARC retain/release insertion rules."
sources:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC ownership qualifiers
**Goal:** declare the right lifetime for variables.

```objc
__weak typeof(self) weakSelf = self;
NSString * __strong s = @"x";
__unsafe_unretained id raw = obj;      // no retain: dangling-pointer risk
```
- There are four ownership qualifiers: `__autoreleasing`, `__strong`, `__unsafe_unretained`, `__weak`.
- Property attributes map to them: `assign` implies `__unsafe_unretained`, `copy` implies `__strong` plus copy semantics in the setter.
- Methods in the `alloc`, `copy`, `init`, `mutableCopy` and `new` families are implicitly marked `ns_returns_retained`.
- Enable ARC with `-fobjc-arc`; disable with `-fno-objc-arc` (the last flag on the command line wins).

## Gotchas
- Mixed ARC/non-ARC files need correct flags per file in the build settings.

## Self-check
Compile with `-fobjc-arc -Wall` and confirm the intended flags apply per file.
## Checked
2026-11-02. Confirmed against the Clang "Objective-C Automatic Reference Counting" specification: qualifier list, property attribute mapping, method families, flags. Removed: __weak zeroing and OS-support remarks, forbidden-message list, `NSError **` rules and the retain/release/autorelease returning rules (not compared; Apple memory guide page was a thin summary).
Method: documentation only; no commands were run.
