---
id: computing-software.cloud-infrastructure-engineering.harbor.scan-individual-artifacts
name: scan-individual-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [vulnerability-scan, scan-status, export-cves, oci-image-index, harbor]
level: practitioner
status: docs-checked
description: "Scan single artifacts, read status and severity colours, understand OCI index aggregation, and export a project CVE CSV."
sources:
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/scan-individual-artifact/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A project admin or above can pick the project scanner on the project **Scanner** tab (**Edit**). If **Prevent vulnerable images from running** is set, blocking is decided by the project scanner, or the global default if none is set.

To scan: Projects, repository, select artifacts (or tick all), then **Scan Vulnerability**. Do not scan before the scanner database is populated. You can scan any time except while the status is Queued or Scanning. Statuses: Not Scanned, Unsupported, Queued, Scanning, Scan stopped, View log (task failed), Complete.

Severity colour: Red critical, Orange high, Yellow medium, Blue low, Green none found, Grey unknown. Hover the fixable count for a summary; click the digest for the full report, which has its own **Scan** button.

OCI image index: Harbor sends a scan request for each referenced artifact the scanner supports. If any is Scanning, the index shows Scanning, and the index summary is aggregated from the individual results.

Export CVEs (project admin, maintainer or developer; one project at a time): **Action**, **Export CVE(s)**, then filter by Repositories (comma list, `repo*`, or `**`), Tags, Labels or CVE IDs and click **Export**. The file is named `csv_file_yyyyMMddHHmmss.csv`, for example `csv_file_20220804123037.csv`. Download it from **Event Log**; Harbor deletes it once downloaded.

Scan all uses Interrogation Services, Vulnerability, **Scan Now**.

## Checked

2026-11-03. Scanner tab, statuses, severity colours, OCI image index behaviour and the CVE export steps and file name were read against the Harbor docs page Scan Individual Artifacts; the scan-all location against the Schedule Scans and Stop Scan pages. Nothing removed.

Method: documentation only; no commands were run.
