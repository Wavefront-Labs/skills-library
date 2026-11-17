---
id: computing-software.software-engineering.objective-c.import-vs-include
name: import-vs-include
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-preprocessor, import-vs-include]
level: intro
status: draft
description: "Use #import for once-only inclusion, know when #include and guards are still needed, and organize import order."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# #import vs #include
**Goal:** avoid duplicate inclusion and circular headers.

- `#import` is `#include` that includes each file only once per translation unit; no include guards needed in Objective-C-only headers.
- Headers also consumed by C/C++ should keep include guards or `#pragma once`.
- Conventions: `#import "Local.h"` for project headers, `#import <Framework/Header.h>` for system and framework headers.
- Order in a .m file: its own header first (proves the header is self-sufficient), then system, then project headers.
- Use forward declarations (`@class`, `@protocol`) in headers; import in the implementation.
- Prefix header (`.pch`) precompiled headers are discouraged in new projects; modules replace them.
- Circular dependencies: break with forward declarations or protocols.

## Gotchas
- Importing the same header via two different paths (symlinks/copies) defeats once-only detection.
- Import cycles show up as "unknown type name" errors.

## Self-check
Compile each header alone (`clang -fsyntax-only -x objective-c-header Foo.h`) to ensure self-containment.
