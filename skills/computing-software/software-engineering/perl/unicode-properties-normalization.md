---
id: computing-software.software-engineering.perl.unicode-properties-normalization
name: unicode-properties-normalization
category: computing-software
field: software-engineering
product: perl
tags: [perl, unicode-properties, normalization, grapheme-cluster, unicode-normalize, unicode-properties-normalization]
level: advanced
status: docs-checked
description: "Use p{...} properties, X, the /a modifier and Unicode::Normalize NFC/NFD/NFKC/NFKD for correct Unicode matching and comparison."
sources: ["https://perldoc.perl.org/perlunicode", "https://perldoc.perl.org/perlrecharclass", "https://perldoc.perl.org/Unicode::Normalize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode properties and normalization

**Goal:** treat text as people do.

```perl
/\p{Lu}/;  /\p{Thai}/;  /[\p{Thai}\d]/;  /[^\p{Arabic}()]/;    # properties, alone or in a class
/\d+/a;                                  # ASCII digits only
use Unicode::Normalize;                  # NFC NFD NFKC NFKD exported by default
my $same = NFD($x) eq NFD($y);           # compare after the same normalization form
```

## Properties (perlrecharclass, perlunicode)
- `\p{Prop}` matches a character with the given Unicode property; `\P{Prop}` is the negation. Examples from
  perlrecharclass: `"a" =~ /\p{Lu}/` does not match (Lu is upper case letters); `"\x{0e0b}" =~ /\p{Thai}/` matches.
- Properties can sit inside bracketed classes (`[\p{Thai}\d]`, `[^\p{Arabic}()]`). A range such as `[\p{Thai}-\d]` is
  wrong.
- Perl's full property list is in perluniprops; you can define your own properties (perlunicode, "User-Defined
  Character Properties").
- For natural-language processing, perlunicode says `Script_Extensions` or `Script` are likely the properties you want;
  `Block` is occasionally useful for the nuts and bolts.
- For identifier-like characters beyond ASCII, perlrecharclass points to `\p{ID_Start}`, `\p{ID_Continue}`,
  `\p{XID_Start}` and `\p{XID_Continue}`.

## \d, \w and /a
- Unless `/a` is in effect, `\d` matches not only 0-9 but also Arabic, Devanagari and other digits, which "may cause
  some confusion, and some security issues". Under `/a`, `\d` and `\w` are restricted to ASCII.
- `\w` matches exactly what `\p{Word}` matches: letters of any script, connector punctuation such as underscore, and
  combining marks.

## Characters and clusters
- Perl treats a "character" as a single code point; the only place it treats a sequence of code points as one logical
  character is `\X`. perlunicode also lists `\b{gcb}` and `\b{wb}` boundary forms; `\b{wb}` meets the UTS#18 word
  boundary requirement more fully than `\b`.

## Normalization
- Unicode::Normalize: `NFD` returns Normalization Form D (canonical decomposition); `NFC` is Form C (canonical
  decomposition followed by canonical composition); `NFKC` is Form KC (compatibility decomposition followed by
  canonical composition). `NFC`, `NFD`, `NFKC`, `NFKD` are exported by default.
- perlunicode on UTS#18 canonical equivalence: it is basically left to the programmer. Use NFD to write both your
  regular expressions and the text to match against them.
- Compare strings only after normalizing both to the same form.

## Self-check
- [ ] Digit and word validation uses `/a` where only ASCII is acceptable, and both sides of a comparison are
      normalized to the same form.

## Checked
Confirmed 2026-11-08 against perlrecharclass (property syntax and examples, `\d` and `/a`, `\w` and `\p{Word}`,
identifier properties), perlunicode (`\X` as the only multi-code-point logical character, Script/Script_Extensions
advice, UTS#18 notes on `\b{wb}`, `\b{gcb}` and NFD) and Unicode::Normalize (form definitions, default exports).
Removed: the `fc`/`lc`/`uc` claims and examples, charnames and Unicode::UCD calls, Unicode::GCString,
Unicode::Collate sorting, `tr///` and `\b{sb}` claims, the version-lookup one-liner and the numeric self-check,
which these pages do not establish.
Method: docs-only read of cited pages, 2026-11-08
