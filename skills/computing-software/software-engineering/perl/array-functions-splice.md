---
id: computing-software.software-engineering.perl.array-functions-splice
name: array-functions-splice
category: computing-software
field: software-engineering
product: perl
tags: [perl, push, pop, shift, unshift, splice, perlfunc, array-functions-splice, perl-arrays]
level: intro
status: docs-checked
description: "Modify arrays in place with push, pop, shift, unshift and splice, including negative offsets and the $#array idiom."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perldata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# push, pop, shift, unshift, splice and reverse

**Goal:** manipulate arrays with the right built-in.

```perl
my @a = (1..5);
push @a, 6, 7;            # append; returns new length
my $x = pop @a;           # remove last (7)
unshift @a, 0;            # prepend
my $y = shift @a;         # remove first (0)
splice(@a, 1, 2);         # remove 2 elements at index 1 -> returns removed
splice(@a, 1, 0, 'x', 'y');   # insert without removing
splice(@a, -2);           # remove the last two
my @removed = splice(@a, 2, 1, 'z');  # replace one element
$#a = 1;                  # truncate to 2 elements
$#a = -1;  @a = ();       # empty
my $n = @a;  my $max = $#a;   # count and last index
```

## Details
- Negative index counts from the end: `$a[-1]`; `$a[$#a]` is the same.
- Reading `$a[10]` past the end returns undef without extending; assigning extends and fills gaps with undef.
- `splice(@a)` with no further args empties it; `splice(@a, $off)` removes to the end.
- `reverse @a` returns a new list; `@a = reverse @a` reverses in place. In scalar context `reverse` joins and reverses a string.
- `delete $a[i]` is discouraged; use `splice`. `exists $a[i]` tests for an initialised slot.
- `wantarray`-free pattern for queues: `push` + `shift`; stacks: `push` + `pop`.

## Failure modes
- `my @copy = @a;` copies the top level only; nested refs are shared.
- Using `scalar(@a) - 1` vs `$#a` off-by-one in loops.
- Modifying an array while iterating with `foreach` over it (adding/removing) gives undefined behaviour.
- `my ($first, @rest) = @list;` consumes all remaining items: an array on the left is greedy.

## Self-check
- [ ] `perl -e 'my @a=(1..5); splice(@a,1,2); print "@a"'` prints `1 4 5`.

## Checked
2026-11-02: confirmed against perlfunc (push, pop, shift, unshift, splice, delete, exists, reverse) and perldata (negative indexes, $#array, array assignment). Removed: Storable::dclone pointer.
Method: documentation only; no commands were run.
