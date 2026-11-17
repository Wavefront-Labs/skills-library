---
id: computing-software.software-engineering.perl.hash-ordering-locking
name: hash-ordering-locking
category: computing-software
field: software-engineering
product: perl
tags: [perl, hash-randomisation, hash-util, lock-keys, tie-ixhash, perl-hash-seed, hash-ordering-locking]
level: advanced
status: docs-checked
description: "Deal with randomised hash order, produce stable output with sort keys, and restrict keys with Hash::Util lock_keys."
sources: ["https://perldoc.perl.org/perlsec", "https://perldoc.perl.org/perlrun", "https://perldoc.perl.org/Hash::Util"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash ordering, randomisation and Hash::Util

**Goal:** deterministic output and typo-proof hashes.

## Order is not stable
Hash order is deliberately randomised as protection against algorithmic-complexity attacks (perlsec, Hash Seed Randomization). Never depend on it, never assert it in tests.
```perl
for my $k (sort keys %h) { ... }                  # stable output
for my $k (sort { $h{$b} <=> $h{$a} or $a cmp $b } keys %h) { ... }   # by value, tie-broken
```

## Debugging with fixed order
`PERL_HASH_SEED=0 PERL_PERTURB_KEYS=0 perl script.pl` makes order reproducible for debugging; do not set these in production (perlrun documents both).

## Restricting keys
```perl
use Hash::Util qw(lock_keys unlock_keys lock_hash lock_value);
my %cfg = (host => 'x', port => 80);
lock_keys(%cfg);         # adding unknown keys now dies
$cfg{prot} = 1;          # dies: 'prot' is not in the restricted key set
lock_hash(%cfg);         # also makes values read-only
```
`lock_keys(%h, @allowed)` restricts the key set to `@allowed`; `lock_keys_plus` allows extra keys on top of the current ones (Hash::Util).

## Failure modes
- Tests that compare `keys %h` order fail intermittently.
- `lock_hash` applies to one hash: use `lock_hash_recurse` (Hash::Util) or lock nested hashes separately.

## Self-check
- [ ] Run the test suite 3 times; no order-dependent failure.
- [ ] `perl -MHash::Util=lock_keys -e '%h=(a=>1);lock_keys(%h);$h{b}=1'` dies.

## Checked
2026-11-03: confirmed against perlsec (hash seed randomisation, algorithmic complexity), perlrun (PERL_HASH_SEED and PERL_PERTURB_KEYS) and Hash::Util (lock_keys with and without a key list, lock_keys_plus, lock_value, lock_hash, lock_hash_recurse). Removed: the exact error message, the per-process 5.18 date, JSON::PP canonical, Data::Dumper Sortkeys, Hash::Ordered, Tie::IxHash, Readonly and the claim about lock_keys failing on extra keys.
Method: documentation only; no commands were run.
