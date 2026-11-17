---
id: computing-software.software-engineering.perl.data-dumper-inspection
name: data-dumper-inspection
category: computing-software
field: software-engineering
product: perl
tags: [perl, data-dumper, sortkeys, dumper-config, debug-print, data-dumper-inspection, perl-data-utils]
level: intro
status: docs-checked
description: "Print nested Perl data with Data::Dumper configured via Indent, Sortkeys, Terse, Useqq, Deepcopy and Maxdepth, with the documented limits on code refs and eval."
sources: ["https://perldoc.perl.org/Data::Dumper"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data::Dumper and structure inspection

**Goal:** inspect structures quickly and reproducibly.

```perl
use Data::Dumper;
local $Data::Dumper::Sortkeys = 1;   # hash keys in sorted order (default 0)
local $Data::Dumper::Indent   = 1;   # 0 = no newlines, 1 = fixed indent, 2 = default, 3 = adds array index comments
local $Data::Dumper::Terse    = 1;   # avoid $VARn names where possible
local $Data::Dumper::Useqq    = 1;   # double-quoted strings, unprintable characters escaped
local $Data::Dumper::Deepcopy = 1;   # cross-reference only when essential (breaking cycles)
local $Data::Dumper::Maxdepth = 3;   # do not descend deeper than 3 (default 0 = no limit)
print Dumper($data);                 # Dumper(\%h, \@a) numbers the values $VAR1, $VAR2
warn Data::Dumper->Dump([$obj], ['obj']);   # named
```

## Rules and gotchas
- The configuration variables are meant to be localised in a block so other code is not affected. They set the default state of objects created by `new`; after that use the equivalent methods (`$d->Indent(1)`), which return the object so calls chain.
- Output is Perl code, and the return value can be `eval`ed to get an identical copy. The docs warn about the security implications of eval-ing code from untrusted sources.
- Self-referential structures are handled. Default output uses `$VARn` references that are undefined when evaled; set `Purity` to 1 for extra statements that fill in the references (default 0). Under `use strict`, variables the output uses must be declared first.
- `Maxdepth` has no effect when `Purity` is set.
- Code refs: unless `Deparse` is set, a placeholder anonymous sub containing the string `"DUMMY"` is inserted (with a warning if `Purity` is set). Even `Deparse` can give results that behave differently after eval.
- Perl hash key order differs between runs, so Dumper output with hashes differs between runs unless you set `Sortkeys` (or `PERL_HASH_SEED`, see perlrun).
- `Sortkeys` can also be a sub ref that returns an array ref of the keys to dump, in order, which also filters keys.
- `Quotekeys` (default 1) controls hash key quoting; `Pair` (default `=>`) sets the key/value separator.
- You cannot pass an array or hash directly to `Dumper`; pass a reference (`\@a`) or use `Dump` with a name starting with `*`.
- `Maxrecurse` (default 1000) throws an exception beyond that depth; it exists to stop perl running out of stack on very deep structures.

## Self-check
- [ ] With `$Data::Dumper::Indent = 0`, `Dumper([1,{a=>2}])` prints with no newlines or indentation.

## Checked

Date: 2026-11-08. Confirmed against the Data::Dumper page on perldoc.perl.org: Indent styles 0-3 and default 2, Sortkeys (boolean or sub), Terse, Useqq, Deepcopy, Maxdepth, Maxrecurse, Purity, Quotekeys, Pair, Deparse and the "DUMMY" placeholder, eval and security warning, the localise-and-methods guidance, and the hash-order note. Removed: claims about quoting of numbers stored as strings, overloaded stringification on objects, and the Data::Printer, Storable, Sereal and JSON::PP alternatives and the exact self-check output, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
