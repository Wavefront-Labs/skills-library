---
id: computing-software.cybersecurity-defensive.trivy.scan-asset-version-support-and-end-of-updates
name: scan-asset-version-support-and-end-of-updates
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [scan-assets, trivy-db, trivy-java-db, trivy-checks, schema-version, upgrade-policy]
level: advanced
status: docs-checked
description: "How Trivy CLI versions tie to vulnerability DB, Java index DB and checks bundle versions, and what happens when updates for an old asset version end."
sources:
  - https://trivy.dev/latest/docs/guide/references/compatibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some scan assets use versioned formats tied to particular Trivy CLI versions:

- Vulnerability Database (trivy-db): schema version.
- Java Index Database (trivy-java-db): schema version.
- Checks Bundle (trivy-checks): major version.

Each CLI version is compatible with particular versions of these assets. Release notes identify breaking changes and give migration guidance whenever possible. When updates for an older asset version end, CLI versions that depend on it can no longer receive newly published vulnerability information, Java artifact identification data or misconfiguration checks from that asset.

Before ending updates for a version, the Trivy project announces the affected CLI versions, the end date for updates and the minimum CLI version users should upgrade to. A scan asset version change is not considered a breaking change to the Trivy CLI. Because users must upgrade to keep receiving current scan asset updates, it is announced separately from ordinary internal changes.

## Checked

2026-11-03. Read and confirmed against the Compatibility and Stability page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the claims about the three GitHub repository locations and a terminology page, which the page does not state.

Method: documentation only; no commands were run.
