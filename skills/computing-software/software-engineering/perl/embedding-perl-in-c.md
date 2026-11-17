---
id: computing-software.software-engineering.perl.embedding-perl-in-c
name: embedding-perl-in-c
category: computing-software
field: software-engineering
product: perl
tags: [perl, embedding-perl, perlembed, extutils-embed, perl-interpreter-api, call-perl-from-c, embedding-perl-in-c]
level: sme
status: docs-checked
description: "Embed the Perl interpreter in a C program per perlembed: perl_alloc, perl_parse, eval_pv, call_pv and build flags."
sources: ["https://perldoc.perl.org/perlembed", "https://perldoc.perl.org/perlcall", "https://perldoc.perl.org/perlguts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding Perl and calling out to Perl from other languages

**Goal:** run Perl code from a C host.

```c
#include <EXTERN.h>
#include <perl.h>
static PerlInterpreter *my_perl;
int main(int argc, char **argv, char **env) {
    char *embedding[] = { "", "-e", "0", NULL };
    PERL_SYS_INIT3(&argc, &argv, &env);
    my_perl = perl_alloc();
    perl_construct(my_perl);
    PL_exit_flags |= PERL_EXIT_DESTRUCT_END;
    perl_parse(my_perl, NULL, 3, embedding, NULL);
    eval_pv("print qq(hello from Perl\\n);", TRUE);       /* TRUE: croak on error */
    SV *sv = eval_pv("6 * 7", TRUE);                       /* run an expression, read the result */
    printf("%d\n", (int)SvIV(sv));
    perl_destruct(my_perl);
    perl_free(my_perl);
    PERL_SYS_TERM();
    return 0;
}
```
Build flags come from the installed Perl:
```bash
cc -o host host.c $(perl -MExtUtils::Embed -e ccopts -e ldopts)
```
Call a named sub with no arguments and ignore its result via `call_argv("showtime", G_DISCARD | G_NOARGS, args)`, as perlembed does; flags are discussed in perlcall.

## Rules (perlembed)
- Call `PERL_SYS_INIT3()` once, on `main`'s `argc`, `argv` and `env`, before creating the first interpreter, and `PERL_SYS_TERM()` once after freeing the last.
- `PL_exit_flags |= PERL_EXIT_DESTRUCT_END` runs END blocks in `perl_destruct` (even if `perl_parse` fails), so you do not need `perl_run`. Since Perl 5.7.2.
- To pass fewer than the real arguments, perlembed uses `{ "", "-e", "0" }` and `perl_parse(my_perl, NULL, 3, embedding, NULL)`.
- Use `eval_pv(code, TRUE)` and take its returned `SV *` for the value; `SvTRUE(ERRSV)` checks for errors, e.g. after `call_*` with `G_EVAL`.
- Wrap callbacks to Perl subs in `ENTER; SAVETMPS; ... FREETMPS; LEAVE;` as in perlembed's `call_pv("expo", G_SCALAR)` example (details in perlcall).
- Loading XS modules needs glue: pass an `xs_init` function as perl_parse's second argument; generate it with `perl -MExtUtils::Embed -e xsinit -- -o perlxsi.c`. It registers `DynaLoader::boot_DynaLoader`.
- Several interpreters: `PL_perl_destruct_level` defaults to 0 and `perl_construct` resets it, so set it to 1 before and after for a clean `perl_destruct` when you create more than one. For concurrent interpreters in threads, perlembed recommends building perl with `-Dusethreads -Duseithreads`.
- Setting `PL_origalen = 1` stops perl from writing to `argv` memory when a script assigns `$0`; perlembed's persistent example would otherwise segfault on read-only strings.
- In embedding code the API macros take `aTHX_` (see "Background and MULTIPLICITY" in perlguts).

## Self-check
- [ ] The host program prints `hello from Perl` and `42`.

## Checked
2026-11-09. perlembed searched section by section (initialisation macros, build command, eval_pv, call_pv, destruct level, xs_init, END blocks) and read in the matching passages; perlcall and perlguts were not read in full. Removed: `perl_run` from the example, the "one interpreter per thread" and "temporaries leak" assertions, alternatives (subprocess, FFI::Platypus, PerlEmbed) and the valgrind check.
Method: documentation only; no commands were run.
