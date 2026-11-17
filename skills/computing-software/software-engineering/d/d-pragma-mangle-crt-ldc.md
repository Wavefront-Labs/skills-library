---
id: computing-software.software-engineering.d.d-pragma-mangle-crt-ldc
name: d-pragma-mangle-crt-ldc
category: computing-software
field: software-engineering
product: d
tags: [d-pragma-mangle-crt-ldc, pragmas, pragma-mangle, crt_constructor, ldc_attributes, linker-name, symbol-name, d]
level: advanced
status: docs-checked
description: "Set linker symbol names with pragma(mangle), run functions at C runtime startup with pragma(crt_constructor), and use LDC-only pragmas such as ldc_attributes."
sources:
  - https://dlang.org/spec/pragma.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pragma(mangle), crt_constructor and LDC pragmas

Goal: control exported names and early init.

- `pragma(mangle, "my_c_name") extern(D) void f();` overrides the mangled name of a function or variable (one compile-time string literal; other symbols are ignored). On macOS and Win32 an extra leading underscore is prepended to the string.
- `pragma(crt_constructor)` / `pragma(crt_destructor)` mark functions run after the C runtime is initialized and before the D runtime is initialized (destructor: the counterpart). The function must be `extern (C)`, take no parameters, not be a non-static member or nested function, and have a body. Order between such functions is implementation defined. The spec suggests it as a replacement for `shared static this` in betterC.
- `pragma(printf)`/`pragma(scanf)` mark an `extern (C)` or `extern (C++)` function as printf-/scanf-like so the compiler checks literal format strings against the arguments.
- Vendor-specific pragmas must be prefixed with the vendor's name (e.g. `pragma(DigitalMars_extension)`).

Gotchas:
- `crt_constructor` functions run before the D runtime library is initialized.

Verify: `nm` (or `dumpbin /symbols`) shows the chosen symbol name.

## Checked

Date 2026-11-02. Confirmed pragma mangle, crt_constructor, crt_destructor, printf and scanf (Pragmas spec). Corrected crt_constructor placement and requirements. Removed LDC/GDC attribute, set_attribute and mangle-validation claims.

Method: documentation only; no commands were run.
