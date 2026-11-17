---
id: computing-software.software-engineering.perl.scalar-util-blessed-dualvar
name: scalar-util-blessed-dualvar
category: computing-software
field: software-engineering
product: perl
tags: [perl, scalar-util, looks-like-number, dualvar, readonly-check, refaddr, scalar-util-blessed-dualvar]
level: practitioner
status: docs-checked
description: "Use Scalar::Util: blessed, reftype, refaddr, looks_like_number, weaken, dualvar, readonly, openhandle and tainted."
sources: ["https://perldoc.perl.org/Scalar::Util"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scalar::Util helpers

**Goal:** safe type and state checks for scalars.

```perl
use Scalar::Util qw(blessed reftype refaddr looks_like_number weaken isweak dualvar readonly openhandle tainted isvstring);
blessed($x);                 # class name or undef (works on non-references)
reftype($x);                 # underlying 'HASH', 'ARRAY' even for objects
refaddr($x);                 # numeric address; use as an id key (stable while the object lives)
looks_like_number($s);       # true if perl thinks the value is a number (perlapi looks_like_number)
weaken($self->{parent});
my $d = dualvar(5, "five"); print $d + 1, " $d";       # 6 five
readonly($v);                # true if the scalar is readonly
my $fh = openhandle(\*STDIN); # returns the handle if open, else undef
```

## Rules
- Use `blessed($x) && $x->isa('Class')` rather than `ref($x) eq 'Class'`.
- `reftype` ignores blessing; `ref` returns the class for objects.
- `weaken` makes a copy strong again if assigned: `my $copy = $weak;` is a strong reference.
- The documentation calls `dualvar` not as useful as it may seem.
- `Scalar::Util::tainted` supports taint testing.
- For booleans use `builtin::is_bool` (5.36+, check status in your Perl).

## Self-check
- [ ] `perl -MScalar::Util=blessed -e 'print defined blessed("x") ? 1 : 0'` prints `0` without dying.

## Checked
2026-11-03: confirmed against the Scalar::Util documentation (blessed, reftype, refaddr, looks_like_number, weaken and strong copies, dualvar and its caution, readonly, openhandle, tainted, isvstring) and the builtin documentation (is_bool). Removed: the list of strings said to be numeric, the whitespace claim, Ref::Util, and the inside-out object remark.
Method: documentation only; no commands were run.
