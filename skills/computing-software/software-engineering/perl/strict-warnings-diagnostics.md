---
id: computing-software.software-engineering.perl.strict-warnings-diagnostics
name: strict-warnings-diagnostics
category: computing-software
field: software-engineering
product: perl
tags: [perl, use-strict, use-warnings, diagnostics, fatal-warnings, perltrap, strict-warnings-diagnostics, perl-pragmas]
level: intro
status: docs-checked
description: "Start every Perl file with strict and warnings, disable categories narrowly, treat FATAL warnings with care, and use the diagnostics pragma and splain."
sources: ["https://perldoc.perl.org/strict", "https://perldoc.perl.org/warnings", "https://perldoc.perl.org/diagnostics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strict, warnings and diagnostics

**Goal:** catch typos and bad data early.

```perl
use strict;               # all of: vars (declare variables), refs (no symbolic refs), subs (no barewords)
use warnings;             # lexically scoped, by category
use v5.36;                # use VERSION >= 5.11 implies strict; use v5.35 or above enables warnings
{
    no warnings 'uninitialized';          # narrowly, in a block
    no strict 'refs';                     # one strictness category off
}
use warnings qw(all -uninitialized);      # everything except one category
use warnings FATAL => qw(void);           # fatal for selected categories
use warnings FATAL => 'all', NONFATAL => 'syntax';   # downgrade one category again
```
```bash
perl -w script.pl                    # global $^W; also affects code you did not write
perl -c script.pl                    # check syntax and exit
perl -Mdiagnostics script.pl         # verbose explanations from perldiag
perl script.pl 2>diag.out; splain diag.out    # explain saved messages
perl -Mdiagnostics=-traceonly script.pl       # stack traces only, no explanations
```

## Rules
- `strict` effects are limited to the current file or scope block. Currently the restrictions are `vars` (compile-time error for variables not declared with `my`, `our`, `state` or `use vars`, or fully qualified; `$a` and `$b` are exempt), `refs` (runtime error on symbolic references) and `subs` (compile-time error on barewords, except in curly braces, left of `=>`, or with unary minus).
- `use warnings` is a more flexible, lexically scoped replacement for `-w` and `$^W`. `-w` is all or nothing and turns on warnings in modules you did not write; `$^W` is dynamically scoped and easy to change unexpectedly. Under `use warnings`, `$^W` and `-w` are ignored for that scope. `-W` enables all warnings everywhere, regardless of `no warnings`.
- The warnings docs say use of `FATAL => 'all'` is discouraged and is particularly risky; the perl5 porters strongly recommend understanding the risks first, especially in library code, because downstream users cannot change the choice. `use v5.20` or higher allows `use warnings 'FATAL'` as shorthand for the same thing, with the same advice.
- `warnings::register` creates a warnings category for a module, and `warnings::warnif` emits a warning in that category when the caller has enabled it; a plain `use warnings` enables even categories not yet registered.
- `use diagnostics` enables `-w`, sends the longer descriptions to STDERR, and shows each perldiag explanation only once. `no diagnostics` cannot turn it off at compile time; use `diagnostics->disable` and `->enable` at runtime. It also adds a stack trace when perl dies.

## Self-check
- [ ] `perl -e '$x=1'` is accepted but `perl -Mstrict -e '$x=1'` fails to compile (strict vars).

## Checked

Date: 2026-11-08. Confirmed against the strict, warnings and diagnostics pages on perldoc.perl.org: the three strict categories and their behaviour, use VERSION implying strict (5.11 and later) and warnings (5.35 and later), warnings category syntax, FATAL and NONFATAL, the FATAL => 'all' discouragement, the 5.20 `use warnings 'FATAL'` shorthand, the -w, $^W and -W discussion, warnings::register and warnif, and the diagnostics and splain usage. Removed: error-message strings, the claim that `no strict 'refs'` is needed to install subs via globs, advice naming particular FATAL categories, and the Test::Warnings, Test::NoWarnings, Modern::Perl, Moo, Mojo::Base and Test2::V0 notes, none of which these pages state.

Method: docs-only read of cited pages, 2026-11-08
