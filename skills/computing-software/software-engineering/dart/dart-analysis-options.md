---
id: computing-software.software-engineering.dart.dart-analysis-options
name: dart-analysis-options
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-analysis, analysis-options]
level: practitioner
status: docs-checked
description: "Configure the analyzer with package:lints or flutter_lints, strict language modes, excludes and ignore comments."
sources: ["https://dart.dev/tools/analysis", "https://dart.dev/tools/dart-analyze"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# analysis_options.yaml, lints and strict modes
- `include: package:lints/recommended.yaml` (or `package:flutter_lints/recommended.yaml`) in `analysis_options.yaml`; included options merge in order and local options win. `linter: rules:` enables individual lints.
- Strict modes: under `analyzer: language:` set `strict-casts`, `strict-inference` and `strict-raw-types` to `true`.
- `analyzer: exclude:` takes files or globs relative to the options file (for example `build/**`); `analyzer: errors:` ignores or changes the severity of a diagnostic by name.
- `// ignore: rule` suppresses a diagnostic on one line; `// ignore_for_file: rule` suppresses it for the whole file.
- `dart analyze --fatal-infos` makes info-level issues fail the run (by default only errors and warnings do).
Verify: CI runs `dart analyze` and fails on any issue.

## Checked
2026-11-03. Confirmed against dart.dev tools/analysis (include, merge order, linter rules, three strict modes, exclude globs, errors, ignore comments) and tools/dart-analyze (`--fatal-infos`). Removed: the `core.yaml` rule set (not on the pages read).
Method: documentation only; no commands were run.
