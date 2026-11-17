---
id: computing-software.software-engineering.objective-c.build-settings
name: build-settings
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-build, build-settings]
level: practitioner
status: draft
description: "Know the key Xcode build settings for Objective-C: ARC, modules, warnings, linker flags, deployment target and preprocessor macros."
sources:
  - https://developer.apple.com/documentation/xcode
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Objective-C build settings
**Goal:** configure targets via xcconfig, not manual clicking.

```
// Config/Base.xcconfig
CLANG_ENABLE_OBJC_ARC = YES
CLANG_ENABLE_MODULES = YES
CLANG_MODULES_AUTOLINK = YES
CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES
CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES
CLANG_WARN_STRICT_PROTOTYPES = YES
CLANG_ANALYZER_NONNULL = YES
GCC_TREAT_WARNINGS_AS_ERRORS = YES
GCC_PREPROCESSOR_DEFINITIONS = $(inherited) DEBUG=1
OTHER_LDFLAGS = $(inherited) -ObjC
IPHONEOS_DEPLOYMENT_TARGET = 15.0
```
- Per-file ARC opt-out: Build Phases > Compile Sources > Compiler Flags `-fno-objc-arc`.
- `OTHER_CFLAGS` / `WARNING_CFLAGS` accept raw clang flags such as `-Wall -Wextra`.
- Debug configs: `ONLY_ACTIVE_ARCH = YES`, `ENABLE_TESTABILITY = YES`; Release: `GCC_OPTIMIZATION_LEVEL = s` or `3`, `DEBUG_INFORMATION_FORMAT = dwarf-with-dsym`.
- `$(inherited)` preserves lower-level values; omit it and you lose project defaults.
- Print effective values with `xcodebuild -showBuildSettings`.

## Gotchas
- Setting names above are the keys Xcode writes; confirm exact names for new warnings in the Build Settings editor (hover shows the key).
- Bitcode is obsolete in recent Xcode releases.

## Self-check
Diff `xcodebuild -showBuildSettings` output before and after changing an xcconfig.
