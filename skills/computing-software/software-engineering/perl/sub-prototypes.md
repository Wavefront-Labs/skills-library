---
id: computing-software.software-engineering.perl.sub-prototypes
name: sub-prototypes
category: computing-software
field: software-engineering
product: perl
tags: [perl, prototype, perlsub, block-argument, attribute-prototype, sub-prototypes]
level: advanced
status: docs-checked
description: "Use prototypes only for block-taking and context-imposing helpers (&@, @); know why they are not argument validation."
sources: ["https://perldoc.perl.org/perlsub"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototypes and block-taking subs

**Goal:** know the narrow legitimate uses of prototypes.

```perl
sub apply(&@) { my ($code, @l) = @_; map { $code->($_) } @l }
my @r = apply { $_[0] * 2 } 1, 2, 3;       # block syntax like grep/map
sub mypush(\@@) { my $a = shift; push @$a, @_ }   # takes @array by reference implicitly
mypush @list, 1, 2;
sub max2($$) { $_[0] > $_[1] ? $_[0] : $_[1] }
sub opt(;$)  { ... }                        # optional arg
sub noargs() { 42 }                         # constant-like; can be inlined
```
With signatures: `sub apply :prototype(&@) ($code, @l) {...}`.

## Rules
- A prototype affects parsing at compile time. The sub must be declared before the call is compiled.
- Prototypes are ignored for method calls (`$obj->m(...)`) and for calls using the `&` sigil (`&name(...)`) (perlsub).
- A `$` in a prototype forces scalar context, so `f(@a)` passes the array length.
- Use `prototype('CORE::push')` to inspect built-ins; `prototype(\&f)` for yours.
- perlsub says prototypes exist mainly so you can define subroutines that work like built-in functions.

## Failure modes
- Adding a prototype to an existing sub silently changes how callers' arguments are parsed.
- Exporting a prototyped sub to a package compiled earlier loses the prototype effect.

## Self-check
- [ ] The prototype exists solely for block or reference syntax, and `perl -c` passes for callers.

## Checked
2026-11-03: confirmed against perlsub (prototype syntax and the :prototype attribute, \@ and & and $ and ; characters, compile-time visibility, method calls and & calls bypass prototypes, signatures versus prototypes) and perlfunc (prototype). Removed: the f 1, 2 parsing claim, the references claim, Try::Tiny and List::Util mentions and the Perl::Critic policy.
Method: documentation only; no commands were run.
