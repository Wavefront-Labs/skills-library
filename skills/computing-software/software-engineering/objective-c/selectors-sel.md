---
id: computing-software.software-engineering.objective-c.selectors-sel
name: selectors-sel
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-messaging, selectors-sel]
level: practitioner
status: docs-checked
description: "Create SEL values with @selector and NSSelectorFromString, test with respondsToSelector:, and vary messages with performSelector:."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocSelectors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selectors
**Goal:** build and call selectors dynamically and test the receiver first.

```objc
SEL setWidthHeight = @selector(setWidth:height:);
setWidthHeight = NSSelectorFromString(aBuffer);       // string to selector at runtime
NSString *method = NSStringFromSelector(setWidthHeight);

if ([anObject respondsToSelector:@selector(setOrigin::)])
    [anObject setOrigin:0.0 :0.0];
```
- A selector is the name of a method; compiled selectors have type `SEL`. All methods with the same name have the same selector, across classes, and a class method and an instance method with the same name share a selector.
- `@selector()` assigns the compiled selector at compile time and is the most efficient route; `NSSelectorFromString` converts a string at runtime and `NSStringFromSelector` converts back.
- The selector name includes the colons (`setWidth:height:`) and not return or parameter types. Let the system assign `SEL` values; valid selectors are never 0.
- `performSelector:`, `performSelector:withObject:` and `performSelector:withObject:withObject:` map directly to the messaging function: `[friend performSelector:@selector(gossipAbout:) withObject:aNeighbor]` equals `[friend gossipAbout:aNeighbor]`. They return `id`; a different return type must be cast, which works only for pointer-compatible types.
- `respondsToSelector:` (defined on `NSObject`) tests at runtime whether the receiver has a matching method; use it when the selector or the receiver's class is not known at compile time. Target-action (`setAction:`, `setTarget:`) is built on this mechanism.

## Gotchas
- Because dynamic binding finds return and parameter types from the selector, all implementations of identically named methods should share return and parameter types, except for statically typed receivers.
- A message to an object that cannot respond is an error that appears only at run time; an object may also forward messages it does not handle itself.

## Self-check
Guard each dynamically built selector with `respondsToSelector:` before sending it.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on selectors: `SEL`, `@selector`, `NSSelectorFromString`, `NSStringFromSelector`, shared selectors, `performSelector:` family, `respondsToSelector:`, target-action, forwarding note. Removed: ARC `performSelector` leak warning, IMP-cast pattern, `performSelector:afterDelay:` run-loop remark, `NSInvocation`, `@selector(foo)` versus `foo:` claim, compiler-flag self-check (not on the page). The page is a retired document.
Method: documentation only; no commands were run.
