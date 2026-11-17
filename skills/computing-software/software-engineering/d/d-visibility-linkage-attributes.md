---
id: computing-software.software-engineering.d.d-visibility-linkage-attributes
name: d-visibility-linkage-attributes
category: computing-software
field: software-engineering
product: d
tags: [d-visibility-linkage-attributes, attributes, private, package, protected, public, export, extern, final, override, abstract, visibility, d]
level: practitioner
status: docs-checked
description: "Control symbol visibility (private, package, protected, public, export), extern linkage, final, override, abstract and attribute scoping."
sources:
  - https://dlang.org/spec/attribute.html
  - https://dlang.org/spec/function.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visibility, linkage and storage attributes

Goal: expose only the intended API.

- Visibility: `private` is accessible only within the same module (not class-private); `package` extends `private` to modules in the same package, and `package(pkg.sub)` to the named package and its descendants; `protected` applies inside classes (same module or derived classes); `public` is the default; `export` makes a symbol accessible from outside the executable, shared library or DLL.
- Linkage: `extern(LinkageType)` where the type is `C`, `C++`, `D`, `Windows`, `System` or `Objective-C`; `extern(C++, ns)` places declarations in a C++ namespace.
- Class: overriding methods are marked `override`; `final` blocks overriding; an `abstract` member function must be overridden by a derived class.
- Forms: single `private int x;`, block `private { ... }`, label `private:` (applies to the rest of the scope).
- `deprecated("msg")` marks API; `align(N)` sets struct field alignment.

Gotchas:
- A class's `private` members are still visible to everything in the same module (friend semantics).
- Private member functions are implicitly final and cannot be overridden.

Verify: compile a second module that imports and touches the private name, expecting an error.

## Checked
Checked 2026-11-03 against the D spec Attributes page (linkage, visibility, `deprecated`, `align`) and Functions page (virtual functions). Removed: the `static` storage remark and the `final:` label remark (not on those pages).

Method: documentation only; no commands were run.
