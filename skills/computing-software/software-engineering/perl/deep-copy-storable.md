---
id: computing-software.software-engineering.perl.deep-copy-storable
name: deep-copy-storable
category: computing-software
field: software-engineering
product: perl
tags: [perl, dclone, storable, deep-copy, freeze-thaw, serialisation, deep-copy-storable]
level: practitioner
status: docs-checked
description: "Deep-copy nested Perl data with Storable::dclone and serialise with store, nstore and freeze, knowing the documented code-ref, hook and untrusted-data limits."
sources: ["https://perldoc.perl.org/Storable"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep copy, freezing and Storable

**Goal:** copy or persist nested data safely.

```perl
use Storable qw(dclone store retrieve nstore freeze thaw nfreeze);
my $copy = dclone($data);              # deep copy: thaw(freeze(.)) without the intermediate scalar
store(\%h, $file);   my $h = retrieve($file);
nstore(\%h, $file);                    # network order, for sharing across platforms
my $bytes = nfreeze($ref);  my $back = thaw($bytes);
```

## Rules
- Storable stores recursively, so objects that share data keep sharing it after retrieval. `dclone` is documented as equal to `thaw(freeze(.))` but without creating the intermediate scalar.
- `store` returns undef on I/O problems and a true value otherwise; `retrieve` returns undef on read errors; serious errors die, so trap them with `eval {}`. There is no `nretrieve`: `retrieve` reads native or network order data alike.
- CODE refs can be serialised only with `$Storable::Deparse` true, and deserialised only with `$Storable::Eval` true (done through `eval`, dangerous with malicious data; `$Storable::Eval` can be a sub ref such as a `Safe` compartment `reval`).
- GLOB and FORMLINE refs cannot be stored: store croaks unless `$Storable::forgive_me` is true, in which case it warns and stores a meaningless string.
- `nstore`/`nfreeze` write network order for sharing across platforms; native-order files record sizes and byte order and refuse to load on an incompatible perl. Doubles are stored stringified in network order, with possible loss in the last decimals.
- `$Storable::canonical` true stores hashes sorted by key so frozen strings can be compared; it can be slower on large hashes and may still not compare equal when numbers were used as strings.
- Security: the docs say do not accept Storable data from untrusted sources. There is no way to configure it safely; retrieving can load the module for any object class named in the data, run object destructors, and with CODE refs execute code. If you must accept untrusted data, the docs suggest Cpanel::JSON::XS or Data::MessagePack for simple data, and Sereal for complex Perl structures (configure its encoder and decoder, since it is unsafe by default).
- Hooks `STORABLE_freeze($self, $cloning)` and `STORABLE_thaw` customise how a class serialises; `$cloning` is true under `dclone`, and the docs advise `return if $cloning;` in `STORABLE_freeze` to keep reasonable `dclone` semantics. Return extra references from `STORABLE_freeze` so shared objects stay shared.
- `STORABLE_attach` (with `STORABLE_freeze`) is the documented route for shared resource objects such as singletons, database pools or caches.
- The CPAN `Clone` module deep-clones natively but, per the docs, does not support Storable hooks.
- References used as hash keys do not survive store/retrieve with meaning, because their stringified addresses change. Call `binmode` on descriptors passed to Storable functions where it matters.

## Self-check
- [ ] After `my $c = dclone($d); $c->{a}[0] = 99;` the original `$d->{a}[0]` is unchanged.

## Checked

Date: 2026-11-08. Confirmed against the Storable page on perldoc.perl.org: dclone equals thaw(freeze), store/retrieve return values, nstore network order and header byte-order check, CODE reference Deparse/Eval, forgive_me, canonical, the SECURITY WARNING section and its alternatives, hooks and STORABLE_attach, the Clone note and the hash-key-reference warning. Removed: the shallow-copy idioms, the claim that memory roughly doubles during dclone, the claim that tied hashes copy badly, the statement that cyclic structures and blessing are preserved by name, "version-sensitive for long-term archival" advice and the Data::Dumper plus eval alternative, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
