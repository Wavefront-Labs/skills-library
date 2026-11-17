---
id: computing-software.software-engineering.objective-c.retain-release-rules
name: retain-release-rules
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-mrc, retain-release-rules]
level: practitioner
status: docs-checked
description: "Apply the manual reference counting ownership policy: you own what you alloc, new, copy, mutableCopy or retain, and must release or autorelease it."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmRules.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmPractical.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retain/release rules (MRC)
**Goal:** read and maintain reference-counted (non-ARC) code.

```objc
{
    Person *aPerson = [[Person alloc] init];   // you own it
    NSString *name = aPerson.fullName;         // not an owning method: do not release
    [aPerson release];
}
- (NSString *)fullName {
    NSString *string = [[[NSString alloc] initWithFormat:@"%@ %@",
                         self.firstName, self.lastName] autorelease];
    return string;
}
```
- You own any object you create with a method whose name begins with `alloc`, `new`, `copy` or `mutableCopy`.
- You can take ownership of a received object with `retain`: in an accessor or init method to store it as a property value, or to keep it from being invalidated as a side effect of another operation.
- When you no longer need an owned object you must relinquish it with `release` or `autorelease`; you must not relinquish an object you do not own.
- Use `autorelease` for a deferred `release`, typically when returning an object. `release` there would deallocate it before the caller could use it. Returning an `alloc`ed object without `autorelease` leaks, because nothing in the name tells the caller it owns it.
- Objects returned by reference (an `NSError **` argument) are not created by you, so you do not own them.
- A collection owns the objects it contains: adding retains, removing or releasing the collection releases. If you `alloc` a number to add it, release your own claim afterwards.
- Use accessors to set properties everywhere except initializer methods and `dealloc`, where you set the ivar directly.
- Do not use `retainCount` for logic; the result is often misleading because frameworks may also retain the object.

## Gotchas
- Over-release crashes later; under-release leaks.

## Self-check
For each `alloc`, `new`, `copy`, `mutableCopy` and `retain` in a function, find the matching `release` or `autorelease`.

## Checked
2026-11-03. Confirmed against Apple's Advanced Memory Management Programming Guide, "Memory Management Policy" and "Practical Memory Management" (ownership rules, autorelease, by-reference objects, collections, accessors in init and dealloc, retainCount). Removed: the setter retain-order and `EXC_BAD_ACCESS` remarks, and the Xcode analyzer self-check (not on those pages).
Method: documentation only; no commands were run.
