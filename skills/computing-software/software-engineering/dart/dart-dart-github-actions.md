---
id: computing-software.software-engineering.dart.dart-dart-github-actions
name: dart-dart-github-actions
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-ci, dart-github-actions]
level: practitioner
status: docs-checked
description: "Set up GitHub Actions CI for Dart: setup-dart, format check, analyze, test and an SDK matrix."
sources: ["https://github.com/dart-lang/setup-dart", "https://dart.dev/tools/dart-format", "https://dart.dev/tools/dart-analyze"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions for Dart packages
- Use `actions/checkout` then `dart-lang/setup-dart@v1`. Its `sdk` input takes a channel (`stable`, `beta`, `dev`, `main`), a release such as `3.1`, or an exact version; the default installs the latest stable SDK.
- Steps: `dart pub get`, `dart format --output=none --set-exit-if-changed .`, `dart analyze` (add `--fatal-infos` to fail on info-level issues), `dart test`.
- Matrix: set `sdk: ${{ matrix.sdk }}` over a list such as `[3.1, stable, beta]`, optionally across operating systems.
- For packages, also run `dart pub downgrade` and then test, so the lower bounds in your constraints are exercised.
Verify: the workflow passes on a fresh clone.

## Checked
2026-11-03. Confirmed against the dart-lang/setup-dart README (usage workflow, `sdk` input forms, matrix example), dart.dev tools/dart-analyze (`--fatal-infos`) and tools/pub/cmd/pub-downgrade (lowest versions). Removed: the `~/.pub-cache` caching recommendation and the `sdk: stable` input line (the README shows stable is what the default installs, and the channel list as above).
Method: documentation only; no commands were run.
