---
id: computing-software.software-engineering.objective-c.fast-enumeration
name: fast-enumeration
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-enumeration, fast-enumeration]
level: intro
status: docs-checked
description: "Iterate collections with for...in, understand mutation-during-enumeration exceptions and implement NSFastEnumeration."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocFastEnumeration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast enumeration
**Goal:** loop over collections safely and quickly.

```objc
for (NSString *name in names) { ... }
for (NSString *key in dict) { id v = dict[key]; }      // iterates keys
for (id obj in [array reverseObjectEnumerator]) { ... }
```
- The expression must yield an object that conforms to `NSFastEnumeration`. NSArray, NSDictionary, NSSet and NSEnumerator adopt it; NSDictionary enumerates its keys.
- The enumerator has a mutation guard: modifying the collection during enumeration raises an exception. Iterate over a `copy`, or collect changes and apply them after the loop.
- Two forms: `for (Type newVar in expr)` and `Type existing; for (existing in expr)`. With the second form the variable is set to nil when the loop exhausts the collection; if you `break` early it keeps the last item visited.
- `break` and `continue` work as in a standard `for` loop.
- Order: for collections with a defined order (NSArray, or an NSEnumerator derived from one) enumeration follows that order, so counting iterations gives the index. NSEnumerator objects work too, and after a `break` you can continue with `nextObject`.
- Faster than using NSEnumerator directly.
- Because mutation is forbidden, you can run several enumerations concurrently.

## Gotchas
- The loop variable's declared type is not checked against the elements; heterogeneous collections need `isKindOfClass:`.
- Removing from an NSMutableArray in a forward index loop shifts indices; iterate backward or collect and remove afterwards.

## Self-check
Remove an element inside a for...in and confirm the exception, then fix it with a copy.

## Checked
2026-11-08. Confirmed against Apple's archive Objective-C language guide, chapter Fast Enumeration (syntax, NSFastEnumeration conformance, mutation guard, loop-variable value, ordering, NSEnumerator example). Corrected the claim that the variable keeps the last value (only true after an early exit; it is nil after exhaustion). Removed the exception name NSGenericException, the countByEnumeratingWithState:objects:count: selector, the nil-iterates-zero-times claim, the dictionary sorting hint and the "similar to indexed loops" speed claim, which that page does not state.
Method: documentation only; no commands were run.
