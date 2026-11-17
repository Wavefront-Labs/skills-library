---
id: computing-software.cybersecurity-defensive.trivy.secret-skip-patterns-and-speed
name: secret-skip-patterns-and-speed
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [skip-patterns, doublestar, glob, skip-dirs, skip-files, secret-performance]
level: advanced
status: docs-checked
description: "Replace the default secret-scan skip list with skip-patterns globs, and apply the documented recommendations to speed up secret scanning on large images."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/secret/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Trivy skips certain paths during secret scanning, expressed as doublestar glob patterns. They include `**/.git/**`, `**/node_modules/**`, lock files such as `**/go.sum`, `**/package-lock.json`, `**/yarn.lock`, `**/pnpm-lock.yaml`, `**/Pipfile.lock` and `**/Gemfile.lock`, image and document types such as `**/*.jpg`, `**/*.png`, `**/*.pdf` and `**/*.bin`, and archives or packages such as `**/*.zip`, `**/*.gz`, `**/*.tar`, `**/*.deb` and `**/*.rpm`.

Override the list with `skip-patterns` in the secret config file:

```yaml
skip-patterns:
  - "**/vendor/**"
  - "**/testdata/**"
  - "**/custom.lock"
  - "**/*.xyz"
```

Important: when `skip-patterns` is specified it replaces the default list entirely. Defaults are not merged, so include the ones you want to keep. To disable all skipping set `skip-patterns: []`.

Speed recommendations from the page:
- Use `--skip-dirs` or `--skip-files`, or `skip-patterns`, to avoid files that need no scanning, such as test secrets.
- In image scanning Trivy walks the tree from `/` and scans every file outside the built-in allowed paths, which is slow for images with many files. Glob patterns such as `**/vendor/**` skip those paths entirely.
- Use `allow-rules` to suppress known matches.
- Use `enable-builtin-rules` or `disable-rules` to run fewer rules.
- Disable secret scanning with `--scanners` if you do not need it.

## Checked

2026-11-03. Read and confirmed against the Secret Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
