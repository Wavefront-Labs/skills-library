---
id: computing-software.software-engineering.objective-c.clang-compile
name: clang-compile
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-build, clang-compile]
level: intro
status: draft
description: "Compile and link Objective-C with clang, ARC and frameworks, produce object files, and pick SDKs with xcrun on macOS."
sources:
  - https://clang.llvm.org/docs/
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiling with clang
**Goal:** build a command-line Objective-C program without Xcode.

```bash
clang -fobjc-arc -Wall -Wextra -framework Foundation main.m -o hello
./hello
xcrun --sdk iphonesimulator --show-sdk-path                 # path of an SDK
xcrun clang -fobjc-arc -isysroot "$(xcrun --sdk macosx --show-sdk-path)" -c Foo.m -o Foo.o
clang -fobjc-arc -fmodules -c Foo.m -o Foo.o                # modules instead of header parsing
clang -fobjc-arc -g -O0 -fsanitize=address main.m -framework Foundation -o hello_asan
```
- `-ObjC` is a linker flag for static libraries that contain categories.
- Preprocess/inspect: `clang -E`, `clang -S -emit-llvm`, `clang -Xclang -ast-dump -fsyntax-only Foo.m` (AST), `clang -fobjc-arc -S` to see retain/release calls.
- Objective-C is selected by the `.m` extension; `.mm` for Objective-C++; force with `-x objective-c`.
- Deployment target: `-mmacosx-version-min=<ver>` / `-mios-version-min=<ver>` (or `-target <triple>`).
- `-fobjc-arc` toggles ARC; `-fno-objc-arc` disables it per file.

## Gotchas
- Missing `-framework Foundation` gives undefined symbols for `NSLog` and `_OBJC_CLASS_$_NSObject`.
- On Linux, clang needs a GNUstep or other runtime; see the GNUstep skills.

## Self-check
Compile a hello-world with `-Wall -Werror` and run it; confirm exit code 0.
