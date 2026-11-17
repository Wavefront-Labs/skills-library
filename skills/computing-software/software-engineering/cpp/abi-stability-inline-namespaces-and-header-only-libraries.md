---
id: computing-software.software-engineering.cpp.abi-stability-inline-namespaces-and-header-only-libraries
name: abi-stability-inline-namespaces-and-header-only-libraries
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-tooling, cpp-tl-abi, abi-stability, inline-namespaces, header-only, pimpl, binary-compatibility, abi-compliance-checker]
level: practitioner
status: docs-checked
description: "Design C++ libraries for compatibility: what breaks the ABI, inline namespaces for versioning, d-pointer/pimpl, abi-compliance-checker, and header-only notes."
sources: ["https://en.cppreference.com/w/cpp/language/namespace#Inline_namespaces", "https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B", "https://lvc.github.io/abi-compliance-checker/", "https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dual_abi.html", "https://en.cppreference.com/w/cpp/language/inline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ABI stability, inline namespaces, header-only libraries

A library is binary compatible if a program linked dynamically to a former version keeps running with newer versions without recompiling. The rules below follow the KDE policy, which targets the most restrictive set of conditions across compilers (mostly the Itanium C++ ABI, plus MSVC mangling notes).

## What breaks binary compatibility (existing shared-library classes)
Do not, for an existing class or function:
- add, remove or reorder base classes; add, remove or reorder non-static data members; change a member's type (except where the size is guaranteed the same and no inline method uses it)
- add a virtual function to a class with no virtuals or virtual bases, or add virtuals to a non-leaf class; reorder or remove virtuals
- change a function's signature: parameter types, const/volatile qualifiers of the function or parameters, return type; extend it with another parameter even if that parameter has a default argument
- inline an existing function (including moving its body into the class definition)
- remove `noexcept` (unless it was unconditionally false)
- unexport or remove an exported class or function

Generally safe (per the same page): add new non-virtual functions that do not overload a non-overloaded function, add new classes, add static data members, make a function `noexcept`, and change the default arguments of a method (callers need recompiling to see the new values). Appending enumerators to an enum is safe unless the compiler then picks a larger underlying type, so give enums an explicit underlying type.

## Techniques
- **d-pointer (pimpl)**: forward-declare `class FooPrivate;`, keep `FooPrivate* const d;` in the class, define `FooPrivate` in the .cpp, create it in the constructors and delete it in the destructor. It lets you add private data later. Make constructors, the destructor and copy operations non-inline for a class meant to be extended.
- **Add new overloads instead of editing signatures**: add a new function with the new parameters and note that the two should merge later (`//BCI: merge with int b = 0`).
- **Inline namespaces** (C++11): declarations in `inline namespace v2 { }` are visible in the enclosing namespace, and different versions of a library template can live in different inline namespaces while users can still specialise through the parent namespace.
```cpp
namespace mylib {
inline namespace v2 {            // mylib::Widget resolves to v2::Widget
  struct Widget { /* new layout */ };
}
namespace v1 { struct Widget { /* old layout */ }; }
}
```
libstdc++ does something similar for its dual ABI: the new `std::list<int>` is defined as `std::__cxx11::list<int>`, so the old and new versions have different names for linkage. Linker errors mentioning `std::__cxx11` or `[abi:cxx11]` usually mean object files built with different values of `_GLIBCXX_USE_CXX11_ABI` are being linked together. Not every use changes symbol names (a class with a `std::string` member has the same mangled name), so compile with `-Wabi-tag` to be warned of potential incompatibilities.
- **ABI Compliance Checker** (`abi-compliance-checker`) compares two versions of a C/C++ library for binary and source compatibility problems such as v-table changes and removed symbols.

## Header-only libraries
Since C++17, `inline` variables (and `constexpr` static data members) may be defined in a header included by many translation units; cppreference notes this removes the main obstacle to header-only libraries. An inline function or variable with external linkage may be defined in several translation units only if all definitions are identical; differing definitions are ill-formed, no diagnostic required. Mark non-template functions defined in headers `inline`.

## Verify
- [ ] The ABI Compliance Checker report between releases shows no binary-incompatible changes for a patch release.
- [ ] A test links an old client binary against the new library and runs it.

## Checked
2026-11-09. Confirmed on the KDE Binary Compatibility page (what you can and cannot change, d-pointer steps, BCI merge note, explicit enum underlying types), the cppreference namespace page (inline namespaces since C++11, library versioning note) and inline page (inline variables since C++17, identical definitions rule), the libstdc++ dual ABI page (std::__cxx11, linker errors, -Wabi-tag) and the ABI Compliance Checker page (what it analyses). Removed as not on the pages read: the earlier claim that default arguments and noexcept changes break the ABI (the KDE page says default-argument changes and adding noexcept are safe), soname and version-script advice, abidiff, -fvisibility, extern "C" wrappers, the header-only pros and cons list and CMake snippet, and Debug/CRT gotchas.
Method: documentation only; no commands were run.
