---
id: computing-software.software-engineering.dart.dart-test-mocking-golden
name: dart-test-mocking-golden
category: computing-software
field: software-engineering
product: dart
tags: [dart, test-mocking-golden]
level: practitioner
status: docs-checked
description: "Write Dart tests with package:test groups, setUp, tags and the dart test runner flags for names, platforms and coverage."
sources: ["https://dart.dev/tools/dart-test", "https://github.com/dart-lang/test/tree/master/pkgs/test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing
- `group('String', () { test('desc', () { ... }); });` prefixes the group description onto each test's description. `setUp()` runs before every test in a group or suite and `tearDown()` after, even if the test fails.
- Run `dart test` (all tests under `test/`), `dart test path/to/test.dart`, or a directory. Select tests by name with `dart test -n "regex"` (regular expression over the full description including groups) or `-N "plain text"`; `--tags` (`-t`) and `--exclude-tags` (`-x`) select by tag.
- Tags: `@Tags(['browser'])` on a suite, or `tags: 'chrome'` on `test()`/`group()`; `@OnPlatform` and the `onPlatform` parameter configure per-platform behaviour.
- Platforms: the VM by default; `dart test -p chrome path/to/test.dart`, or `-p "chrome,vm"` for both.
- Coverage: `dart test --coverage-path=./coverage/lcov.info` writes an LCOV report to that path. Other runner controls include `--concurrency=4`, sharding with `--total-shards` and `--shard-index`, and `--test-randomize-ordering-seed`.
- Mocks and fakes (judgement, not covered by these pages): prefer a hand-written fake for simple dependencies and use a mocking package only when the interaction needs verifying.

Verify: a failing test prints the matcher description.

## Checked

Checked 2026-11-08 against https://dart.dev/tools/dart-test (read in full) and the README of the test package (https://github.com/dart-lang/test/tree/master/pkgs/test), read for the sections on groups, setUp, running, tags, platforms and coverage. Corrected: the coverage flag is `--coverage-path`, not `--coverage=coverage`. Removed (not confirmed in pages read): the mocktail API, `expectLater`/`emitsInOrder`/`throwsA(isA<...>)` matcher examples and golden testing.

Method: documentation only; no commands were run.
