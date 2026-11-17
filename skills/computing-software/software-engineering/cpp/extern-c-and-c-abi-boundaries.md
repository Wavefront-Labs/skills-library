---
id: computing-software.software-engineering.cpp.extern-c-and-c-abi-boundaries
name: extern-c-and-c-abi-boundaries
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-c-interop, cpp-ci-extern, extern-c, name-mangling, c-abi, opaque-handle, exceptions-across-boundaries, extern-c-boundaries]
level: practitioner
status: docs-checked
description: "Expose or consume C APIs from C++ with extern C: headers valid in both languages, opaque handles, language linkage rules and error-code returns."
sources: ["https://en.cppreference.com/w/cpp/language/language_linkage", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i26-if-you-want-a-cross-compiler-abi-use-a-c-style-subset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extern "C" and C ABI boundaries

Language linkage covers the calling convention and the name mangling algorithm needed to link with a unit written in another language; only "C++" (default) and "C" are guaranteed. Core Guidelines I.26: different compilers implement different binary layouts for classes, exception handling and function names, so use a C-style subset for a cross-compiler ABI (a single compiler can use full C++ in interfaces, which may need recompilation after a compiler upgrade).

```c
/* mylib.h : valid C and C++ */
#ifndef MYLIB_H
#define MYLIB_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct mylib_ctx mylib_ctx;                  /* opaque handle */
int  mylib_open(const char* path, mylib_ctx** out);  /* returns 0 or error code; never throws */
int  mylib_read(mylib_ctx*, void* buf, size_t len, size_t* got);
void mylib_close(mylib_ctx*);
#ifdef __cplusplus
}
#endif
#endif
```
```cpp
// mylib.cpp
struct mylib_ctx { std::ifstream f; };
extern "C" int mylib_open(const char* path, mylib_ctx** out) {
  try { *out = new mylib_ctx{std::ifstream(path)}; return (*out)->f ? 0 : 2; }
  catch (...) { return 1; }                          // report failure as a C error code
}
extern "C" void mylib_close(mylib_ctx* c) { delete c; }
```

## Rules
- Keep the signatures to C types: no `std::` types, references or overloads cross a C boundary.
- A shared header needs `#ifdef __cplusplus` around `extern "C"`, because `extern "C"` is not allowed in C (cppreference).
- `extern "C"` makes it possible to include header files declaring C library functions in a C++ program, and to define C++ functions callable from C code.
- Function types carry language linkage too, so pointers to functions keep it; the linkage of a function's name (mangling) and of its type (calling convention) are independent.
- A language specification can only appear at namespace scope; its braces do not establish a scope, and the innermost specification wins when they nest.

## Gotchas
- Two declarations that give an entity different language linkages are ill-formed (`extern "C" int f(); extern "C++" int f();`); a redeclaration without a specification inherits the earlier linkage.
- Class members and non-static member functions inside an `extern "C"` block keep C++ language linkage.
- `extern "C" int x;` is a declaration, not a definition, while `extern "C" { int x; }` is a definition.

## Verify
- [ ] The public header is included from both a C and a C++ translation unit.

## Checked
2026-11-03. Confirmed on cppreference Language linkage (two guaranteed linkages, name versus type linkage, conflicting declarations, scope rules, `__cplusplus` guard for shared headers) and Core Guidelines I.26. Removed: the claim that C++ has no stable ABI and C does (I.26 says only that compilers differ and that common ABIs are emerging), the rule that exceptions must be caught in each exported function, allocation ownership and CRT advice, export macros, `void* user_data` callbacks, the Windows 32-bit `__stdcall` note, template and overload linkage claim, layout `static_assert` advice, static initialiser note, and the `nm` and `cc -fsyntax-only` checks.
Method: documentation only; no commands were run.
