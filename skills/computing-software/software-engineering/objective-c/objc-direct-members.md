---
id: computing-software.software-engineering.objective-c.objc-direct-members
name: objc-direct-members
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-attributes, objc-direct-members]
level: advanced
status: gated
description: "Use __attribute__((objc_direct)) and objc_direct_members to make methods statically dispatched, and objc_subclassing_restricted to seal classes."
sources:
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct methods and sealed classes
**Goal:** cut dispatch overhead and shrink the method surface for internal methods.

```objc
__attribute__((objc_direct_members))
@interface ABCParser : NSObject
- (void)parseBytes:(const char *)p;                         // direct: no selector, not overridable
- (void)hook __attribute__((objc_direct));                  // single method
@end
__attribute__((objc_subclassing_restricted)) @interface ABCFinal : NSObject @end
```
- `objc_direct` (clang 11 and later) makes a method or property dispatched as a C function call: faster, not in the method list, not accessible via `performSelector:`, KVC, or swizzling, and cannot be overridden. (gated: unconfirmed, source is paywalled or blocked)
- Direct methods must be declared in the `@interface` (or class extension) of the class that implements them and cannot appear in protocols or categories (with limits; confirm in the clang attribute reference).
- `objc_direct_members` applies direct to all members of an interface or implementation; mark opt-outs with `__attribute__((objc_direct))` absent or `dynamic`.
- Clang also has `-fobjc-disable-direct-methods-for-testing` to permit mocking in tests (unconfirmed exact spelling; check `clang --help`).
- `objc_subclassing_restricted` forbids subclassing and lets the compiler assume exact class.

## Gotchas
- Direct methods break mocking frameworks that rely on dynamic dispatch.
- Calls on `nil` receivers to direct methods still return zero (a nil check is emitted).

## Self-check
Try subclassing the restricted class and overriding a direct method; confirm compile errors.

## Checked
2026-11-02. Not confirmed: the Clang attribute reference page read does not describe `objc_direct`, `objc_direct_members` or `objc_subclassing_restricted`. Claims left in place are unchecked; the first bullet carries the gate marker.
Method: documentation only; no commands were run.
