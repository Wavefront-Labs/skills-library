---
id: computing-software.software-engineering.perl.test-deep-fatal-warnings
name: test-deep-fatal-warnings
category: computing-software
field: software-engineering
product: perl
tags: [perl, test-deep, test-fatal, test-warnings, exception-testing, cmp-deeply, test-deep-fatal-warnings, perl-testing-tools]
level: practitioner
status: docs-checked
description: "Test exceptions with Test::Fatal's exception block and warnings with Test::Warnings (warning, warnings, allow_patterns, automatic no-warnings test)."
sources: ["https://metacpan.org/pod/Test::Fatal", "https://metacpan.org/pod/Test::Warnings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test::Fatal and Test::Warnings

**Goal:** precise assertions about errors and warnings. (Test::Deep structure matching is not covered by this checked version; use its own docs.)

## Exceptions with Test::Fatal
```perl
use Test::More;
use Test::Fatal;                         # exports exception
is( exception { might_die() }, undef, 'the code lived' );
like( exception { might_die() }, qr/turns out it died/, 'died as expected' );
isa_ok( exception { might_die() }, 'Exception::Whatever', 'the thrown exception' );
```
- `exception { ... }` returns the exception thrown or undef. It performs no TAP assertion itself; combine it with `is`, `like`, `isa_ok`.
- Optional exports: `dies_ok` / `lives_ok` (give TAP output, meant as a porting aid from Test::Exception; the author does not suggest them otherwise) and `success` (a Try::Tiny helper that runs only if the try block did not die).
- It does not alter the call stack (unlike Test::Exception's `caller` override). If exceptions carry stack traces with arguments, a helper like `exception_like(sub {...}, qr/foo/, 'name')` can falsely pass because the test name or pattern appears in the trace. Write `like( exception { ... }, qr/foo/, 'name' )` directly. `$Carp::MaxArgNums` is set to -1 inside the block to reduce this.
- Avoid `isnt( exception { ... }, undef )`: it passes for the wrong reason if the block has an unrelated mistake. Test for the class, identifier or message.
- Unblessed false exceptions (0 or empty string) make Test::Fatal die (perls before 5.14); use `is`, not `ok`, around `exception` in that case.

## Warnings with Test::Warnings
```perl
use Test::More;
use Test::Warnings qw(:all);             # default import only adds the end test
like( warning { f() }, qr/deprecated/, 'got a warning' );
is_deeply( [ warnings { g() } ], [ 'msg 1', 'msg 2' ], 'expected warnings' );
done_testing;                            # also emits "no (unexpected) warnings"
```
- Loading the module adds an extra test that fails if any unexpected warning was issued; it runs before `done_testing` counts tests (or in an END block), so it works with or without a plan. It is a drop-in replacement for Test::NoWarnings.
- Functions (import by name or `:all`): `warnings { }` returns all warnings from the block (not propagated further), `warning { }` returns the single warning or an arrayref if there were none or several (capture it in a variable and `diag` it when the test fails), `had_no_warnings($name)`, `allow_patterns(qr/.../)` (allow-list; saved in a lexical variable it applies only to that scope), `disallow_patterns`, and the experimental `allow_warnings`.
- Import options: `:no_end_test`, `:fail_on_warning` (fail at the warning; the author recommends it only while debugging), `:report_warnings`. `PERL_TEST_WARNINGS_ONLY_REPORT_WARNINGS=1` turns failures into reports.
- To avoid new Perl warnings breaking installs, load it only in author tests: `use if $ENV{AUTHOR_TESTING} || $ENV{RELEASE_TESTING}, 'Test::Warnings';`.
- Same stack-trace caveat as above: do not wrap `warning` in a helper that passes the test name. Other modules with their own warn handlers (Devel::Confess, diagnostics) interfere with capture. `use Test::Warnings 'warnings'` imports a `warnings` sub, which prevents `warnings->import` in that package.

## Self-check
- [ ] A test that warns without being allowed fails at the end with the warning text reported.

## Checked
Method: 2026-11-08 read the full plain-text POD of Test::Fatal 0.019 and Test::Warnings 0.038 via the MetaCPAN API. Test::Deep was not read, so its combinators and the Test::Exception/Test::Warn examples were removed and its URL dropped from sources. The rule "prefer Test::Fatal over Test::Exception" is only partly supported (the page calls it a simpler alternative).
