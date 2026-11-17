---
id: computing-software.software-engineering.d.d-interop-cpp-extern-cpp
name: d-interop-cpp-extern-cpp
category: computing-software
field: software-engineering
product: d
tags: [d-interop-cpp-extern-cpp, interop, extern-cpp, cpp-interop, namespace, cpp-class, name-mangling, hc-header, cpp-templates, d]
level: sme
status: draft
description: "Bind C++ using extern(C++), extern(C++, ns) or extern(C++, \"ns\"), class vtables, mangling, templates instantiated in C++, and -HC header export."
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

# C++ interop: extern(C++), namespaces, classes and templates

Goal: call and be called from C++.

- `extern(C++, "ns::sub") { int f(int); }` (string namespace form is current; the old identifier form `extern(C++, ns)` is deprecated, confirm per version). Use `extern(C++, class)` / `extern(C++, struct)` to pick the C++ mangling for a name.
- D classes `extern(C++) class A { ... }` map to C++ classes with single inheritance, virtual methods in declaration order; D side must allocate with the C++ allocator if C++ frees it, or use a C++ constructor via `extern(C++) static A create()`.
- Templates: D can only call instances that exist in the C++ object code; declare `extern(C++) T tmpl(T)(T x);` and instantiate the exact args. Standard library types (std::string, std::vector) are not generally usable across the boundary (core.stdcpp has partial wrappers: `core.stdcpp.string`, `vector`, `new_`, `allocator`).
- Exceptions do not propagate between D and C++ (confirm per platform; DMC/MSVC special cases exist); catch at the boundary.
- Header from D: `dmd -HC -HCf=foo.h foo.d` (C++ header generation, confirm flags).
- Link with the C++ runtime: `-L-lstdc++`; keep the same compiler family/ABI (MSVC vs MinGW).

Gotchas:
- `int`, `long` map differently on Windows/Linux; use `c_long` and `cpp_long`.
- Value-type C++ classes (non-trivial copy) as D structs need careful copy/destructor wrapping.

Verify: small C++ library with a virtual class; call into D and back.
