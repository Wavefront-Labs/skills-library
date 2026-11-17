---
id: computing-software.software-engineering.dart.dart-pubspec-dependencies
name: dart-pubspec-dependencies
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-pub, pubspec-dependencies]
level: practitioner
status: docs-checked
description: "Declare dependencies with caret constraints, use dev_dependencies and overrides, and commit the lockfile for apps."
sources: ["https://dart.dev/tools/pub/dependencies", "https://dart.dev/tools/pub/versioning", "https://dart.dev/tools/pub/cmd/pub-downgrade"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pubspec.yaml, version constraints and pub commands
- `dart pub add http`, `dart pub get`, `dart pub upgrade --major-versions`, `dart pub outdated`, `dart pub deps`.
- Set an SDK constraint under `environment: sdk:` (for example `^3.3.0`). Caret `^1.2.3` means `'>=1.2.3 <2.0.0'`; for 0.x versions `^0.1.2` means `'>=0.1.2 <0.2.0'`. Quote any constraint that contains `>`.
- Put packages imported only from test or example in `dev_dependencies`; pub ignores the dev dependencies of packages you depend on.
- Commit `pubspec.lock` for applications so every machine builds with the same versions.
- `dependency_overrides` temporarily override a dependency (a path or a version); only the overrides in your own pubspec count, and they are ignored by users of a published package. A package with path dependencies cannot be uploaded to pub.dev.
- `dart pub downgrade` resolves the lowest versions allowed by your constraints, so use it to test lower bounds.
Verify: `dart pub get` is clean and `dart pub outdated` reports no unexpected majors.

## Checked
2026-11-03. Confirmed against dart.dev pages tools/pub/dependencies (caret and range syntax, quoting, dev dependencies, overrides, path dependencies not uploadable), tools/pub/versioning (lockfile committed for apps), tools/pub/cmd/pub-upgrade (`--major-versions`) and tools/pub/cmd/pub-downgrade. Removed: the claim that libraries should not commit `pubspec.lock` (not on the pages read) and the claim that git dependencies cannot be published.
Method: documentation only; no commands were run.
