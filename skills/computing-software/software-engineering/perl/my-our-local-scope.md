---
id: computing-software.software-engineering.perl.my-our-local-scope
name: my-our-local-scope
category: computing-software
field: software-engineering
product: perl
tags: [perl, my, our, local, dynamic-scope, lexical-scope, perlsub, my-our-local-scope, perl-scoping]
level: practitioner
status: docs-checked
description: "Choose between my (lexical), our (package alias) and local (dynamic) and use local to save special variables safely."
sources: ["https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/perlvar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# my, our and local

**Goal:** the three declarations and what each does.

```perl
my $x = 1;            # lexical: visible in the enclosing block/file only
our $VERSION = '1.0'; # lexically-scoped alias to $Pkg::VERSION
$main::g = 5;  $::g;  # fully qualified package variable
sub slurp { local $/; <$fh> }        # dynamic: $/ is undef for this call tree
local $_ = $text;                    # protect $_
local $SIG{ALRM} = sub { die "timeout\n" };
local @ARGV = ($file);  local %ENV = (%ENV, LC_ALL => 'C');
local $h{key} = 1;                   # temporarily override one element
```

## Rules
- Prefer `my` everywhere. `use strict` forces declaration (`strict vars`).
- `local` does not create a new variable; it saves the old value and restores it when the enclosing block exits (even on `die`). It works only on package vars, special vars, and hash/array elements, never on `my` variables.
- `our $x` in two packages in one file creates two different variables: `our` follows the current `package`.
- `my $x = $x;` initialises the new lexical from the outer `$x`, because the new name only appears from the next statement.
- `my ($a, $b)` in sorting code hides the sort variables `$a`/`$b`; do not declare them with `my`.
- `local $_` is safest when a function reads `while (<FH>)`, which clobbers `$_`; or use `for my $line`.
- Under `strict vars`, package variables are declared with `our` or `use vars` (perlsub).

## Failure modes
- Forgetting `local` when changing `$/`, `$,`, `$\`, `$"` or `$@` leaks into callers.
- `local $x` inside a loop restores per iteration of the enclosing block only.
- `local` on a lexical: "Can't localize lexical variable" compile error.

## Self-check
- [ ] `perl -e '$x=1;sub f{print $x} sub g{local $x=2;f()} g();f()'` prints `21`.

## Checked

2026-11-02. Confirmed in perlsub: `my`, `our`, `local` semantics, `my $x = $x`, `Can't localize lexical variable` (perldiag), and that package variables must be declared with `our` or `use vars`. Removed: the claim that `use vars` is obsolete and the `$|` autoflush bullet, which the pages read do not state.

Method: documentation only; no commands were run.
