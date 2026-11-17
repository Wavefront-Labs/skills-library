---
id: computing-software.software-engineering.cpp.overloading-and-default-arguments
name: overloading-and-default-arguments
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-functions, cpp-fn-overload, overload-resolution, default-arguments, adl, ambiguous-call, name-hiding, overloading-default-args]
level: practitioner
status: docs-checked
description: "Design C++ overload sets and default arguments safely: resolution ranking, ADL, name hiding, ambiguity, virtual defaults and alternatives like named parameters."
sources: ["https://en.cppreference.com/w/cpp/language/overload_resolution", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c162-overload-operations-that-are-roughly-equivalent", "https://en.cppreference.com/w/cpp/language/default_arguments", "https://en.cppreference.com/w/cpp/language/using_declaration", "https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html", "https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overloading and default arguments

## Overload resolution in short
Candidates are found by name lookup plus **ADL** (argument-dependent lookup: namespaces of the arguments' types), filtered by viability, then ranked per argument: exact match > promotion > conversion > user-defined conversion > ellipsis. Templates lose to non-templates on a tie. If no single best function exists the call is ambiguous.

```cpp
void log(int);
void log(double);
void log(const char*);
log(1);        // int
log(1.0f);     // float -> double is a promotion: log(double)
log('a');      // char -> int promotion
log(1L);       // error: ambiguous (long -> int and long -> double are both conversions)
```

## Guidance
- Overload operations that are roughly equivalent (C.162), and only those (C.163): `open(Gate&)` and `open(const char*, const char*)` for unrelated operations invite confusion, so give different meanings different names.
- Do not mix overloads with defaults in ways that make calls ambiguous: `f(int)` and `f(int, int = 0)`.
- By default declare single-argument constructors `explicit` (C.46) so overloads are not silently selected through conversions.

## Default arguments
```cpp
void connect(std::string host, int port = 443, bool tls = true);
```
- A default argument is evaluated each time the function is called with no argument for that parameter.
- Overriders of virtual functions do not acquire the base class's default arguments, and a virtual call uses the defaults of the **static** type of the object: do not give different defaults to a virtual function and its overrider (C.140).
- Changing a default does not change binary compatibility, but callers must be recompiled to use the new value (KDE binary compatibility policy).

## Gotchas
- `using Base::f;` in a derived class introduces all base-class member functions named `f`; a derived member with a matching signature hides or overrides the introduced one.
- GCC's `-Woverloaded-virtual` warns when a function declaration hides virtual functions from a base class (level 1 is included in `-Wall`; plain `-Woverloaded-virtual` selects level 2).

## Verify
- [ ] Table test each overload with int, long, float and char arguments and check which one is selected.
- [ ] Build with `-Wall -Woverloaded-virtual` (GCC) clean.

## Checked
2026-11-09. Confirmed on the cppreference overload resolution and default arguments pages, the C++ Core Guidelines (C.140: do not give virtual functions different default arguments), the GCC warning options page (-Woverloaded-virtual levels), cppreference using-declarations (using Base::f) and the KDE binary compatibility policy (callers must recompile when defaults change). Removed the incorrect claim that log(nullptr) is ambiguous and the claim that defaults are visible in the ABI.
Method: documentation only; no commands were run.
