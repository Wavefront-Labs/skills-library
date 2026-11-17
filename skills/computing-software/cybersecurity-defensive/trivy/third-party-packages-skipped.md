---
id: computing-software.cybersecurity-defensive.trivy.third-party-packages-skipped
name: third-party-packages-skipped
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [third-party, epel, false-positives, false-negatives, rpm-vendor, heuristic]
level: advanced
status: docs-checked
description: "Why Trivy skips OS packages from third-party repositories such as EPEL or NVIDIA, how it detects them heuristically, and the resulting false positive and negative risks."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/vulnerability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy skips vulnerability scanning for packages installed from third-party repositories, with EPEL, Remi, Docker and NVIDIA given as examples. Official OS security advisories do not cover them, and scanning them against those advisories would produce false positives because the advisories only track packages the OS vendor distributes.

Identification is heuristic. Trivy checks signals such as the RPM vendor field or the APT source repository. Because detection is heuristic, it may not recognise every third-party package. Unrecognised ones are still scanned against official advisories and may produce false positives. Conversely, packages from lesser-known but legitimate OS vendors may be classified as third-party and skipped, giving false negatives. The page asks you to report such cases.

The rule applies to packages matched against an OS vendor advisory. Exceptions noted on the page: a distribution whose own advisories describe the packages it rebuilds, such as Echo and RapidFort, scans them even when they are classified as third-party. Seal Security does both: its own `seal-*` packages are always scanned, while the rest are matched against the base OS vendor advisories and follow the third-party rule.

Unfixed vulnerabilities are a separate matter: those with no patch yet on the distribution can be hidden with `--ignore-unfixed`.

## Checked

2026-11-03. Read and confirmed against the Vulnerability Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the claim that reports go through a GitHub discussion in the bugs category (the page only says to report it).

Method: documentation only; no commands were run.
