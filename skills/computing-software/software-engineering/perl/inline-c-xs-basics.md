---
id: computing-software.software-engineering.perl.inline-c-xs-basics
name: inline-c-xs-basics
category: computing-software
field: software-engineering
product: perl
tags: [perl, inline-c, xs, xsubpp, perlxstut, h2xs, inline-c-xs-basics]
level: sme
status: draft
description: "Extend Perl in C with Inline::C for prototypes and XS (perlxs, perlxstut) for distributions: structure, typemaps, build."
sources: ["https://perldoc.perl.org/perlxs", "https://perldoc.perl.org/perlxstut", "https://perldoc.perl.org/perlapi", "https://metacpan.org/pod/Inline::C"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inline::C and XS basics

**Goal:** choose and start the native-extension path.

## Inline::C (quick, development/prototype)
```perl
use Inline C => <<'END_C';
int add(int a, int b) { return a + b; }
SV *greet(char *name) { return newSVpvf("hello %s", name); }
END_C
print add(2, 3), " ", greet("x"), "\n";
```
Code is compiled on first run into `_Inline/` (set `use Inline Config => DIRECTORY => ...`); needs a C compiler on the user's machine. For distribution, ship via `Inline::Module` or convert to XS.

## XS skeleton
```bash
h2xs -A -n My::Ext            # creates lib/, Ext.xs, Makefile.PL, typemap placeholder
```
```c
/* Ext.xs */
#include "EXTERN.h"
#include "perl.h"
#include "XSUB.h"
#include "ppport.h"                       /* Devel::PPPort: compatibility macros across Perl versions */

MODULE = My::Ext   PACKAGE = My::Ext

int
add(a, b)
    int a
    int b
  CODE:
    RETVAL = a + b;
  OUTPUT:
    RETVAL
```
```bash
perl Makefile.PL && make && make test    # xsubpp translates .xs to C; MakeMaker compiles the shared object
```

## Rules
- Read perlxstut (tutorial), perlxs (reference), perlguts (SV/AV/HV internals), perlapi, perlcall (calling Perl from C).
- Reference counts are the main source of bugs: `SvREFCNT_inc/dec`, `sv_2mortal`; check with `Test::LeakTrace`.
- Use typemaps (`typemap` file) for custom types, `ExtUtils::ParseXS` is the translator.
- Generate `ppport.h` with `perl -MDevel::PPPort -e 'Devel::PPPort::WriteFile'`.
- Alternatives that avoid writing C: FFI::Platypus, Inline with other languages (Inline::Python etc.), Perl modules calling subprocesses.
- Thread safety (`dTHX`, `pTHX_`) matters for threaded perls.
- Test on several Perl versions and on Windows if you publish; build failures there are common.

## Self-check
- [ ] `add(2,3)` returns 5 and `perl -MTest::LeakTrace -e` shows no leaks around calls.
