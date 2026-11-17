---
id: computing-software.software-engineering.perl.defined-or-short-circuit
name: defined-or-short-circuit
category: computing-software
field: software-engineering
product: perl
tags: [perl, defined-or, short-circuit, logical-assign, perlop, defined-or-short-circuit]
level: practitioner
status: docs-checked
description: "Use //, ||, &&, //=, ||= and &&= for defaults and guards, and know the 5.10 and 5.40 differences."
sources: ["https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defined-or, short-circuit and assignment operators

**Goal:** idiomatic defaults and guards.

```perl
my $name = $args{name} // 'anon';     # undef only (5.10+)
my $port = $args{port} || 8080;       # also replaces 0 and ""
$cache{$k} //= compute($k);           # memoise, assigns only when undef
$opt ||= 'x';   $total &&= $total + 1;
my $v = $h && $h->{x} && $h->{x}{y};  # guard chain (returns last true or first false)
do_a() && do_b();                     # statement-level guard
die "usage" unless @ARGV;
```

## Semantics
- `||`, `&&`, `//` return the deciding operand, not 1 or "": `0 || "x"` is "x"; `"" && 5` is "".
- They short-circuit: the right side is not evaluated when unnecessary; do not put side effects there unless intended.
- `//` was added in 5.10.
- Right side of `//=` is evaluated lazily, so expensive defaults are safe.
- `!!$x` normalises to true (1) or false (""); `builtin::true`/`false` exist from 5.36 (`use builtin qw(true false)`; see builtin for current stability).
- Spaceship and string compare return -1/0/1: `$a <=> $b || $a cmp $b` chains sort keys because 0 is false.
- `xor` and the `^^` logical xor (added in 5.40) are rare; prefer explicit conditions.

## Failure modes
- `my $n = shift || 10;` breaks when the caller passes 0; use `shift // 10`.
- Chaining `//` with `||` mixes precedence: both have the same level, left-associative.

## Self-check
- [ ] `perl -e 'my $z=0; print $z//5, $z||5'` prints `05`.

## Checked

2026-11-02. Confirmed: `//` added in 5.10 with the precedence of `||` (perl5100delta, perlop precedence table), `^^` added in 5.40 (perl5400delta, perlop), `<=>`/`cmp` return -1, 0 or 1 (perlop), `builtin::true`/`false` added in 5.36 (perl5360delta, builtin). Removed: the `say`/`state` aside, the list-assignment `die` claim and the 5.40 stability claim for `true`/`false`.

Method: documentation only; no commands were run.
