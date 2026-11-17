---
id: computing-software.software-engineering.objective-c.nsnumber-literals
name: nsnumber-literals
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-literals, nsnumber-literals]
level: intro
status: docs-checked
description: "Write @42, @3.14, @YES, @'c' and @(expression) NSNumber literals, and know the underlying numberWith methods."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# NSNumber literals
**Goal:** create NSNumber objects with literal syntax.

```objc
NSNumber *c = @'Z';          // numberWithChar:
NSNumber *i = @42;           // numberWithInt:
NSNumber *u = @42U;          // numberWithUnsignedInt:
NSNumber *l = @42L;          // numberWithLong:
NSNumber *ll = @42LL;        // numberWithLongLong:
NSNumber *f = @3.141592654F; // numberWithFloat:
NSNumber *d = @3.1415926535; // numberWithDouble:
NSNumber *b = @YES;          // numberWithBool:
NSNumber *e = @(INT_MIN);    // parenthesised: boxed expression
```
- A character, numeric or boolean literal prefixed with `@` evaluates to an `NSNumber` pointer; C type suffixes control the literal's size.
- Only literal scalars may follow `@` directly: `@INT_MAX` works but `@INT_MIN` does not (it expands to a parenthesised expression); use `@(INT_MIN)`.
- A `long double` literal such as `@123.23L` is rejected by the compiler.
- Objective-C++ also accepts `@true` and `@false`, equivalent to `@YES` and `@NO`.
- Feature test: `__has_feature(objc_bool)` for the `@YES` / `@NO` keywords (`__objc_yes`, `__objc_no`).

## Gotchas
- Objects made from literals are not guaranteed to be uniqued, nor newly allocated, so comparing them with `==` is not well defined; use `isEqual:` or `compare:`.

## Self-check
Check no code compares literal objects with `==`.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page: literal-to-factory mapping and suffixes, `@INT_MAX` vs `@INT_MIN`, long double rejection, `@true`/`@false` in Objective-C++, `objc_bool` feature check, `==` caveat. Removed: extraction and comparison method lists, tagged-pointer remark, `@(someBool)` and `@(enumValue)` claims (not stated; the page says enums box by their underlying type).
Method: documentation only; no commands were run.
