---
id: computing-software.software-engineering.c.include-guards-and-header-hygiene
name: include-guards-and-header-hygiene
category: computing-software
field: software-engineering
product: c
tags: [c, include-guards, pragma-once, header-self-contained, forward-declaration]
level: practitioner
status: docs-checked
description: "Structure C headers with include guards, self-contained includes and minimal exposure."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/cpp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Include guards and header hygiene

Goal: headers that can be included in any order, once or many times.

- Guard every header: `#ifndef PROJ_FOO_H` / `#define PROJ_FOO_H` ... `#endif`, with a project-prefixed unique name. `#pragma once` is a less portable alternative (GCC CPP manual). In a user header, the guard macro name should not begin with `_` and should include the file name plus extra text.
- Self-contained: a header must compile when included first. Test by compiling a one-line file that includes only it.
- Include what you use; forward-declare structs (`struct foo;`) to break cycles and reduce rebuilds.
- Put declarations in headers, definitions in `.c` files. Define variables once; headers use `extern int g;`. `static` in a header duplicates per translation unit.
- `static inline` functions are fine in headers.
- Wrap in `extern "C" { }` guarded by `#ifdef __cplusplus` if C++ consumers exist.
- Keep private declarations out of the public header.

Verify: `for h in include/*.h; do echo "#include \"$h\"" | cc -fsyntax-only -x c - -Iinclude; done`.

## Checked

2026-11-02. Confirmed: wrapper `#ifndef` is the standard way to prevent double inclusion; `#pragma once` is the less portable alternative; guard-macro naming advice (GCC CPP manual, Once-Only Headers and Pragmas). Not checked: general header-design advice (self-contained headers, forward declarations, extern/static placement) is judgement, not a documented figure.

Method: documentation only; no commands were run.
