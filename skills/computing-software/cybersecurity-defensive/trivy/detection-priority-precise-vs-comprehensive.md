---
id: computing-software.cybersecurity-defensive.trivy.detection-priority-precise-vs-comprehensive
name: detection-priority-precise-vs-comprehensive
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [detection-priority, precise, comprehensive, precision, recall, unspecified-versions]
level: advanced
status: docs-checked
description: "Use --detection-priority to trade false positives against false negatives, including scanning OS-installed packages with upstream advisories and unpinned version ranges."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/vulnerability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy prioritises precision: it aims to minimise false positives while accepting some false negatives. The `--detection-priority` flag controls the balance, similar to precision versus recall:

```bash
trivy image --detection-priority {precise|comprehensive} alpine:3.15
```

- `precise` (default): fewer false positives and a less noisy report, but some potential vulnerabilities may be missed.
- `comprehensive`: broader coverage with more potential false positives.

Two behaviours change in `comprehensive` mode.

Software installed via OS packages: normally only the OS vendor advisory is used. If vendor advisories are delayed or missing, `comprehensive` lets Trivy also consider upstream advisories such as the GitHub Advisory Database, which can add false positives but reduces false negatives.

Unspecified versions: when a version cannot be determined uniquely (the page's example is `package-a: ">=3.0"`), Trivy normally skips detection for that package. A lock file with fixed versions is used if present. With `comprehensive`, Trivy uses the minimum version in the range for detection, which can over-report if the actual version is higher.

The page says review is crucial in both modes: with `precise`, consider what might have been missed; with `comprehensive`, investigate each reported finding because false positives are more likely.

## Checked

2026-11-03. Read and confirmed against the Vulnerability Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
