---
id: computing-software.software-engineering.objective-c.enumerate-blocks
name: enumerate-blocks
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-enumeration, enumerate-blocks]
level: practitioner
status: gated
description: "Use enumerateObjectsUsingBlock: with options (concurrent, reverse), index sets, stop flag and predicates."
sources:
  - https://developer.apple.com/documentation/foundation
  - https://clang.llvm.org/docs/BlockLanguageSpec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block-based enumeration
**Goal:** index-aware or concurrent iteration.

```objc
[array enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop) {
    if ([obj isEqual:target]) { found = idx; *stop = YES; }
}];
[array enumerateObjectsWithOptions:NSEnumerationReverse usingBlock:^(id o, NSUInteger i, BOOL *s) { ... }];
[dict enumerateKeysAndObjectsUsingBlock:^(id key, id val, BOOL *stop) { ... }];
NSIndexSet *idxs = [array indexesOfObjectsPassingTest:^BOOL(id o, NSUInteger i, BOOL *s) { return [o length] > 3; }];
```
- `NSEnumerationConcurrent` may run block iterations in parallel on multiple threads; the block must be thread-safe and the order is not guaranteed. (gated: unconfirmed, source is paywalled or blocked)
- Set `*stop = YES` to end early (return is local to the block).
- Mutation of the collection inside the block raises the same exception.
- Filtering: `filteredArrayUsingPredicate:`; mapping is manual (`NSMutableArray` loop) in Foundation.
- Under ARC blocks run within an autorelease pool per call; create inner pools for long iterations.

## Gotchas
- `return` inside the block only exits the current iteration.
- Capturing `self` strongly is fine here (block does not escape).

## Self-check
Use NSEnumerationConcurrent with a shared mutable counter and confirm it races; fix with a lock or atomics.

## Checked
2026-11-02. Not confirmed: Foundation enumeration options and block parameters are documented only on Apple pages that were not readable. Claims left in place are unchecked; the first bullet carries the gate marker.
Method: documentation only; no commands were run.
