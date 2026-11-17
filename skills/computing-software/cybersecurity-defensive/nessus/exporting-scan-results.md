---
id: computing-software.cybersecurity-defensive.nessus.exporting-scan-results
name: exporting-scan-results
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-reporting, nessus-export, nessus-file-format, csv-export, report-templates, vulnerability-data, siem-integration]
level: practitioner
status: docs-checked
description: "Export Nessus results as .nessus XML, CSV, HTML or PDF, choose the right format for each consumer and parse .nessus reliably."
sources: ["https://docs.tenable.com/nessus/Content/ScanReportFormats.htm", "https://docs.tenable.com/nessus/Content/ExportAScan.htm", "https://docs.tenable.com/nessus/Content/CreateAScanReport.htm", "https://docs.tenable.com/nessus/Content/PluginRules.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting scan results

**Goal:** get scan results to each consumer (remediation teams, auditors, scripts) in a format that keeps the fields they need.

## Exports and reports (Nessus 10.12 user guide)
| Format | Kind | What Tenable says |
|---|---|---|
| Nessus | Export | A `.nessus` XML file with targets, user-defined policies and scan results. Password credentials are stripped, so re-apply passwords if you import it as a policy. |
| Nessus DB | Export | Proprietary encrypted database with everything in the scan, including audit trails; you set a password on export and need it on import. |
| Policy | Export | Informational JSON file with the scan policy details. |
| Timing Data | Export | Informational CSV: hostname, IP, FQDN, scan start and end times, duration in seconds. |
| PDF | Report | Generation may take several minutes for a large report; needs Oracle Java or OpenJDK (custom path via `nessuscli fix --set path_to_java=<path>`). |
| HTML | Report | Standard HTML; opens in a new browser tab. |
| CSV | Report | You choose the columns; suited to databases and spreadsheets. |

Nessus Essentials cannot create exports or reports; Essentials Plus can create PDF and HTML reports.

UI: open the scan, then **Export** (Nessus, Nessus DB, Policy, Timing Data) or **Report** (PDF, HTML, CSV). PDF and HTML reports use report templates (system templates plus your own); a CSV report lets you pick columns and save them as the default.

## Gotchas
- A report includes the results currently visible on the results page, so search terms and filters narrow it; you can also tick specific hosts or vulnerabilities (in one tab, not both). Clear filters before reporting if you want everything.
- A `.nessus` export does not reflect changes made with plugin rules or by hiding or re-rating a vulnerability: it keeps the original severities. Reports follow what you see on screen, so the two can disagree.
- For vulnerability and remediation analysis Tenable points to Create a Scan Report rather than the export.

## Verify
- [ ] Report row counts match the scan results page for the same filter.
- [ ] Anything that must carry original severities is built from the `.nessus` export, and consumers know plugin-rule changes are absent there.

## Checked
2026-11-02. Confirmed from the Tenable Nessus 10.12 pages "Scan Exports and Reports", "Export a Scan", "Create a Scan Report" and "Plugin Rules", and the `path_to_java` setting on the Nessus CLI page. Removed (not stated on those pages): API export endpoints, `.nessus` XML element and attribute walk-through with Python parser, Excel cell-length limit, "Complete List of Vulnerabilities by Host" template name, percentage of info-severity rows.

Method: documentation only; no commands were run.
