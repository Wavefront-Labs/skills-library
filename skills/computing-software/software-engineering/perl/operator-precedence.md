---
id: computing-software.software-engineering.perl.operator-precedence
name: operator-precedence
category: computing-software
field: software-engineering
product: perl
tags: [perl, precedence, and-or-not, perlop, open-or-die, operator-precedence, perl-operators]
level: practitioner
status: docs-checked
description: "Read perlop's precedence table correctly: why open() || die differs from open() or die, and when to use and/or/not."
sources: ["https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator precedence and low-precedence logic

**Goal:** avoid precedence bugs, especially around list operators and `||`.

## The table, high to low (perlop)
terms and `->`; `++ --`; `**`; `! ~ \ unary+ unary-`; `=~ !~`; `* / % x`; `+ - .`; `<< >>`; named unary ops (`-e`, `defined`, `ref`, `lc`); `isa`; chained relational `< > <= >= lt gt le ge`; equality `== != eq ne <=> cmp` (chained for `==`/`!=`/`eq`/`ne`); `&`; `| ^`; `&&`; `|| ^^ //`; `.. ...`; `?:`; assignment; `, =>`; list operators (rightward); `not`; `and`; `or xor`.

## Classic bugs
```perl
open my $fh, '<', $f || die "no";    # BUG: binds to $f; die never runs
open(my $fh, '<', $f) || die "...";  # OK with parens
open my $fh, '<', $f or die "...";   # OK: 'or' is lower than list operators
print (1+2)*3;                       # prints 3; parens are the call
my $x = $a || $b ? 1 : 2;            # ($a || $b) ? 1 : 2
my @l = (1,2,3) x 2;                 # list repeat: 1 2 3 1 2 3
my $s = "-" x 20;                    # string repeat
return $x or die;                    # BUG: 'or' never reached; use ||
```
- Use `and`/`or`/`not` for control flow (`do_it() or return;`), `&&`/`||`/`!` inside expressions.
- Assignment `my $v = f() or die` assigns first, then tests: fine for failure checking; but `my @r = f() or ...` tests the count.
- `!` binds tighter than comparison: `!$a == $b` is `(!$a) == $b`; use `$a != $b`.
- Ternary chains right-associate: `$n == 1 ? 'a' : $n == 2 ? 'b' : 'c'` works; nested assignment inside needs parens.
- Chained comparison: `1 < $x < 10` works from Perl 5.32 (perl5320delta); older releases need `&&`.
- `**` is right-associative and binds tighter than unary minus: `-2**2` is -4.

## Self-check
- [ ] `perl -MO=Deparse,-p -e 'open F,"<",$f || die'` shows the grouping.
- [ ] No `||` after an open/close/mkdir without parentheses.

## Checked

2026-11-02. Compared the table with the perlop precedence table (current text); confirmed `**` binds tighter than unary minus (`-2**4`), chained comparisons from 5.32 (perl5320delta), `isa` position. Added `^^` to the `||` level and `~.` is a bitwise string operator.

Method: documentation only; no commands were run.
