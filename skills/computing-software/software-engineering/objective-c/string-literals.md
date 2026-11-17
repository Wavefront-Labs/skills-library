---
id: computing-software.software-engineering.objective-c.string-literals
name: string-literals
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-literals, string-literals]
level: intro
status: docs-checked
description: "Write @'...' NSString literals, declare string constants with extern const, and use NS_STRING_ENUM style names."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# NSString literals and constants
**Goal:** define reusable string constants correctly.

```objc
// Header
extern NSString * const ABCNotificationDidUpdate;
// Source
NSString * const ABCNotificationDidUpdate = @"ABCNotificationDidUpdate";
```
- Compile-time string literals (`@"..."`) have historically been uniqued across translation units at link time. That is an implementation detail of the compiler and must not be relied on.
- Comparing literal object locations with `==`, `!=`, `<`, `<=`, `>` or `>=` is not well defined; call `isEqual:` (or `compare:`).
- If code depends on identity, use a global string constant (`NSString * const MyConst = @"..."`) or `isEqual:`.

## Gotchas
- `NSString * const` makes the pointer const; `NSString const *` makes the pointee const.

## Self-check
Search the code for `==` between strings and replace each with `isEqual:`.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page (Caveats): uniquing and comparison guidance, global string constant form. Removed: NSConstantString and deallocation claims, adjacent-literal concatenation, NS_TYPED_ENUM example, header `static` advice, macro-constant remarks (not on the page).
Method: documentation only; no commands were run.
