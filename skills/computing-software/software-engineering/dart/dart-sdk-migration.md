---
id: computing-software.software-engineering.dart.dart-sdk-migration
name: dart-sdk-migration
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-sdk-versions, sdk-migration]
level: advanced
status: docs-checked
description: "Manage SDK constraints, language versions and breaking-change migrations with dart fix."
sources: ["https://dart.dev/tools/dart-fix", "https://dart.dev/tools/pub/pubspec", "https://dart.dev/language/records"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDK constraints and language versions
- The lower bound of `environment: sdk:` in `pubspec.yaml` (for example `^3.2.0`) is what enables language features; each feature page states its minimum language version (records and class modifiers need 3.0, digit separators 3.6, wildcard variables 3.7).
- Raise the lower SDK constraint before using a newer feature; `dart fix` docs show this for super-initializer parameters (2.17).
- Run `dart fix --dry-run` then `dart fix --apply` for automated and data-driven migrations; the Dart 3 migration guide covers manual steps.
- `dart --version` prints the installed SDK version.
Verify: CI runs on the minimum and latest SDK you support.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-fix (lower SDK constraint, `--dry-run`, `--apply`, Dart 3 migration guide link), tools/pub/pubspec (`environment: sdk:` caret form), and the language pages records, class-modifiers, built-in-types and variables for minimum language versions. Removed: the `// @dart=3.0` comment, the `fvm`/`asdf` tools, and the old-style range example.
Method: documentation only; no commands were run.
