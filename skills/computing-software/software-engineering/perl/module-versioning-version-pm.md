---
id: computing-software.software-engineering.perl.module-versioning-version-pm
name: module-versioning-version-pm
category: computing-software
field: software-engineering
product: perl
tags: [perl, module-version, version-pm, dotted-version, semver, perlmodstyle, module-versioning-version-pm]
level: practitioner
status: docs-checked
description: "Declare $VERSION correctly, compare versions with version.pm, and avoid the decimal vs dotted-decimal traps."
sources: ["https://perldoc.perl.org/perlmodstyle", "https://perldoc.perl.org/version", "https://perldoc.perl.org/UNIVERSAL"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module versions and version objects

**Goal:** versions that compare the way you expect.

```perl
package Foo;
our $VERSION = '1.023';          # decimal: 1.023 -> compares as 1.023
# or: package Foo 1.023;
# dotted-decimal, keep on one line with use version:
use version; our $VERSION = version->declare('v1.2.3');
```
```bash
perl -MFoo -e 'print Foo->VERSION'            # reads $Foo::VERSION
perl -e 'use Foo 1.02;'                        # dies if too old
perl -Mversion -e 'print version->parse("1.2.3") > version->parse("1.2.10") ? "gt":"le"'
```

## Rules (perlmodstyle, version)
- Keep `$VERSION` a simple assignment on one line (`our $VERSION = '1.023';`); with `use version`, put `use version;` on the same line as the `$VERSION` declaration.
- A decimal version converts to dotted-decimal in groups of three digits: `version->parse(1.23)` is v1.230.0, so decimal `1.10` equals `1.1` (less than `1.9`) while dotted `v1.10` is greater than `v1.9`.
- Compare versions with `version->parse($a) <=> version->parse($b)`, never with string operators on the raw strings.
- `qv()` is marked deprecated in the version docs; prefer `version->declare('v1.2.3')`.
- perlmodstyle: a correct CPAN version is a floating point number with at least 2 digits after the decimal point; never release without incrementing it, and do not change the number of digits in your scheme.
- Developer releases use an underscore (`1.20_01`) so CPAN.pm does not list them as the most recent; the idiom `$VERSION = eval $VERSION;` keeps `use Module 0.002` from warning.
- `Module->VERSION($min)` returns the version and dies if the package version is lower than `$min`, or if either is not a lax version number.

## Self-check
- [ ] `perl -Mversion -e 'print version->parse("1.10") < version->parse("1.9") ? 1:0'` prints `1`, because decimal 1.10 equals 1.1 (not run; reasoned from the version docs).

## Checked

2026-11-02. Checked against perldoc version (parse, declare, qv deprecated, decimal to dotted-decimal conversion, alpha versions, one-line declaration), perlmodstyle (CPAN version format, underscore developer releases and the eval idiom, never release without incrementing, keep the digit count) and UNIVERSAL (VERSION method with REQUIRE). Removed: the PAUSE indexing remark, the minimum-Perl metadata advice, the cpanfile/dist.ini mention, the 1.9-after-1.10 and 'does not define' failure modes, and a garbled decimal-to-dotted switching rule.

Method: documentation only; no commands were run.
