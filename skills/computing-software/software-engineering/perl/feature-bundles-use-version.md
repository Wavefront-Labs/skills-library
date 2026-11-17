---
id: computing-software.software-engineering.perl.feature-bundles-use-version
name: feature-bundles-use-version
category: computing-software
field: software-engineering
product: perl
tags: [perl, feature-bundle, use-v5-36, say-feature, state-feature, builtin, feature-bundles-use-version]
level: practitioner
status: docs-checked
description: "Enable language features per file with use v5.xx or use feature, and know what each bundle turns on and off."
sources: ["https://perldoc.perl.org/feature", "https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/builtin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# use VERSION and feature bundles

**Goal:** choose one declaration that sets the language level for a file.

```perl
use v5.36;        # bundle :5.36 + strict + warnings (5.36 and later)
use v5.10;        # say, state, switch features (older style)
use feature qw(say state signatures postderef_qq);
no feature 'indirect';                    # turn one off
use builtin qw(true false is_bool trim ceil floor reftype blessed);   # 5.36+ (some experimental until 5.40)
```

## Bundle highlights
| Bundle | Adds (cumulative notes) |
|---|---|
| :5.10 | `say`, `state`, `switch`; :5.12 adds `unicode_strings` |
| :5.16 | `current_sub`, `fc`, `evalbytes`, `unicode_eval` |
| :5.24 | `postderef_qq` (postfix dereference interpolation) |
| :5.28 | `bitwise` (separate numeric/string bit ops) |
| :5.36 | `signatures`, `isa`; removes `indirect`, `multidimensional`, `switch` |
| :5.38 | removes `bareword_filehandles` (except STDIN etc.); `module_true` |
| :5.40 | `try` (`try`/`catch`) |

(Source: the bundle table in the feature documentation; later bundles drop further legacy features.)

## Rules
- `use v5.12` or higher turns on `strict`; a version of 5.35.0 or higher (so `use v5.36`) also turns on `warnings` (perlfunc).
- `use VERSION` raises an exception if VERSION is greater than the running perl (perlfunc).
- Feature scope is lexical (file or block); features do not leak into modules you load.
- Experimental features warn in the `experimental::X` category unless you disable it with `no warnings "experimental::X"`; they can change.

## Self-check
- [ ] `perl -E 'say "hi"'` works (`-E` enables the current bundle).

## Checked
2026-11-03: confirmed against the feature documentation (bundle table :5.10 to :5.44, lexical scope, -E switch, experimental warning categories), the builtin documentation (functions available from 5.36, non-experimental in the 5.40 bundles) and perlfunc use VERSION (strict from 5.12, warnings from 5.35.0, exception when the version is too new). Fixed the bundle table (unicode_strings arrives in :5.12, unicode_eval in :5.16, try is not described as stable). Removed: experimental.pm, the exact error message and the indirect self-check.
Method: documentation only; no commands were run.
