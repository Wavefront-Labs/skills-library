---
id: computing-software.software-engineering.objective-c.framework-headers
name: framework-headers
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-modules, framework-headers]
level: practitioner
status: draft
description: "Control header visibility in frameworks with Public, Private and Project membership and the umbrella header rules."
sources:
  - https://developer.apple.com/documentation/xcode
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framework headers
**Goal:** expose exactly the intended API.

- Header roles in a target's Copy Headers phase: **Public** (shipped, importable by clients), **Private** (shipped in `PrivateHeaders`, for internal clients), **Project** (not shipped).
- The umbrella header (`<Framework>/<Framework>.h`) must import every Public header; clang warns "umbrella header does not include header" with `-Wincomplete-umbrella`.
- Inside a framework use `#import "Foo.h"` or `#import <Framework/Foo.h>`; clients must use the angle form `#import <Framework/Foo.h>`.
- Public headers may not import Project headers; they should not include private framework dependencies without declaring them.
- Forward declare (`@class`) in public headers to keep them light.
- Each public header should be self-contained (compilable alone); modules enforce that more strictly.
- Annotate public headers with `NS_ASSUME_NONNULL_BEGIN/END` and availability macros.

## Gotchas
- Swift clients only see headers reachable from the umbrella header.
- A header marked Public but not in the umbrella header is invisible to Swift and modules.

## Self-check
Build a client app that imports only `<Framework/Framework.h>` and uses every public class.
