---
id: computing-software.cybersecurity-defensive.nessus.tenable-findings-to-siem
name: tenable-findings-to-siem
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-reporting, tenable-siem-integration, splunk-add-on-for-tenable, sentinel-tenable-connector, vulnerability-data, alert-enrichment]
level: practitioner
status: draft
description: "Send Tenable vulnerability findings to a SIEM (Splunk add-on, Sentinel connector, API exports) and use them to enrich alerts and prioritise detections on vulnerable hosts."
sources: ["https://docs.tenable.com/integrations/Splunk/Content/Welcome.htm", "https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/tenable-vulnerability-management", "https://docs.tenable.com/vulnerability-management/Content/Platform/API/ExportAPI.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tenable findings into the SIEM

Vulnerability data in the SIEM answers "is the host in this alert actually exploitable?" and lets
detections weight exploit attempts against hosts that have the matching CVE.

## Splunk
- **Tenable Add-on for Splunk** (Splunkbase 4060) plus the Tenable App. Inputs for Tenable VM
  (cloud), Tenable Security Center, and Nessus (via SC). Sourcetypes `tenable:io:vuln`,
  `tenable:io:assets`, `tenable:sc:vuln`.
- Configure on a heavy forwarder or IDM (Splunk Cloud): API access/secret keys of a dedicated
  read-only Tenable user, start date, lowest severity to collect (Medium+ keeps volume sane),
  interval (daily is usually enough).
- CIM: maps to the Vulnerabilities data model, so ES asset risk and dashboards can use it.

## Microsoft Sentinel
- **Tenable Vulnerability Management** connector (Content hub solution, Azure Function or
  codeless connector) writing to custom tables (`Tenable_VM_Vuln_CL`, `Tenable_VM_Asset_CL`).
- Needs API keys in Key Vault/app settings; watch function failures in Application Insights.

## Any SIEM: export API
```python
from tenable.io import TenableIO
tio = TenableIO(access_key, secret_key)
for v in tio.exports.vulns(severity=['high','critical'], state=['open','reopened'], since=last_run):
    send_to_siem(v)   # one JSON per asset-plugin finding
```
`state` and `since` (last_found) keep incremental pulls small.

## Using it
Enrich alerts:
```
index=ids signature_cve=*
| lookup tenable_open_vulns_by_ip ip AS dest_ip OUTPUT plugin_id cve severity
| where like(cve, "%".signature_cve."%")
```
(A scheduled search builds the lookup daily from the vuln index.)
- Raise urgency/risk when an exploit attempt targets a host with that open CVE.
- Dashboards: hosts with KEV CVEs that also show suspicious activity.

## Gotchas
- Full-state dumps every run multiply volume; pull only changes and keep a current-state lookup.
- Asset identity mismatch (IP vs hostname vs agent UUID) breaks joins; normalise on what the
  SIEM's asset framework uses.
- API keys tie to a user; if the user is disabled the input silently stops: monitor the
  last-event time per sourcetype.

## Verify
Pick a host with a known open critical finding and confirm it appears in the SIEM with matching
plugin ID, state and last_found within one collection interval.
