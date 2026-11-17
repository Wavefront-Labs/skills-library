---
id: computing-software.cybersecurity-defensive.trivy.license-scanning-classification-and-severity
name: license-scanning-classification-and-severity
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [license-scanning, license-full, google-license-classification, forbidden, restricted, unknown-license]
level: practitioner
status: docs-checked
description: "Scan packages for licenses with --scanners license, understand classification-to-severity mapping, and when --license-full adds file-level scanning."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/license/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy scans container images for license files and gives an opinionated view of license risk. Licenses are classified using the Google License Classification: Forbidden, Restricted, Reciprocal, Notice, Permissive, Unencumbered and Unknown. Licenses Trivy fails to recognise are UNKNOWN; the page recommends checking those too because they may be in violation.

Classification maps to severity:

| Classification | Severity |
| --- | --- |
| Forbidden | CRITICAL |
| Restricted | HIGH |
| Reciprocal | MEDIUM |
| Notice | LOW |
| Permissive | LOW |
| Unencumbered | LOW |
| Unknown | UNKNOWN |

Standard scanning covers packages installed by `apk`, `apt-get`, `dnf`, `npm`, `pip`, `gem` and similar:

```shell
trivy image --scanners license --severity UNKNOWN,HIGH,CRITICAL alpine:3.15
```

The result is an `OS Packages (license)` table with Package, License, Classification and Severity, for example GPL-2.0 classified Restricted and HIGH.

`--license-full` adds scanning of source code files, Markdown documents, text files and `LICENSE` documents. The result gains a `Loose File License(s)` section listing file locations, such as an AGPL-3.0 `LICENSE` classed Forbidden and CRITICAL. The page warns full scanning is expensive and takes a while.

Support by target: standard scanning works for image, rootfs, filesystem, repository and SBOM; full scanning works for image, rootfs, filesystem and repository, but not SBOM. For filesystem and repository, some lock files need additional files, such as cache directory files, to detect licenses.

## Checked

2026-11-03. Read and confirmed against the License Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
