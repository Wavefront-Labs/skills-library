---
id: computing-software.software-engineering.d.d-interop-objc-and-abi
name: d-interop-objc-and-abi
category: computing-software
field: software-engineering
product: d
tags: [d-interop-objc-and-abi, interop, objective-c, extern-objc, abi, name-mangling, calling-convention, slice-layout, delegate-layout, vtable, d]
level: sme
status: draft
description: "Use extern(Objective-C) classes and selectors, and know D ABI facts: name mangling, calling conventions, struct/slice/delegate layout and dlang.org ABI chapter."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Objective-C interop and the D ABI (calling conventions, name mangling)

Goal: understand the binary layout when crossing languages.

- Objective-C (macOS/iOS, dmd and LDC): `extern(Objective-C) extern class NSObject { void* isa; static NSObject alloc() @selector("alloc"); NSObject init() @selector("init"); }`. Methods bind selectors with `@selector("name:arg:")`; D classes can implement Objective-C classes only as `extern(Objective-C)` subclasses with limitations (confirm).
- ABI facts: a D slice `T[]` is `{size_t length; T* ptr}`; a delegate is `{void* context; fnptr}`; a class reference is a pointer to an object whose first slot is the vtable pointer (then monitor); associative arrays are one pointer; `dchar/char/wchar` are code units.
- Mangling: `_D` prefix + module/function path + type encoding (`__traits(mangleof, f)`, `.mangleof`), different from C and C++; `extern(C)` names are undecorated (Windows 32-bit adds `_` and stdcall `@n`).
- Calling convention: default `extern(D)` is mostly the platform C convention with D-specific rules for argument order (confirm: reversed order for some non-variadic cases) and `ref`/hidden pointers; do not call across compilers using `extern(D)` unless the same compiler produced both.
- Document in the dlang.org spec chapter "Application Binary Interface".

Gotchas:
- Using `extern(D)` across a shared-library boundary couples both sides to compiler version.
- Struct return in registers vs hidden pointer follows platform ABI only for `extern(C)`.

Verify: print `__traits(mangleof, f)` and compare with the linker symbol table.
