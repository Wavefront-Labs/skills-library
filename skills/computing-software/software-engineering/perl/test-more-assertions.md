---
id: computing-software.software-engineering.perl.test-more-assertions
name: test-more-assertions
category: computing-software
field: software-engineering
product: perl
tags: [perl, test-more, is-deeply, done-testing, tap-output, cmp-ok, test-more-assertions, perl-testing-core]
level: intro
status: docs-checked
description: "Write tests with Test::More ok, is, isnt, like, cmp_ok, is_deeply, isa_ok, can_ok, diag, note and done_testing, with useful diagnostics."
sources: ["https://perldoc.perl.org/Test::More"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test::More assertions and plans

**Goal:** tests that fail with clear messages. All content is from the Test::More documentation.

```perl
use Test::More;
BEGIN { use_ok('Some::Module') }
ok($got eq $expected, 'test name');
is  ($got, $expected, 'test name');
isnt($got, $expected, 'test name');
like($got, qr/expected/, 'test name');
cmp_ok($got, '<=', $upper_limit);
is_deeply($got_structure, $expected_structure, 'test name');
can_ok('Foo', qw(this that whatever));
isa_ok($obj, 'Some::Module');
my $obj = new_ok('Some::Module' => \@args);
ok( grep(/foo/, @users), "There's a foo user" ) or diag("check that /etc/bar is set up right");
note explain \%args;
done_testing();
```

## Rules
- Plan: `use Test::More tests => 23;`, or `done_testing()` at the end when the count is unknown (`done_testing($n)` to also check the count). `done_testing()` replaces the "no_plan" plan and must never be put in an END block.
- Give every test a name. It is optional but strongly encouraged, and makes failures easy to find.
- `ok` passes on a true expression. `is`/`isnt` compare with `eq`/`ne` and show got/expected on failure; `undef` only matches `undef`. Do not use `is` to test truth, e.g. `is(exists $h{x}, 1)` checks the value is 1, not that it is true; use `ok`.
- `like`/`unlike` match against a `qr//` regex (or a string like `'/expected/i'`).
- `cmp_ok($got, $op, $expected)` takes any binary Perl operator and shows both values on failure; useful for numeric comparison where `is`'s `eq` would interfere, and for `<=`-style bounds.
- `can_ok($class_or_object, @methods)` counts as one test regardless of how many methods; loop over methods for one test each.
- `isa_ok` also checks the object was defined; it works on classes and on references (`isa_ok($ref, 'ARRAY')`). `new_ok($class => \@args, $name)` is `$class->new(@args)` plus `isa_ok`, and assumes `new` returns a single object.
- `is_deeply` walks references and shows where they start differing. It compares dereferenced values, so blessing and ties are not considered different; function refs and globs are only checked for the same referent; it unoverloads arguments, so avoid it with overloaded objects.
- `use_ok` should run inside `BEGIN { }` so functions are exported at compile time and prototypes are honoured; for just loading a module, `require_ok` is recommended. Do not put dependent code in the same BEGIN block.
- `diag` prints a diagnostic that will not interfere with test output and returns false (so `ok(...) or diag(...)` works). `note` is like `diag` but is not seen under a harness, only in the verbose TAP stream. `explain` dumps references in a readable form, normally passed to `note` or `diag`.
- `pass`/`fail` are synonyms for `ok(1)`/`ok(0)`; use very sparingly.
- Exit code: 0 if all pass, 255 if the test died or ran the wrong number of tests, otherwise the number of failures (capped at 254).
- Avoid `eq_array`, `eq_hash`, `eq_set`; the page discourages them as they give no diagnostics and says `is_deeply` is better.

## Checked
- 2026-11-08: all points confirmed on the Test::More page.
- Removed: the "is('1.0', 1) fails" example, the claim that a mid-test die gives "Dubious, test returned" (the page gives exit code 255 only), the File::Temp and `perl -Ilib` advice, Test::Deep and Test2::V0 advice, the self-check, and the Test::Tutorial source (not read).
Method: docs-only read of cited pages, 2026-11-08
