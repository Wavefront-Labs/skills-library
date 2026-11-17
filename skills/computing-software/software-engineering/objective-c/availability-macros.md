---
id: computing-software.software-engineering.objective-c.availability-macros
name: availability-macros
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-preprocessor, availability-macros]
level: practitioner
status: docs-checked
description: "Guard newer APIs with @available, API_AVAILABLE, API_UNAVAILABLE and deprecation attributes for multi-OS deployment targets."
sources:
  - https://clang.llvm.org/docs/
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Availability
**Goal:** support older OS versions and guard newer API.

```objc
if (@available(macOS 10.12, iOS 10, *)) {
    [var fancyNewMethod];
} else {
    // fallback for old versions and unlisted platforms
}
API_AVAILABLE(macos(10.12)) void my_fun(NSSomeClass *var) { [var fancyNewMethod]; }
```
- Build against a new SDK but run on older systems with `-mmacos-version-min=` / `-miphoneos-version-min=`.
- `-Wunguarded-availability` warns when a call to API newer than the deployment target is not guarded. It is off by default; `-Wunguarded-availability-new` (only for APIs introduced in macOS 10.13, iOS 11, watchOS 4, tvOS 11 or later) is on by default.
- Guard with `if (@available(platform version, *))`. The `*` is required: unlisted platforms take the true branch, and the compiler warns for them against their deployment target. More than one platform may be listed.
- `@available()` is Objective-C only; use `__builtin_available()` in C and C++.
- A function that is only called on a new enough OS can carry an availability attribute such as `API_AVAILABLE(macos(10.12))`, which also suppresses the warning and requires callers to check.
- Replace older null checks and `-respondsToSelector:` guards with `@available()`.

## Self-check
Lower the deployment target and confirm an unguarded call warns.

## Checked
2026-11-02. Confirmed against the Clang "Language Extensions" page (Objective-C @available): version-min flags, `-Wunguarded-availability` and `-new` defaults, mandatory `*`, `__builtin_available`, attribute form. Removed: `API_DEPRECATED` / `API_UNAVAILABLE` examples, `NS_AVAILABLE` remarks, weak-link class check, Xcode deployment-target setting names and the iOS 15 / macOS 12 example versions (not on the page).
Method: documentation only; no commands were run.
