---
id: computing-software.software-engineering.prolog.foreign-c-interface
name: foreign-c-interface
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-interop, foreign-c-interface, pl-register-foreign]
level: sme
status: draft
description: "Extend SWI-Prolog with C using SWI-Prolog.h: PL_register_foreign, install function and load_foreign_library/1."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C foreign predicates
```c
#include <SWI-Prolog.h>
static foreign_t pl_hello(term_t a) {
  char *s; if (!PL_get_atom_chars(a, &s)) return PL_type_error("atom", a);
  Sprintf("hello %s\n", s); return TRUE; }
install_t install(void) { PL_register_foreign("hello", 1, pl_hello, 0); }
```
Build: `swipl-ld -shared -o hello hello.c` (or `gcc -shared -fPIC $(swipl --dump-runtime-variables ...)`); load: `:- use_foreign_library(hello).`
## Gotchas
- Return `PL_type_error`/`PL_raise_exception` results, not plain `FALSE`, to report errors.
- Term references are valid only within the foreign call; use `PL_new_term_ref`.
- Non-deterministic foreign predicates need `PL_FA_NONDETERMINISTIC` and a context handle.
## Self-check
Compile and call the example; verify `hello(42)` raises a type error.
