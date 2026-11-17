---
id: computing-software.software-engineering.objective-c.clang-tidy-objc
name: clang-tidy-objc
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-style-lint, clang-tidy-objc]
level: advanced
status: docs-checked
description: "Run clang-tidy's objc-* and google-objc-* checks on Objective-C sources with a compilation database."
sources:
  - https://clang.llvm.org/extra/clang-tidy/
  - https://clang.llvm.org/extra/clang-tidy/checks/list.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/avoid-nserror-init.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/dealloc-in-category.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/nsinvocation-argument-lifetime.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/super-self.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/missing-hash.html
  - https://clang.llvm.org/extra/clang-tidy/checks/objc/property-declaration.html
  - https://clang.llvm.org/extra/clang-tidy/checks/google/objc-avoid-nsobject-new.html
  - https://clang.llvm.org/docs/JSONCompilationDatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clang-tidy for Objective-C
**Goal:** lint Objective-C beyond compiler warnings.

```bash
clang-tidy -checks='-*,objc-*,google-objc-*' Sources/Foo.m -- -x objective-c -fobjc-arc -isysroot <sdk-path>
```
- The `objc-` checks listed for clang-tidy include `objc-assert-equals`, `objc-avoid-nserror-init`, `objc-dealloc-in-category`, `objc-forbidden-subclassing`, `objc-missing-hash`, `objc-nsdate-formatter`, `objc-nsinvocation-argument-lifetime`, `objc-property-declaration` and `objc-super-self`. What they do: `objc-missing-hash` flags `-isEqual:` without `-hash`; `objc-super-self` flags `[super self]` in initializers (call a superclass initializer instead); `objc-dealloc-in-category` flags `-dealloc` in a category, which overrides the class's own; `objc-avoid-nserror-init` flags `[[NSError alloc] init]` (use `errorWithDomain:code:userInfo:`); `objc-nsinvocation-argument-lifetime` wants `__unsafe_unretained` objects passed to `getArgument:atIndex:` and `getReturnValue:` under ARC; `objc-property-declaration` flags property names that are not lower camel case.
- `google-objc-avoid-nsobject-new` (forbids calling or overriding `+new`), `google-objc-global-variable-declaration`, `google-objc-function-naming` and `google-objc-avoid-throwing-exception` implement Google Objective-C style rules.
- `-checks=` takes comma-separated globs, `-` prefix removes; `.clang-tidy` (found in the closest parent directory of the source file) supplies `Checks:` and `CheckOptions:`; `--list-checks` lists the enabled checks (use with `-checks=*` for all).
- clang-tidy can reuse build flags from a `compile_commands.json` compilation database, which CMake generates with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` (or tools such as Bear). Flags after `--` are passed to the compiler.
- `--fix` applies suggested fixes; review the diff.

## Gotchas
- Check names change across LLVM releases; list them with `--list-checks`.

## Self-check
Run `clang-tidy --list-checks -checks='objc-*'` to confirm the checks exist in your version.

## Checked

2026-11-08. Confirmed against the clang-tidy index page (`-checks=` globs, `--list-checks`, `.clang-tidy` with `Checks` and `CheckOptions`, `--fix`, `compile_commands.json` search and `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`), the clang-tidy checks list (every objc-* and google-objc-* name above), the individual check pages for avoid-nserror-init, dealloc-in-category, nsinvocation-argument-lifetime, super-self, missing-hash, assert-equals, property-declaration and google-objc-avoid-nsobject-new, and the JSON Compilation Database page (CMake option, Bear). Removed as unconfirmed: `objc-forward-class-redeclaration` (page 404, absent from the list), xcpretty and Xcode distribution claims, and the `xcrun` SDK lookup.
Method: documentation only; no commands were run.
