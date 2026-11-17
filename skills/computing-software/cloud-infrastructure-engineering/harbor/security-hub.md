---
id: computing-software.cloud-infrastructure-engineering.harbor.security-hub
name: security-hub
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [security-hub, cve-search, vulnerability-overview, interrogation-services, harbor]
level: practitioner
status: docs-checked
description: "Use the Harbor Security Hub for a registry-wide vulnerability view, top dangerous artifacts and CVEs, and the exact-match search fields."
sources:
  - https://goharbor.io/docs/main/administration/security-hub/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Security Hub gives administrators a registry-wide view of vulnerabilities, unlike the per-artifact vulnerability view. Open it as an admin through Administration, **Interrogation Service**, Security Hub tab, or directly at `https://<harbor-domain>/harbor/interrogation-services/security-hub`.

The page title shows total artifacts and scanned artifacts. Cards:
- **Total Vulnerabilities**: all vulnerabilities in scanned images, split by severity.
- **Top 5 Most Dangerous Artifacts**: ranked by number of vulnerabilities and severity. Click one to query all vulnerabilities in it.
- **Top 5 Most Dangerous CVEs**: ranked by number of affected artifacts and severity. Click one to list where it appears.

Search Vulnerabilities fields, all exact match except CVSS3:
- CVE ID: required in the query for performance reasons
- Severity
- CVSS3: a score range
- Project Name
- Digest
- Repository Name
- Package
- Tag

Note: the CVE ID condition is required to query vulnerability information (for performance), so start a search from a CVE ID, then add the other conditions.

The cards count vulnerabilities found in scanned artifacts.

## Checked

2026-11-03. Access paths, the page title, the three cards and the search field table were read against the Harbor docs page Security Hub. Removed: the advice to run scans first or the cards under-report (the page says only that the cards cover scanned artifacts).

Method: documentation only; no commands were run.
