---
id: computing-software.software-engineering.d.d-extern-cpp-com-interfaces
name: d-extern-cpp-com-interfaces
category: computing-software
field: software-engineering
product: d
tags: [d-extern-cpp-com-interfaces, interfaces, com, extern-cpp-interface, iunknown, vtable, windows-com, cpp-interface, d]
level: sme
status: draft
description: "Declare extern(C++) and COM interfaces so D classes can implement or call foreign vtables: IUnknown, extern(Windows), IID layouts and lifetime rules."
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

# COM and C++ interfaces

Goal: interoperate through binary interfaces.

- `extern(C++) interface IFoo { void f(); }` lays out vtable like a C++ abstract class; implement in D with `extern(C++) class Foo : IFoo`.
- COM: `interface IUnknown { extern(Windows): HRESULT QueryInterface(const(GUID)* riid, void** ppv); uint AddRef(); uint Release(); }` derives from `core.sys.windows.com.IUnknown`.
- COM classes need reference counting and `QueryInterface` implementation; D's runtime GC does not manage COM lifetime, so root the object (e.g. `GC.addRoot`) or allocate manually.
- Method order in the interface defines vtable slots; keep identical to the C++/IDL header and test with a C++ caller.
- Multiple inheritance of C++ classes is not supported.
- Calling convention per platform: `extern(Windows)` is stdcall on 32-bit, otherwise same as the default.

Gotchas:
- Passing a GC pointer to C++ that retains it needs `GC.addRoot`/`addRange`.
- Destructors are not virtual across the boundary unless declared in the C++ interface.

Verify: round-trip test calling a method from a small C++ harness linked in.
