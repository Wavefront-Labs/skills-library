---
id: computing-software.software-engineering.objective-c.associated-objects
name: associated-objects
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-categories, associated-objects]
level: advanced
status: docs-checked
description: "Back category properties with objc_setAssociatedObject, choose the right association policy, and avoid key and lifetime mistakes."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocAssociativeReferences.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Associated objects
**Goal:** store state on an instance from a category.

```objc
#import <objc/runtime.h>
static char kTagKey;
@implementation UIView (ABCTag)
- (NSString *)abc_tag { return objc_getAssociatedObject(self, &kTagKey); }
- (void)setAbc_tag:(NSString *)t {
    objc_setAssociatedObject(self, &kTagKey, t, OBJC_ASSOCIATION_RETAIN);
}
@end
```
- Associative references (OS X 10.6 and later) simulate adding instance variables to an existing class without changing its declaration, useful when you lack the source or cannot change the object layout.
- `objc_setAssociatedObject` takes the source object, a key, the value and a policy. The key is a `void *` and must be unique per association; the typical pattern is the address of a static variable.
- The policy says whether the value is assigned, retained or copied, and whether the association is atomic or non-atomic, like a declared property's attributes. `OBJC_ASSOCIATION_RETAIN` makes the host retain the value, so it stays valid at least as long as the host; it is released when the host is deallocated.
- Read with `objc_getAssociatedObject(obj, key)`.
- Break one association by calling `objc_setAssociatedObject` with a nil value (the policy then does not matter).
- `objc_removeAssociatedObjects` removes all associations, including ones set by other clients; Apple discourages it except to restore an object to "pristine condition".

## Gotchas
- Using the same key for two associations on one object overwrites the first; keep one static key per association.
- With a policy that does not retain, the value may be deallocated while still associated; reading it then raises a runtime exception.

## Self-check
Set a value with the retain policy, release the host in an autorelease pool, and confirm the value's dealloc ran.

## Checked
2026-11-08. Confirmed against Apple's archive Objective-C language guide, chapter Associative References (purpose, key rules, policy meaning, OBJC_ASSOCIATION_RETAIN lifetime, get, break, objc_removeAssociatedObjects advice). Removed the other policy constant names, the "@selector as key" and "ASSIGN is not weak" statements, the string-literal key remark and the NSCopying/archiving remark, which that page does not state. The example key now follows the page's static char pattern.
Method: documentation only; no commands were run.
