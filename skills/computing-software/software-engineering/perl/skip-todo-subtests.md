---
id: computing-software.software-engineering.perl.skip-todo-subtests
name: skip-todo-subtests
category: computing-software
field: software-engineering
product: perl
tags: [perl, test-skip, test-todo, subtest, bail-out, conditional-tests, skip-todo-subtests]
level: practitioner
status: docs-checked
description: "Control test flow with Test::More SKIP and TODO blocks, todo_skip, BAIL_OUT, plan skip_all and subtests for grouped assertions."
sources: ["https://perldoc.perl.org/Test::More"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKIP, TODO, BAIL_OUT and subtests

**Goal:** express expectations that cannot always run. Everything below is from the Test::More documentation.

```perl
use Test::More;
if ($^O eq 'MacOS') { plan skip_all => 'Test irrelevant on MacOS' }
else                { plan tests => 42 }

SKIP: {
    eval { require HTML::Lint };
    skip "HTML::Lint not installed", 2 if $@;
    my $lint = new HTML::Lint;
    isa_ok( $lint, "HTML::Lint" );
    $lint->parse( $html );
    is( $lint->errors, 0, "No errors found in HTML" );
}

TODO: {
    local $TODO = "URI::Geller not finished";
    is( URI::Geller->your_card, $card, 'Is THIS your card?' );
}

subtest 'An example subtest' => sub {
    plan tests => 2;
    pass("This is a subtest");
    pass("So is this");
};
```

## Rules
- SKIP block: `skip $why, $how_many if $condition;`. It is important that `$how_many` accurately reflects the number of tests in the block so the number run matches the plan. If the plan is `no_plan`, `$how_many` is optional and defaults to 1. SKIP blocks may be nested, and each must carry the label `SKIP`.
- Skipped tests are output as special oks that Test::Harness interprets as skipped but passing.
- `plan skip_all => $reason` (or `use Test::More skip_all => $reason`) skips the whole script: it declares a skip with the reason and exits immediately with zero. A subtest may also call `plan skip_all`; no tests run and the subtest counts as a skip.
- TODO block: `local $TODO = $why;` marks tests expected to fail. They run normally but are flagged todo; the harness treats failures as ok and reports any success as an unexpected success, at which point move the test out of the block (delete the block when empty).
- If `$TODO` is unset or undef, failures are reported as normal, so `local $TODO = "..." if $condition;` marks tests as expected-to-fail only in some conditions.
- `todo_skip $why, $how_many if $condition;` is for TODO tests that cannot even run (they would die or hang). It behaves like SKIP, except the tests are marked failing but todo, which the harness treats as passing.
- When to use which: SKIP is for things the user might not be able to do (optional module missing, OS lacks fork or symlinks, no internet). TODO is for things the programmer has not done yet (unwritten code, unfixed bugs).
- Subtest: `subtest $name => \&code, @args;` runs the code as its own test with its own plan and result; the main test counts it as one test. Extra arguments are passed to the callback. A plan may be omitted, which adds an implicit `done_testing()` at the end of the subtest (not before Test::More 0.96).
- `done_testing()` must never be called inside an END block, as that bypasses the premature-exit protection of the plan.
- `BAIL_OUT($reason)` tells the harness that testing should terminate, including any additional test scripts. Use it when testing cannot continue (a critical module will not compile, a database connection fails). The test exits with 255.

## Checked
- 2026-11-08: all points confirmed on the Test::More page.
- Removed: the claim that a TODO success is reported as "TODO passed" (page says "unexpected success"), the Test::Requires and `eval { require Foo; 1 }` idioms, Test2::V0 and "Test2 underlying since 1.3" claims, failure-indent claim, advice not to use TODO for flaky tests, and the self-check, none of which the page states.
Method: docs-only read of cited pages, 2026-11-08
