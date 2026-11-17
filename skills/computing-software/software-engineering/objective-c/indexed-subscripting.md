---
id: computing-software.software-engineering.objective-c.indexed-subscripting
name: indexed-subscripting
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-subscripting, indexed-subscripting]
level: practitioner
status: docs-checked
description: "Support obj[index] reads and writes in your own class by implementing objectAtIndexedSubscript: and setObject:atIndexedSubscript:."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Indexed subscripting
**Goal:** make `container[i]` work on your own class.

```objc
@interface ABCRing : NSObject
- (id)objectAtIndexedSubscript:(NSUInteger)idx;
- (void)setObject:(id)obj atIndexedSubscript:(NSUInteger)idx;
@end
ring[2] = @"x";          // [ring setObject:@"x" atIndexedSubscript:2]
id v = ring[2];          // [ring objectAtIndexedSubscript:2]
```
- An integral subscript on an object reads via `objectAtIndexedSubscript:` and writes via `setObject:atIndexedSubscript:`. The sends are type-checked like explicit sends.
- The getter takes an integral argument and returns an object pointer; the setter takes an object pointer first and an integral second argument. The class decides what indexes mean; the compiler coerces the index to the parameter type.
- A class need not declare both. `NSArray` declares only the getter, so assignment fails to type-check; `NSMutableArray` adds the setter.
- Reading an `NSArray` index outside `[0, count)` raises an exception. Assigning to an `NSMutableArray` index outside that range raises too; no syntax appends, inserts or removes.
- A subscript expression is always an l-value; compound assignment such as `+=` is ill-formed. Taking its address is an error.
- Object subscripting is supported only under the modern runtime; test with `__has_feature(objc_subscripting)`.

## Gotchas
- Subscripting is sugar: the methods can still be called directly.

## Self-check
Subscript a custom class with and without the setter declared and check which forms compile.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page (Object Subscripting): selectors, signatures, NSArray/NSMutableArray behaviour, l-value rules, modern runtime, feature macro. Removed: `m[m.count] = x` append claim (the page says out-of-range writes raise), `NSRangeException` name, any-integral-type wording beyond the page.
Method: documentation only; no commands were run.
