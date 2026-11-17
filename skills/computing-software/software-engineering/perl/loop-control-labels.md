---
id: computing-software.software-engineering.perl.loop-control-labels
name: loop-control-labels
category: computing-software
field: software-engineering
product: perl
tags: [perl, last, next, redo, loop-labels, continue-block, perlsyn, loop-control-labels, perl-control-flow]
level: practitioner
status: docs-checked
description: "Control loops with last, next, redo and labels; know why do-while is not a loop and how bare blocks behave."
sources: ["https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# last, next, redo, continue blocks and labels

**Goal:** exit and skip correctly, including nested loops.

```perl
OUTER: for my $row (@rows) {
    for my $cell (@$row) {
        next OUTER if $cell eq 'skip-row';
        last OUTER if $cell eq 'stop';
        next unless length $cell;
    }
}
for (my $i = 0; $i < 10; $i++) { ... }
while (my $l = <$fh>) { next if $l =~ /^#/; ... } continue { $count++ }  # continue runs even after next
do { $n++ } until $n >= 5;       # body first, condition after
{ last if $done; ...; }          # a bare block is a loop that runs once
```

## Rules
- `last` leaves the innermost loop (or the named label); `next` jumps to the next iteration (running the `continue` block); `redo` restarts the iteration without re-testing the condition.
- `do { } while ...` is a statement-modifier on a `do` block, not a loop: `last`/`next` do not work inside it (use a real `while` or wrap in a bare block).
- Using `next`/`last` inside a sub called from a loop leaves the sub with warning "Exiting subroutine via next"; avoid.
- A label identifies the loop that `last`/`next`/`redo` apply to (perlsyn).
- `while (<$fh>)` implicitly tests `defined($_ = <$fh>)`; `while (my $l = <$fh>)` also adds an implicit `defined` test, so a line "0" without a newline does not stop the loop.
- Infinite loops: `while (1)`, `for (;;)`.
- Multi-variable foreach `for my ($k, $v) (%h)` was added as experimental in Perl 5.36 and is no longer experimental in 5.40.

## Self-check
- [ ] `perl -e 'A: for $i (1..3){for $j (1..3){next A if $j==2;print "$i$j "}}'` prints `11 21 31`.

## Checked

2026-11-02. Confirmed in perlsyn: loop control statements, `continue` blocks, labels, and that `do {} while` is a statement modifier where `next`/`last` do not work; perldiag for `Exiting subroutine via %s`; perlop for the implicit `defined` test in `while (<$fh>)`. FIXED: multi-variable `foreach` was experimental in 5.36 and is no longer experimental in 5.40 (perl5360delta, perl5400delta). Removed the `grep`/`map`/`sort` and uppercase-label claims.

Method: documentation only; no commands were run.
