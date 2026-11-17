---
id: computing-software.software-engineering.perl.constant-readonly-values
name: constant-readonly-values
category: computing-software
field: software-engineering
product: perl
tags: [perl, use-constant, constants, readonly, inlined-constants, perlsub, constant-readonly-values]
level: practitioner
status: docs-checked
description: "Define constants with use constant (scalars and lists), interpolate them correctly, and use Readonly or Internals::SvREADONLY."
sources: ["https://perldoc.perl.org/constant", "https://perldoc.perl.org/perlsub"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# constant pragma and read-only values

**Goal:** named constants that the compiler can inline.

```perl
use constant PI      => 3.14159;
use constant DEBUG   => $ENV{DEBUG} // 0;
use constant COLORS  => qw(red green blue);          # list constant
use constant {                                       # several at once
    HOST => 'localhost',
    PORT => 8080,
};
my @c = (COLORS);  my $second = (COLORS)[1];
print "pi is @{[ PI ]}\n";                            # constants do not interpolate in strings
my %h = (PI, 1);          # key is the string "3.14159"; but PI => 1 would quote it
$h{+HOST} = 1;            $h{HOST()} = 1;            # use + or () for hash keys
```

## Rules
- Scalar constants are inlinable subroutines, so `PI * 2` parses as expected.
- Hash key `PI => 1` and `$h{PI}` treat PI as a string: use `PI() => 1`, `$h{+PI}`.
- Refs are shallow: `use constant LIST => [1,2];` the array itself is still mutable.

## Failure modes
- Do not use a multi-value constant in scalar context: it currently returns the number of values but this may change; copy it with `my @c = (COLORS)`.

## Self-check
- [ ] `perl -e 'use constant PI=>3; %h=(PI=>1); print keys %h'` prints `PI`.

## Checked
2026-11-02: confirmed against constant pragma page (list constants, scalar-context result, bareword hash-key rule with `+` and `()`, `CONSTANT() =>`, inlinable scalar constants). Removed: constant folding, Readonly, Internals::SvREADONLY, lock_hash, Exporter, builtin::true and redefinition remarks.
Method: documentation only; no commands were run.
