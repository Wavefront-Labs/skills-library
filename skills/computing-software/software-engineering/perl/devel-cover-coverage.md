---
id: computing-software.software-engineering.perl.devel-cover-coverage
name: devel-cover-coverage
category: computing-software
field: software-engineering
product: perl
tags: [perl, devel-cover, coverage-report, cover-command, statement-coverage, uncoverable, devel-cover-coverage]
level: practitioner
status: docs-checked
description: "Measure statement, branch, condition, subroutine and pod coverage with Devel::Cover and the cover command; select files and mark uncoverable code."
sources: ["https://metacpan.org/pod/Devel::Cover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code coverage with Devel::Cover

**Goal:** find untested code (documented version 1.52).

```bash
cover -test                                          # uncommitted module: run tests with coverage, build report
cover -delete                                        # or by hand: clear old data in cover_db
HARNESS_PERL_SWITCHES=-MDevel::Cover make test       # (for prove: same variable)
cover                                                # build the reports
./Build testcover                                    # Module::Build 0.26+
dzil cover                                           # Dist::Zilla, with Dist::Zilla::App::Command::cover
PERL5OPT=-MDevel::Cover make test                    # if the module does not use the t/*.t framework
perl -MDevel::Cover yourprog args ; cover            # a program
perl -MDevel::Cover=-db,cover_db,-coverage,statement,time yourprog args   # change defaults
```

## Facts from the docs
- Reports: statement, branch, condition, subroutine and pod coverage (pod via Pod::Coverage, or Pod::Coverage::CountParents if installed). Statement and sub data should be accurate; branch and condition data "mostly accurate, although not always what one might initially expect". Criteria for `-coverage`: statement, branch, condition, path, subroutine, pod, time, all, none. The statement-timing facility should not be relied on; use Devel::NYTProf for profiling.
- `cover` ships various HTML reports, text, a compiler-error-style missing-coverage report and a Vim report. The default HTML report is `html_minimal`; with uncoverable markers prefer `html_basic`. Syntax-highlighted HTML needs Template plus PPI::HTML or Perl::Tidy. Annotations (for example git blame) can be added.
- Requires perl 5.20.0+ for v1.52 and a C compiler and make (it uses XS). Different perl versions can give slightly different results.
- Options: `-db`, `-dir`, `-ignore RE`, `+ignore RE`, `-inc`, `+inc`, `-select RE`, `+select RE`, `-merge` (default on, for multiple test benches), `-silent`, `-subs_only`, `-summary`, `-loose_perms`. Regexes are given without `//`; multiple values are comma separated with no space.
- File selection: a file matching `select` is included; otherwise matching `ignore` excludes it; otherwise files under an `inc` directory (initially perl's `@INC`) are excluded; else included. `-ignore` replaces the default ignore list, `+ignore` appends. Example: `cover -test -silent +ignore ^t/lib/,Foo.pm$`.
- Environment: `-silent` is on when invoked through `HARNESS_PERL_SWITCHES` or `PERL5OPT`; `DEVEL_COVER_OPTIONS` is appended to the options. Modules loaded by `-M` on the command line are not covered when Devel::Cover comes in via an environment variable, so put it on the command line instead.
- Under mod_perl, `use Devel::Cover;` early in startup or `PerlSwitches -MDevel::Cover=-silent,1`.
- The DB is stored with Sereal, else JSON (JSON::MaybeXS), else Storable. `gcov2perl` converts gcov data so C/XS coverage can sit with Perl coverage.

## Uncoverable code
Mark genuinely unreachable code as a last resort so it is not counted as an error (it is an error if it is covered, unless `class:ignore_covered_err`):
```perl
$impossible++;  # uncoverable statement
# uncoverable branch true
# uncoverable condition right
# uncoverable condition false
if ($x && !$y) { ... }
sub z { # uncoverable subroutine
```
- Use `count:n` for the nth statement or branch on a line (for `elsif`). A `note:` attribute documents the reason.
- Non-invasive alternative: a `.uncoverable` file in the current or home directory (or `-uncoverable_file`), managed with `cover -add_uncoverable_point "$file $criterion $line $count $type $class $note"`. `-delete_uncoverable_point` and `-clean_uncoverable_points` are unimplemented.

## Limits
- You cannot cover failure paths for modules Devel::Cover itself uses (B, B::Deparse, Carp, Cwd, Digest::MD5, File::Path, File::Spec, Storable/JSON/Sereal): a runtime `require` of them will succeed under coverage.
- Redefined subroutines may not be reported; Test::TestCoverage should not be combined with it. xor conditions are not properly handled.

## Self-check
- [ ] `cover` lists `lib/` files with per-criterion percentages and the uncoverable markers do not show as uncovered in `html_basic`.

## Checked
Method: 2026-11-08 read the full plain-text POD of Devel::Cover 1.52 via the MetaCPAN API. Removed unsupported v1 claims (2 to 10 times slowdown, threads, Coveralls/Codecov plugins, `-report` examples, `.gitignore` advice, parallel `prove -j` notes).
