---
id: computing-software.software-engineering.objective-c.nsdictionary-nsset
name: nsdictionary-nsset
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-text, nsdictionary-nsset]
level: intro
status: draft
description: "Use dictionaries, sets, ordered sets and counted sets with correct key requirements, hashing and equality."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSDictionary, NSSet and relatives
**Goal:** pick the right keyed or unique-collection type.

```objc
NSMutableDictionary<NSString *, NSNumber *> *d = [NSMutableDictionary dictionary];
d[@"a"] = @1;  [d removeObjectForKey:@"a"];
NSArray *keys = [[d allKeys] sortedArrayUsingSelector:@selector(compare:)];
NSSet<NSString *> *set = [NSSet setWithArray:array];     // unique
BOOL has = [set containsObject:@"x"];                    // O(1) average
NSOrderedSet *os = [NSOrderedSet orderedSetWithArray:array];
NSCountedSet *cs = [NSCountedSet set]; [cs addObject:@"a"]; NSUInteger n = [cs countForObject:@"a"];
```
- Dictionary keys are copied and must implement `NSCopying`, `hash` and `isEqual:` consistently; strings are the usual key.
- Dictionary and set iteration order is unspecified.
- Objects used as keys/members must not mutate their hash-relevant state while in the collection.
- Custom `isEqual:` requires a matching `hash` (equal objects must have equal hashes).
- `NSMapTable`/`NSHashTable` provide weak or pointer-identity semantics when needed.
- `NSOrderedSet` is ordered and unique but not an array subclass.

## Gotchas
- `objectForKey:` returns nil for missing keys (distinguish from `NSNull`).
- Setting `nil` via `setObject:forKey:` raises; use subscripting or `removeObjectForKey:`.

## Self-check
Override `isEqual:` without `hash` in a test and show a Set containing duplicates; then fix.
