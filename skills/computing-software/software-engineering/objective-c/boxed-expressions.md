---
id: computing-software.software-engineering.objective-c.boxed-expressions
name: boxed-expressions
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-literals, boxed-expressions]
level: practitioner
status: docs-checked
description: "Box scalars, enums, C strings, structs with @(...) and know which types the compiler supports."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Boxed expressions
**Goal:** convert C values to objects with `@(...)`.

```objc
NSNumber *n = @(M_PI / 2);                // numberWithDouble:
NSString *s = @(getenv("PATH"));          // stringWithUTF8String:
typedef enum : unsigned char { Red, Green, Blue } Color;
NSNumber *g = @(Green);                   // numberWithUnsignedChar:
struct __attribute__((objc_boxable)) Point { int x, y; };
struct Point p;
NSValue *v = @(p);                        // NSValue valueWithBytes:objCType:
```
- `@(expr)` supports scalar (numeric, enumerated, `BOOL`), C string pointer and some C structure expressions.
- An enum value must be inside `@(...)`, not used directly after `@`. The `NSNumber` factory follows the enum's fixed underlying type, or the compiler-chosen integer type that holds all members.
- A `char *` / `const char *` expression boxes to an `NSString`; the data is assumed NUL-terminated and UTF-8.
- Passing `NULL` as the character pointer raises an exception at runtime; the compiler rejects it when it can see it.
- Struct boxing requires the structure to carry `objc_boxable`; a struct without it is an error. Add the attribute through a `typedef` for older headers.
- Feature tests: `__has_feature(objc_boxed_expressions)`, `__has_feature(objc_boxed_nsvalue_expressions)`, `__has_attribute(objc_boxable)`.

## Gotchas
- Check C string pointers for `NULL` before boxing when they can be null.

## Self-check
Box an enum, a `double`, a `BOOL`, a C string and a boxable struct; check each compiles.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page and the Clang attribute reference (`objc_boxable`): boxable types, enum rules, C string boxing, NULL behaviour, struct boxing and feature macros. Removed: pointer-boxing error claim, UIKit `NSValue` category remarks, unboxing method names (not on the pages).
Method: documentation only; no commands were run.
