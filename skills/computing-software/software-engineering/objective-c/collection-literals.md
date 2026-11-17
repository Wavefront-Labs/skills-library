---
id: computing-software.software-engineering.objective-c.collection-literals
name: collection-literals
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-literals, collection-literals]
level: intro
status: docs-checked
description: "Use @[...] and @{...} literals, understand that they create immutable collections, and handle nil elements."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Collection literals
**Goal:** create immutable arrays and dictionaries concisely.

```objc
NSArray *a = @[ @"Hello", NSApp, [NSNumber numberWithInt:42] ];
NSDictionary *d = @{ @"name": NSUserName(), @"date": [NSDate date] };
```
- `@[...]` expands to `+[NSArray arrayWithObjects:count:]`; `@{...}` to `+[NSDictionary dictionaryWithObjects:forKeys:count:]`. Both validate that no object or key is `nil`, unlike the variadic `arrayWithObjects:` and `dictionaryWithObjectsAndKeys:`, which use `nil` as a terminator.
- Elements must be Objective-C object pointer expressions. Dictionary keys must be object pointers implementing `<NSCopying>`.
- Neither keys nor values may be `nil`: a warning when the compiler can prove it, otherwise a runtime error.
- The results are immutable containers.
- Feature tests: `__has_feature(objc_array_literals)`, `__has_feature(objc_dictionary_literals)`.

## Gotchas
- A variable that happens to be `nil` fails at runtime; guard it or substitute a placeholder object.

## Self-check
Feed a `nil` variable into a literal in a test and confirm the runtime error.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page: expansion methods, nil validation, key/value type rules, feature macros. Removed: `mutableCopy` advice, `NSInvalidArgumentException` name, duplicate-key and evaluation-order claims, empty literal remarks (not on the page).
Method: documentation only; no commands were run.
