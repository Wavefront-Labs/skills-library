---
id: computing-software.software-engineering.perl.statement-modifiers-unless
name: statement-modifiers-unless
category: computing-software
field: software-engineering
product: perl
tags: [perl, statement-modifier, unless, postfix-if, ternary, perlsyn, statement-modifiers-unless]
level: intro
status: docs-checked
description: "Choose between postfix modifiers, if/elsif/else, unless and the ternary operator for readable conditionals."
sources: ["https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/perlstyle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statement modifiers, unless and conditional forms

**Goal:** readable conditionals without traps.

```perl
print "ok\n" if $ok;
warn "bad\n" unless $ok;
$total += $_ for @nums;            # postfix for
push @q, shift @src while @src;    # postfix while
if    ($n < 0) { ... }
elsif ($n == 0){ ... }
else           { ... }              # braces are mandatory: no dangling else
my $kind = $n < 0 ? 'neg' : $n == 0 ? 'zero' : 'pos';
```

## Style
- Postfix modifiers suit short guards and early exits: `return unless defined $x;`.
- Modifiers take a single simple statement, not a block; `do { ... } if $x;` runs the block once when true.
- A `my` declaration with a postfix condition (`my $x = 1 if $c;`) has undefined behaviour; declare first.
- The condition of `if` must be parenthesised and the keyword is `elsif`.

## Smartmatch and given/when
`given`/`when` and `~~` were declared a failed experiment and deprecated in 5.38. Removal planned for 5.42 was indefinitely postponed, but they need the `switch` and `smartmatch` features (not in the 5.36 or later bundles). Prefer `if`/`elsif` or hash dispatch tables.

## Dispatch table alternative
```perl
my %act = (start => \&start, stop => \&stop);
($act{$cmd} // die "unknown command $cmd\n")->(@args);
```

## Self-check
- [ ] `perl -we 'print "a" if 1; print "b" unless 1; print "\n"'` prints `a`.

## Checked

2026-11-02. Confirmed in perlsyn: statement modifiers take an expression not a block, `unless ... elsif ... else` is valid, `my $x if ...` is undefined; in perl5380delta and perl5420delta: switch and smartmatch were deprecated in 5.38 but their removal has been postponed indefinitely and they need their features. FIXED: the skill said they are slated for removal. Removed the style bullets attributed to perlstyle (not found there).

Method: documentation only; no commands were run.
