---
id: computing-software.software-engineering.dart.dart-pubspec-constraints-overrides
name: dart-pubspec-constraints-overrides
category: computing-software
field: software-engineering
product: dart
tags: [dart, pubspec-constraints-overrides]
level: practitioner
status: docs-checked
description: "Manage Dart dependencies: caret constraints, dev_dependencies, dependency_overrides, git and path sources, pub commands."
sources: ["https://dart.dev/tools/pub/dependencies", "https://dart.dev/tools/pub/cmd/pub-upgrade", "https://dart.dev/tools/pub/versioning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pubspec
- `http: ^1.2.0` under `dependencies:` means `'>=1.2.0 <2.0.0'`. The SDK constraint lives under `environment: sdk:`.
- Pub commands: `dart pub get`, `upgrade`, `outdated`, `deps`, `add <pkg>`, `remove <pkg>`, `downgrade`; `dart pub upgrade --major-versions` rewrites constraints to allow the latest major versions (preview with `--dry-run`).
- Commit `pubspec.lock` for apps. `dependency_overrides` only counts in the root package's own pubspec; overrides inside dependencies are ignored.
- Git and path sources: `pkg: {git: {url: ../foo.git, ref: branch, path: subdir}}`, `pkg: {path: ../foo}`. A package with path dependencies cannot be uploaded to pub.dev.
Verify: `dart pub outdated` lists upgradable entries.

## Checked
2026-11-03. Confirmed against dart.dev tools/pub/dependencies (constraint syntax, git and path forms, overrides root-only, path deps not uploadable), tools/pub/cmd/pub-upgrade (`--major-versions`, `--dry-run`) and tools/pub/versioning (lockfile for apps). Removed: a specific SDK constraint example marked "confirm current".
Method: documentation only; no commands were run.
