---
id: computing-software.software-engineering.perl.perl-version-support-policy
name: perl-version-support-policy
category: computing-software
field: software-engineering
product: perl
tags: [perl, perlpolicy, perl-releases, perldelta, deprecations, perl-version-support-policy]
level: practitioner
status: docs-checked
description: "Plan which Perl versions to support: 5.X.Y numbering, perlpolicy support window, reading perldelta and handling deprecations."
sources: ["https://perldoc.perl.org/perlpolicy", "https://perldoc.perl.org/perldelta", "https://perldoc.perl.org/perlhist", "https://perldoc.perl.org/perldeprecation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Perl release cycle, support policy and deprecations

**Goal:** pick a minimum Perl and keep code upgrade-ready.

## Facts (perlpolicy; re-read it for the current state)
- Perl uses 5.X.Y numbering. Even X is a stable series (5.40, 5.42), odd X is a development series leading to the next stable one, and Y increments in a stable series are maintenance releases (critical bug fixes and security patches only). A new stable series is typically produced once a year.
- Support commitment: the project attempts to fix critical issues in the two most recent stable series (current series first), and to provide critical security patches for any series whose 5.x.0 release was within the past three years, only for the most recent .y release of that series. No fixes for development releases.
- perlpolicy carries a table of "officially" supported tracks: current stable and previous stable get full support, the one before that gets security fixes only, anything older is end of life. Read the table in the page for the live versions.
- Vendors are encouraged to ship the most recent supported release at their code freeze.
- Each release has a perldelta page describing what changed; read it before upgrading.

## Deprecation terms (perlpolicy)
- experimental: may change, be deprecated or removed without notice; a feature must be experimental in two stable releases before it is marked non-experimental.
- deprecated: may be removed later (or not). Backward-incompatible changes generally warn for two release cycles before removal, sometimes after one. Since Perl 5.12 deprecated features warn when used. A deprecated core module is also made available on CPAN, and installing it from CPAN silences the warning.
- discouraged: considered a mistake but not currently a removal candidate.
- removed: no longer in core; a removed module continues to be available on CPAN.
- `perldeprecation` lists what is deprecated, grouped by the version in which it disappears, with alternatives.

## How to choose a minimum version
1. Check what your deployment targets ship.
2. Pick the language features you need and confirm the version that introduced each in the perldelta of that release (perlhist lists releases, not features).
3. Make the declared minimum explicit in code and dist metadata, and test a CI matrix of the oldest supported and the latest stable Perl.

## Handling deprecations
- Deprecations have warning categories (for example `deprecated::dot_in_inc`, `deprecated::subsequent_use_version`). `use warnings FATAL => 'deprecated'` in tests turns them into failures; perldoc warns that `FATAL => 'all'` in general is discouraged.
- Example from perldeprecation: `.` was removed from `@INC` in Perl 5.26 for security reasons; `do EXPR` on a bare filename found only in `.` now produces a deprecation warning and the file is not loaded.
- Example: after `use v5.11` or higher, a later `use VERSION` requesting an earlier version was deprecated in 5.36 and is fatal in 5.40.
- Literal unescaped `{` in regex patterns was deprecated in 5.20 and made fatal in stages (5.26, 5.30, 5.32); escape it as `\{` or `[{]`.
- The `diagnostics` pragma and the `splain` program explain warning and error messages.

## Self-check
- [ ] CI runs the oldest supported and newest stable Perl.
- [ ] The perldelta of every release between them has been read for removals.

## Checked
2026-11-09. Read in full: perlpolicy (versioning, support table and commitments, terminology), perldeprecation (5.26 dot in INC, 5.40 downgrade, 5.32 left brace). Confirmed: even/odd series, yearly cadence, two-series and three-year commitments, two-cycle deprecation, 5.12 warnings. Removed as not stated on these pages or unreadable sources: per-feature introduction versions (say/state, postfix deref, signatures, try/catch, class), the 5.22 and 5.38 removal examples, `my $_`, Module::CoreList, Perl::MinimumVersion and perlver, the shebang and Docker advice, cpanfile syntax. perldelta and perlhist were not used for specific claims.
Method: documentation only; no commands were run.
