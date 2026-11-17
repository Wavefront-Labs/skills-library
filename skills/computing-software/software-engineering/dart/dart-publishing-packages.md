---
id: computing-software.software-engineering.dart.dart-publishing-packages
name: dart-publishing-packages
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-pub, publishing-packages]
level: advanced
status: docs-checked
description: "Prepare, dry-run and publish a package with a proper layout, changelog and licence; retract bad versions."
sources: ["https://dart.dev/tools/pub/publishing", "https://dart.dev/tools/pub/package-layout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing to pub.dev
- Include a `LICENSE` file, a `CHANGELOG.md` and the standard pubspec fields; follow the package layout conventions (`lib/`, `lib/src/` for private code, `test/`, `example/`).
- `dart pub publish --dry-run` lists the files that would be published and validates the package; inspect the list, then remove `--dry-run` to upload. Use `.pubignore` or `.gitignore` to leave files out.
- Versions are not deleted: within seven days of publication you can retract one on the package Admin tab (restorable for seven days). Prefer publishing a fixed version unless the dependency constraints are wrong.
- After the first manual publish, automated publishing is available through GitHub Actions or Google Cloud service accounts.
Verify: the dry run reports no warnings.

## Checked
2026-11-03. Confirmed against dart.dev tools/pub/publishing (LICENSE, CHANGELOG.md, `--dry-run`, .pubignore, retraction rules, automated publishing) and tools/pub/package-layout. Removed: the OIDC wording and the pub points description (not on the pages read).
Method: documentation only; no commands were run.
