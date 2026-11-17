---
id: computing-software.software-engineering.objective-c.objective-c-plus-plus
name: objective-c-plus-plus
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-c-interop, objective-c-plus-plus]
level: advanced
status: draft
description: "Mix C++ and Objective-C in .mm files, keep C++ out of public headers and manage ownership of C++ members under ARC."
sources:
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Objective-C++
**Goal:** wrap C++ libraries for Objective-C/Swift consumers.

- Name files `.mm` (or compile as Objective-C++ with `-x objective-c++`).
- Hide C++ from public headers so pure Objective-C and Swift can import them: use a pimpl member in the `@implementation` or class extension.
```objc
// Wrapper.h  (pure Objective-C)
@interface ABCWrapper : NSObject
- (int)compute:(int)x;
@end
// Wrapper.mm
#include "engine.hpp"
@implementation ABCWrapper { std::unique_ptr<Engine> _engine; }
- (instancetype)init { if ((self = [super init])) { _engine = std::make_unique<Engine>(); } return self; }
- (int)compute:(int)x { return _engine->compute(x); }
@end
```
- C++ ivars are constructed/destroyed automatically with the Objective-C object (ARC and the runtime emit `.cxx_construct`/`.cxx_destruct`).
- Objective-C objects can be members of C++ classes (ARC manages them with `-fobjc-arc`); a C++ lambda can capture them.
- ARC and exceptions: Objective-C++ enables `-fobjc-arc-exceptions` by default.
- Do not mix `NSException` and C++ exceptions across boundaries.

## Gotchas
- A `.m` file importing a header containing C++ fails to compile.
- `nil` and `NULL`/`nullptr` are distinct; use `nil` for objects.

## Self-check
Import the wrapper header from a pure .m file; it must compile.
