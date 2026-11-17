---
id: computing-software.cybersecurity-defensive.trivy.filter-package-types-with-pkg-types
name: filter-package-types-with-pkg-types
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [pkg-types, os-packages, library-packages, scanning-scope, sbom-impact]
level: practitioner
status: docs-checked
description: "Restrict a Trivy scan to OS packages or language library packages with --pkg-types, and note that the flag also changes package lists in JSON reports and SBOMs."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/vulnerability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Trivy scans both OS packages and language-specific packages. The `--pkg-types` option enables only chosen package types. It takes a comma-separated list with two available values:

- `os`: OS packages managed by the OS package manager, such as `dpkg`, `yum` and `apk`.
- `library`: language-specific packages, such as those installed by `pip`, `npm` or `gem`.

Example from the page, scanning only OS packages in a Ruby image:

```bash
trivy image --pkg-types os ruby:2.4.0
```

The documented output lists the vulnerability database update, then Alpine detection, and a table of OS libraries such as curl, git, libssh2, sqlite and tar with their vulnerability IDs, severity, installed version and fixed version.

Note the page's info box: this flag filters the packages themselves, not only the findings. It therefore also affects the list of detected packages in JSON reports and in SBOM generation. A BOM produced with `--pkg-types os` will not contain library packages.

Contrast with `--scanners`, which selects which scanners run (for example `--scanners vuln` to disable secret scanning), rather than which package types are detected.

## Checked

2026-11-03. Read and confirmed against the Vulnerability Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
