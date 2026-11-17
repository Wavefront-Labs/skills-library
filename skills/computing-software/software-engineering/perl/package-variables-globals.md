---
id: computing-software.software-engineering.perl.package-variables-globals
name: package-variables-globals
category: computing-software
field: software-engineering
product: perl
tags: [perl, package-variables, global-variables, sort-variables, use-vars, perlvar, package-variables-globals]
level: practitioner
status: docs-checked
description: "Understand package (global) variables, fully qualified names, and the special globals $a and $b, and keep them under strict."
sources: ["https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/vars"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package variables, special globals and sort's $a and $b

**Goal:** know when globals exist and how to keep them tame.

```perl
package Config::App;
our $Debug = 0;                       # package variable $Config::App::Debug, declared under strict
our @Handlers;  our %Registry;
$main::Verbose = 1;  $::Verbose = 1;  # fully qualified, no declaration needed
use vars qw($Old);                    # pre-5.6 style declaration; prefer our
```

## Rules
- Under `use strict 'vars'` an undeclared, unqualified global is a compile error: declare with `my` (lexical) or `our` (package).
- `$a` and `$b` are exempt from strict because `sort` and `List::Util::reduce` use them; never declare `my $a`/`my $b`.
- `our $x` introduces a lexical alias to the package variable, visible to the end of the enclosing block even across `package` statements in the same scope: `package A; our $x; package B; print $x` still prints `$A::x`.
- Special globals `$_`, `@_`, `$0`, `$1`.., `%ENV`, `@ARGV`, `STDIN`, `STDOUT`, `STDERR`, `INC` live in package `main` regardless of the current package.
- Read a variable by name with symbolic references only when strict refs is off: `${"Pkg::$name"}`; prefer a hash.
- An `our $x;` after code that already used `$x` does not affect earlier statements.

## Failure modes
- Two modules each declaring `our $VERSION` are independent: they are different packages.
- Leaving a modified global (`$/`, `$|`, `$,`) changes behaviour of unrelated code; use `local`.

## Self-check
- [ ] `perl -Mstrict -e '$x = 1'` fails; `perl -Mstrict -e 'our $x = 1; print $main::x'` prints `1`.

## Checked
2026-11-03: confirmed against perlsub (our, my, local), perlvar and vars (special variables live in main, $a and $b for sort, use vars), perlfunc our (lexical alias to the package variable, redundant repeated declarations) and perlref (symbolic references under strict refs). Removed: the exact compiler error text, the Data::Dumper and Carp variable examples, and Perl::Critic.
Method: documentation only; no commands were run.
