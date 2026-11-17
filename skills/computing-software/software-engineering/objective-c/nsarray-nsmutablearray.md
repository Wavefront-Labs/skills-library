---
id: computing-software.software-engineering.objective-c.nsarray-nsmutablearray
name: nsarray-nsmutablearray
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-text, nsarray-nsmutablearray]
level: intro
status: draft
description: "Create, index, search, sort, filter and mutate arrays; know ordering guarantees, immutability and copy semantics."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSArray / NSMutableArray
**Goal:** idiomatic array use.

```objc
NSArray<NSString *> *a = @[@"b", @"a"];
NSArray *sorted = [a sortedArrayUsingSelector:@selector(localizedStandardCompare:)];
NSUInteger i = [a indexOfObject:@"a"];                         // NSNotFound if absent
NSArray *f = [a filteredArrayUsingPredicate:[NSPredicate predicateWithFormat:@"length > 0"]];
NSMutableArray *m = [a mutableCopy];
[m addObject:@"c"]; [m insertObject:@"z" atIndex:0]; [m removeObjectAtIndex:1];
id first = a.firstObject;                                      // nil when empty
```
- `objectAtIndex:` / `a[i]` raises `NSRangeException` out of range; `firstObject` and `lastObject` return nil safely.
- Arrays retain elements; elements cannot be nil (use `NSNull`).
- Sorting: `sortedArrayUsingDescriptors:` with `NSSortDescriptor`, `sortedArrayUsingComparator:`.
- Containment: `containsObject:` uses `isEqual:` (O(n)); use `NSSet` for repeated membership tests.
- `arrayByAddingObject:` creates a new array.
- Share arrays across threads only if immutable; mutable ones need external synchronization.

## Gotchas
- Mutating while enumerating raises an exception.
- `NSArray` containing `NSNumber` `@YES` and `@1` compare equal under `isEqual:`.

## Self-check
Verify `[@[] firstObject]` is nil and that `@[][0]` throws in a test.
