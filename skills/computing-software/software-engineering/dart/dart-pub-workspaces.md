---
id: computing-software.software-engineering.dart.dart-pub-workspaces
name: dart-pub-workspaces
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-workspaces, pub-workspaces]
level: advanced
status: docs-checked
description: "Manage multi-package repositories with pub workspaces (Dart 3.6 or newer)."
sources: ["https://dart.dev/tools/pub/workspaces"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub workspaces
- Workspaces need Dart 3.6.0 or newer: every workspace package's SDK constraint must be at least `^3.6.0`.
- The root `pubspec.yaml` lists members under `workspace:`; each member sets `resolution: workspace`. Listing a member's own sub-packages in its `workspace:` entry also includes them.
- `dart pub get` anywhere in the repo creates one `pubspec.lock` next to the root pubspec for all members, and deletes stray lockfiles and `package_config.json` files in between.
- One shared resolution means one version of each package; conflicts are more likely. You can override a package only once in the workspace, so keep `dependency_overrides` in the root pubspec.
- To resolve a member on its own temporarily, reset `resolution` in a `pubspec_overrides.yaml` next to it.
Verify: `dart pub deps` shows consistent versions.

## Checked
2026-11-03. Confirmed against dart.dev tools/pub/workspaces. Removed: the melos paragraph and `melos run test` (third-party, not on the page), the "dart test runs per package" line, and "internal dependencies use workspace resolution instead of path overrides".
Method: documentation only; no commands were run.
