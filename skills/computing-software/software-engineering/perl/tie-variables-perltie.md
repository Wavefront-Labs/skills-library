---
id: computing-software.software-engineering.perl.tie-variables-perltie
name: tie-variables-perltie
category: computing-software
field: software-engineering
product: perl
tags: [perl, tie, tied-hash, tie-scalar, tie-std-hash, perltie, tie-variables-perltie, perl-advanced-language]
level: sme
status: docs-checked
description: "Implement tied scalars, arrays, hashes and handles in Perl (TIEHASH, FETCH, STORE, UNTIE) per perltie, inherit from Tie::StdHash, and avoid the untie gotcha."
sources: ["https://perldoc.perl.org/perltie", "https://perldoc.perl.org/Tie::Hash"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tied variables

**Goal:** make a variable's operations call methods.

```perl
package UpperHash;
require Tie::Hash; our @ISA = 'Tie::StdHash';          # base class provides a working hash
sub STORE { my ($self, $k, $v) = @_; $self->{uc $k} = $v }
sub FETCH { my ($self, $k) = @_; $self->{uc $k} }
sub EXISTS { exists $_[0]->{uc $_[1]} }
package main;
tie my %h, 'UpperHash';
$h{abc} = 1; print join(',', keys %h);     # ABC
my $obj = tied %h;                           # the underlying object
untie %h;
```

Methods per type, per perltie:
- Scalar: `TIESCALAR`, `FETCH`, `STORE`, and possibly `UNTIE` and/or `DESTROY`.
- Array: `TIEARRAY`, `FETCH`, `STORE`, `FETCHSIZE`, `STORESIZE`, `CLEAR`, and perhaps `UNTIE`/`DESTROY`. `POP`, `PUSH`, `SHIFT`, `UNSHIFT`, `SPLICE`, `DELETE` and `EXISTS` are required only if the matching operator is used on the tied array (`Tie::Array` can implement the first five; its `DELETE` and `EXISTS` croak). `EXTEND` is called when perl would pre-extend a real array; a no-op is acceptable and it must not just be `STORESIZE`.
- Hash: `TIEHASH` (constructor), `FETCH`, `STORE`, `EXISTS`, `DELETE`, `CLEAR`, `FIRSTKEY` and `NEXTKEY` (for `keys` and `each`), `SCALAR`, `UNTIE`, `DESTROY`.
- Handle: `TIEHANDLE`, at least one of `PRINT`, `PRINTF`, `WRITE`, `READLINE`, `GETC`, `READ`, and possibly `CLOSE`, `UNTIE`, `DESTROY`; also `BINMODE`, `OPEN`, `EOF`, `FILENO`, `SEEK`, `TELL` if those operators are used on the handle.

## Base classes
- `Tie::Hash` documents `Tie::StdHash` and `Tie::ExtraHash` as base class definitions for tied hashes. Inherit from `Tie::StdHash` and redefine only the interesting methods. `Tie::ExtraHash` stores the extra `tie()` arguments from offset 1 in the array behind `tied(%h)`.
- `UNTIE` and `DESTROY` are not defined in `Tie::Hash`, `Tie::StdHash` or `Tie::ExtraHash`; `SCALAR` is defined in `Tie::StdHash` and `Tie::ExtraHash` only.
- perltie names `Tie::Scalar`, `Tie::Array`, `Tie::Hash` and `Tie::Handle` as good starting points for tie implementations, and `DB_File` and `Config` as interesting examples.

## Rules
- Keep one tie type per class; the method names (`FETCH`, `STORE`) are shared across types but the constructors differ.
- `tied VARIABLE` returns the object that `tie` returned. `untie` destroys the variable's reference to it; if you hold another reference, the object is not destroyed then, and with `use warnings 'untie'` or `-w` perl prints `untie attempted while 1 inner references still exist` (the count varies). Drop your own references before `untie`.
- If an `UNTIE` method exists, that warning does not occur; `UNTIE` receives the count of extra references and can warn itself. The docs suggest moving cleanup that would go in `DESTROY` to `UNTIE` in most cases.
- Localising tied arrays or hashes does not work: after leaving the scope they are not restored.
- Negative array indices are translated using `FETCHSIZE` before `FETCH`; set `$NEGATIVE_INDICES` true in the tied array class to disable that.
- Perl may mistakenly return true for a tied hash in scalar context after you empty it by repeated `DELETE`; supply your own `SCALAR` when that matters.

## Self-check
- [ ] `tied %h` returns an `UpperHash` object and `exists $h{ABC}` is true after `$h{abc}=1`.

## Checked

Date: 2026-11-08. Confirmed against perltie and Tie::Hash on perldoc.perl.org: the method sets per tie type, Tie::Array/EXTEND notes, Tie::StdHash and Tie::ExtraHash behaviour, the untie gotcha and its warning text, UNTIE semantics, no localising of tied arrays and hashes, negative index handling and the SCALAR advice. Removed: Tie::File, Tie::IxHash, Tie::RefHash and the DBM-file ties, Tie::StdScalar, Tie::StdArray and Tie::StdHandle, speed claims, and the tied-handle output-capture advice, which these two pages do not state.

Method: docs-only read of cited pages, 2026-11-08
