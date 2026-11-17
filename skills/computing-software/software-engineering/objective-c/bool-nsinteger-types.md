---
id: computing-software.software-engineering.objective-c.bool-nsinteger-types
name: bool-nsinteger-types
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-types, bool-nsinteger-types]
level: intro
status: draft
description: "Use BOOL YES/NO, NSInteger/NSUInteger, CGFloat and NSNotFound correctly across 32/64-bit and in format strings."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BOOL, NSInteger and friends
**Goal:** avoid platform-width and truthiness bugs.

- `BOOL` values are `YES`/`NO`. On 64-bit ARM Apple platforms `BOOL` is a C `bool`; on some other platforms it is `signed char` (an int-sized truthy value can be truncated). Always write `if (x)` or `x != 0`, never `x == YES`.
- Convert: `BOOL b = (ptr != nil);` or `!!value`.
- `NSInteger`/`NSUInteger` follow pointer width (`long`/`unsigned long` on 64-bit). Format with `%ld`/`%lu` and cast: `[NSString stringWithFormat:@"%ld", (long)n]`.
- `NSNotFound` is `NSIntegerMax`; compare ranges with it: `[a indexOfObject:x] != NSNotFound`.
- `CGFloat` is `double` on 64-bit, `float` on 32-bit.
- Comparing unsigned: `array.count - 1` underflows when empty; check `count` first.
- Use `NSComparisonResult` (`NSOrderedAscending/Same/Descending`) in comparators.

## Gotchas
- `%d` with `NSInteger` triggers format warnings on 64-bit; use `-Wformat`.
- `NSUInteger i = -1` becomes huge.

## Self-check
Compile for arm64 and x86_64 with `-Wformat -Wsign-compare` and fix all warnings.
