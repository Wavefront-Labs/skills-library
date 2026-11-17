---
id: computing-software.software-engineering.perl.sub-signatures
name: sub-signatures
category: computing-software
field: software-engineering
product: perl
tags: [perl, signatures, feature-signatures, use-v5-36, perlsub, sub-signatures]
level: practitioner
status: docs-checked
description: "Declare parameters with use feature 'signatures' (default in use v5.36), including defaults, slurpy args and arity checks."
sources: ["https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/feature"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subroutine signatures

**Goal:** replace `my (...) = @_;` with declared, arity-checked parameters.

```perl
use v5.36;                       # enables signatures, strict, warnings, say
sub greet ($name, $greeting = "Hello") { say "$greeting, $name" }
sub total ($first, @rest)        { ... }             # slurpy array
sub opts  ($x, %o)               { ... }             # slurpy hash
sub ignore($, $second)           { ... }             # placeholder for an unused arg
sub cb    ($x, $y //= 0)         { ... }             # default when undef (5.38+)
my $anon = sub ($n) { $n * 2 };
```
Method signatures count the invocant: in a package use `sub name ($self, $x) {...}`.

## Behaviour
- Too few or too many arguments dies at runtime ("Too few arguments for subroutine 'main::greet'"); this is the main behavioural change from `@_`.
- Default expressions are evaluated at call time and may refer to earlier parameters: `($x, $y = $x * 2)`.
- Signatures were introduced in Perl 5.20 and are stable from 5.36, where they join the `:5.36` feature bundle.
- `//=` and `||=` defaults arrived in 5.38.
- Prototypes with signatures: use the `:prototype($$)` attribute before the signature, not the old `($$)` position.

## Gotchas
- Code that mutates `$_[0]` (aliasing) no longer fits signatures; reading `@_` inside a signatured sub is discouraged and warns in the `experimental::args_array_with_signatures` category.
- Under `use feature 'signatures'`, `sub f($$)` is a signature with two unnamed args, not a prototype.

## Self-check
- [ ] `perl -E 'use v5.36; sub f($x,$y=2){$x+$y} say f(1); f()'` prints `3` then dies on the call with no args.

## Checked

2026-11-02. Confirmed in perlsub: `:prototype(...)` before the signature, `@_` use with signatures warns in `experimental::args_array_with_signatures`; perl5360delta: signatures part of the 5.36 bundle and stable; perl5380delta: `//=` and `||=` defaults. Removed: the 'on 5.20 to 5.34' pragma line and the third-party module bullet.

Method: documentation only; no commands were run.
