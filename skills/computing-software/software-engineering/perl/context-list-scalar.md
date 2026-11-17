---
id: computing-software.software-engineering.perl.context-list-scalar
name: context-list-scalar
category: computing-software
field: software-engineering
product: perl
tags: [perl, context, wantarray, perldata, context-list-scalar, perl-scalars]
level: practitioner
status: docs-checked
description: "Predict what an expression returns in list versus scalar context, and write subs that use wantarray correctly."
sources: ["https://perldoc.perl.org/perldata", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List versus scalar context and wantarray

**Goal:** know which context every expression runs in; most surprising Perl behaviour is context.

## Rules of thumb
```perl
my @a = (10, 20, 30);
my $n = @a;            # scalar context: 3 (element count)
my ($first) = @a;      # list assignment: 10
my $last = $a[-1];     # 30
print "n=" . @a . "\n";          # '.' gives scalar context: n=3
print "a: @a\n";                  # interpolation joins with $"
```
- `scalar(@a)` forces scalar context; `scalar(reverse "abc")` is "cba" but `print reverse "abc"` prints "abc" (list context).
- A function chooses its own result per context: `localtime` returns a list in list context, a string in scalar context.
- The comma operator in scalar context returns the last value: `my $x = (4, 5, 6);` gives 6 (arrays are not "lists").

## wantarray
```perl
sub parts {
    my @r = split /,/, shift;
    return wantarray ? @r : scalar @r;   # list, scalar; undef in void context
}
my @p = parts("a,b,c");   # a b c
my $c = parts("a,b,c");   # 3
```
`wantarray` is true in list context, false (defined) in scalar, `undef` in void.

## Failure modes
- `return (1,2,3)` in scalar context yields 3 (last element), but `return @a` yields the count; do not mix them.
- `my $x = func_returning_list();` is not the same as `my ($x) = func_returning_list();`.
- `if (my @found = grep {...} @l)` tests the element count; `if ((my $r = f()) )` tests the value.
- Do not make a sub return different shapes per context unless documented; callers pass it to `print`/hash constructors unexpectedly.
- `return;` gives empty list in list context, `undef` in scalar: safer than `return undef` (which gives a one-element list that is true in `if (my @r = f())`).

## Self-check
- [ ] `perl -e 'my @a=(1,2,3); my $c=@a; my ($f)=@a; print "$c $f\n"'` prints `3 1`.
- [ ] Every sub that can return lists documents (or avoids) context-sensitive returns.

## Checked
2026-11-02: confirmed against perlfunc (wantarray, reverse, localtime context behaviour) and perlsub (return with no value: empty list or undef). Removed: the countof idiom line.
Method: documentation only; no commands were run.
