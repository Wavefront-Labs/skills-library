---
id: computing-software.software-engineering.cpp.header-guards-include-order-and-odr
name: header-guards-include-order-and-odr
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-source, cpp-sf-headers, cpp-sf-odr, cpp-sf-namespaces, header-guards, include-order, odr, inline-variables, anonymous-namespace, header-guards-include-order, odr-inline-variables, namespaces-anonymous]
level: practitioner
status: docs-checked
description: "Structure C++ headers and sources: include guards, self-contained headers, what belongs in a header, ODR rules, inline variables and unnamed namespaces."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#sf-source-files", "https://en.cppreference.com/w/cpp/language/definition"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header guards, include order and the ODR

## Headers
```cpp
// widget.h
#ifndef LIBRARY_WIDGET_H      // guard name includes the library or component, not just the file name (SF.8)
#define LIBRARY_WIDGET_H
#include <string>             // a header includes all its own dependencies (SF.11)
class Widget { /* declarations only */ };
#endif // LIBRARY_WIDGET_H
```
- SF.8 says to use `#include` guards on every header and not to rely on `#pragma once`, which it calls non-standard and non-portable.
- Self-contained (SF.11): a header must work when included on its own. The enforcement note: a test should verify that the header compiles, or that a .cpp file which only includes the header compiles.
- A .cpp file must include the header(s) that define its interface (SF.5); put `#include`s before other declarations (SF.4).
- Do not write `using namespace` at global scope in a header (SF.7).
- A header may contain only: includes of other headers, templates, class definitions, function declarations, `extern` declarations, inline function definitions, `constexpr` definitions, `const` definitions and `using` aliases (SF.2).

## One Definition Rule
One and only one definition of every non-inline function or variable that is odr-used is required in the whole program; the compiler need not diagnose a violation but the behaviour is undefined (cppreference, Definitions and ODR). A class type, enumeration type, inline function, inline variable (since C++17) or templated entity may be defined in more than one translation unit if every definition consists of the same sequence of tokens (typically the same header) and the other listed conditions hold; otherwise the program is ill-formed, no diagnostic required.
```cpp
// config.h
inline constexpr int kMaxUsers = 100;      // C++17 inline variable: one entity across TUs
inline int helper(int x) { return x + 1; } // inline function
extern int g_count;                        // declaration; define once in a .cpp (prefer to avoid globals)
```
A variable or non-inline function defined in a header and included by two .cpp files gives linker errors (SF.2's `int x = 7;` example).

## Namespaces
- Internal entities: SF.22 prefers an unnamed namespace in the implementation file over `static`, since nothing external can depend on an entity in an unnamed namespace:
```cpp
namespace { constexpr int kRetries = 3; int helper(); }
```
- SF.21: do not use an unnamed namespace in a header; it is almost always a bug. Use a named namespace with `inline` functions instead.
- SF.20: use namespaces to express logical structure.

## Gotchas
- Class definitions whose token sequences differ between translation units violate the ODR with no required diagnostic.

## Verify
- [ ] Header self-containment test target builds each header on its own.

## Checked
2026-11-03. Confirmed on Core Guidelines SF.2, SF.4, SF.5, SF.7, SF.8, SF.11, SF.20-SF.22 and cppreference Definitions and ODR. Fixed: the skill recommended `#pragma once` (SF.8 recommends guards and calls pragma once non-portable) and cited SF.5 for the no-definitions rule (that is SF.2). Removed: the shell self-containment one-liner, clang-format `IncludeCategories` order and include-what-you-use advice, `inline namespace v1`, `#define NDEBUG` and `#ifdef DEBUG` layout claims, unity-build and PCH claims, symlink claim, `-Wodr` and ASan detection.
Method: documentation only; no commands were run.
