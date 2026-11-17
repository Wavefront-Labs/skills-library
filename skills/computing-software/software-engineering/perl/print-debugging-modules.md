---
id: computing-software.software-engineering.perl.print-debugging-modules
name: print-debugging-modules
category: computing-software
field: software-engineering
product: perl
tags: [perl, devel-peek, warn-debugging, stack-trace, devel-confess, o-deparse, print-debugging-modules]
level: intro
status: docs-checked
description: "Debug Perl without the debugger: stack traces via Carp and Devel::Confess, Devel::Peek Dump, and B::Deparse (-MO=Deparse,-p) to see how code was parsed."
sources: ["https://perldoc.perl.org/Carp", "https://perldoc.perl.org/Devel::Peek", "https://perldoc.perl.org/B::Deparse", "https://metacpan.org/pod/Devel::Confess"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack traces, Devel::Peek and B::Deparse

**Goal:** the quickest effective probes.

## Stack traces
```perl
use Carp qw(cluck confess longmess shortmess);
cluck "got here";                      # warn with backtrace
my $m = longmess("message from cluck/confess");   # same text, returned
```
```bash
perl -MCarp=verbose script.pl          # croak behaves like confess, carp like cluck, across all modules
perl -d:Confess script.pl              # Devel::Confess: stack trace on every warn and die
perl -MDevel::Confess script.pl        # same, as a module
perl -d:Confess=color script.pl        # warnings yellow, errors red
DEVEL_CONFESS_OPTIONS='color dump' perl -d:Confess script.pl
```
- Devel::Confess builds traces with Carp, via `$SIG{__WARN__}` and `$SIG{__DIE__}` hooks, so it may clash with other modules using those hooks. It also adds traces to thrown exception objects (unlike Carp::Always) by reblessing them into a generated class, so `ref($exception)` can differ. `no Devel::Confess;` disables it inside a script.
- Options: `dump` (show reference contents in arguments, to depth 3 by default; `dump0`... set depth), `source` / `source0..` (source snippets per frame), `evalsource` (string-eval source), `color`, `objects`, `builtin`, `warnings`, `errors`; prefix `no_` to disable. Classes in `%Devel::Confess::NoTrace` get no trace attached (Throwable::Error and Moose::Error::Default by default).
- Trace argument formatting in Carp: `$Carp::MaxArgLen` (64), `$Carp::MaxArgNums` (8), objects can define `CARP_TRACE`.

## Devel::Peek
```bash
perl -MDevel::Peek -e '$a = "x"; Dump($a)'   # raw internals to STDERR
```
- `Dump($x [, $limit])` dumps a scalar; `Dump(@a)` / `Dump(%h)` dump the aggregate; the optional second argument limits recursion and array elements (default 4). `DumpArray($limit, $a, $b, ...)` dumps several values. All output goes to STDERR. `$Devel::Peek::pv_limit` limits printed string length (0 = no limit). `SvREFCNT()` queries reference counts.
- The module is documented as a tool for XS programmers and assumes you know perlguts. Only the first part of its page was read.

## B::Deparse
```bash
perl -MO=Deparse script.pl             # perl source regenerated from the compiled form
perl -MO=Deparse,-p -e 'print ($x ? $a : $b), "\n"'   # extra parentheses show how perl parsed it
perl -MO=Deparse,-P -e 'sub foo (\@) { 1 } foo @x'    # ignore prototypes
```
- Options follow `-MO=Deparse` after commas with no whitespace: `-p` (extra parentheses), `-q` (expand interpolated strings into concatenation/join), `-P`, `-l` (add `#line`), `-d` (Data::Dumper for constants), `-f FILE` (include subs from other files), `-sC`, `-si4`, `-sT` (style).
- Output is not identical to the source (no comments or whitespace, no one-to-one mapping), and a `???` in the output means a constant was optimised away. The page lists known failures. Only the first part of the page (through the style options) was read.

## Self-check
- [ ] A forced `die` inside nested subs shows a full stack trace with `-d:Confess`.

## Checked
Method: 2026-11-08 read Carp and Devel::Confess in full and the first parts of Devel::Peek (to the memory-footprint section) and B::Deparse (through the -s options) via the MetaCPAN API. Removed v1 claims the pages do not make: Data::Dumper tips, `$SIG{__DIE__} = \&Carp::confess`, `perl -c/-V/-v`, Module::CoreList, UTF8-flag advice, `use diagnostics`, Log::Any and `git bisect` advice.
