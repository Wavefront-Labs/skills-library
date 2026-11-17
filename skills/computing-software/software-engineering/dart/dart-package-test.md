---
id: computing-software.software-engineering.dart.dart-package-test
name: dart-package-test
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-testing, package-test]
level: practitioner
status: docs-checked
description: "Write package:test unit tests with expect, equals, setUp and tearDown, and run them with dart test, names, tags and platforms."
sources: ["https://dart.dev/tools/dart-test", "https://github.com/dart-lang/test/tree/master/pkgs/test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# package:test groups, expectations and the runner
- `dart test` runs tests that use `package:test` under the project's `test` directory; pass files or directories to run a subset. Use `flutter test` for Flutter code.
- Write assertions with `expect(actual, equals(expected))`; share code with `setUp()` and `tearDown()` (tearDown runs even if the test fails) and `setUpAll`/`tearDownAll` per suite.
- Filter with `--name`/`-n` (substring match), `--tags`/`-t` and `--exclude-tags`/`-x`; repeated filters must all match. `-p chrome` or `-p "chrome,vm"` selects platforms.
- Tags are declared with `@Tags([...])` on a suite or the `tags` argument; `dart_test.yaml` configures the runner. Tests time out after 30 seconds of inactivity by default; use `@Timeout` or the `timeout` parameter to change it.
- Coverage: `dart run test --coverage-path=./coverage/lcov.info` writes lcov data.
Verify: break the function and confirm the failure message is readable.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-test and the package:test README (expect/equals, setUp/tearDown, setUpAll, filter flags, platforms, tags, dart_test.yaml, timeouts, `--coverage-path`). Removed: `test/*_test.dart` naming, `throwsA`, `closeTo`, `completion`, `emitsInOrder` examples, `--coverage=coverage` with `package:coverage` (not on the pages read).
Method: documentation only; no commands were run.
