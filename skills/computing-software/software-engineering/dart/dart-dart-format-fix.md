---
id: computing-software.software-engineering.dart.dart-dart-format-fix
name: dart-dart-format-fix
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-analysis, dart-format-fix]
level: intro
status: docs-checked
description: "Format code with dart format and apply automated fixes with dart fix."
sources: ["https://dart.dev/tools/dart-format", "https://dart.dev/tools/dart-fix"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart format and dart fix
- `dart format .` rewrites files; `dart format -o none --set-exit-if-changed .` checks in CI (exit code reports changes).
- Page width defaults to 80; set it with a top-level `formatter:` section in `analysis_options.yaml` (`page_width: 123`). Configurable formatter options need language version 3.7 or newer, and the `trailing_commas` option needs 3.8.
- By default the formatter adds trailing commas to argument and parameter lists that split across lines and removes them from ones that do not; the `trailing_commas` option can preserve them.
- `dart fix --dry-run` previews fixes; `dart fix --apply` applies them; `--code=<diagnostic>` limits it to named diagnostics. `dart fix` also applies data-driven fixes that package authors ship for API migrations.
Verify: running format twice produces no changes.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-format (80 default, `page_width`, `--set-exit-if-changed`, version gates 3.7 and 3.8) and tools/dart-fix (`--dry-run`, `--apply`, `--code`, data-driven fixes). Removed: the "tall style / legacy style" wording and the unverified `--output=none` long form (page shows `-o none`).
Method: documentation only; no commands were run.
