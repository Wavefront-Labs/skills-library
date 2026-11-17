---
id: computing-software.systems-network-administration.patch-management.monthly-patch-tuesday-review
name: monthly-patch-tuesday-review
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-tuesday-review, patch-tuesday, msrc, security-update-guide, patch-management, vulnerability-intelligence]
level: practitioner
status: docs-checked
description: "Run the monthly Patch Tuesday review: pull the MSRC release via API, triage exploited/critical CVEs and known issues, set ring dates and publish a one-page brief within 24 hours."
sources:
  - https://msrc.microsoft.com/update-guide
  - https://api.msrc.microsoft.com/cvrf/v3.0/swagger/v3/swagger.json
  - https://github.com/microsoft/MSRC-Microsoft-Security-Updates-API
  - https://learn.microsoft.com/en-us/windows/release-health/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monthly Patch Tuesday review

**When:** second Tuesday of each month (the October 2026 release is dated 13 October 2026 in the MSRC data). Aim to publish the internal brief by the next business morning.

## Pull the release data
```powershell
Install-Module -Name MsrcSecurityUpdates -Scope CurrentUser
$id = Get-Date -Format 'yyyy-MMM'            # e.g. 2026-Oct
$cvrf = Get-MsrcCvrfDocument -ID $id
$cvrf | Get-MsrcCvrfAffectedSoftware | Export-Csv affected.csv -NoTypeInformation
$cvrf.Vulnerability | ForEach-Object {
  [pscustomobject]@{
    CVE      = $_.CVE
    Title    = $_.Title.Value
    Exploited = ($_.Threats | Where-Object Type -eq 1 | Select-Object -Expand Description).Value -match 'Exploited:Yes'
    Severity = ($_.Threats | Where-Object Type -eq 3 | Select-Object -First 1).Description.Value
  } } | Export-Csv cves.csv -NoTypeInformation
```
Raw API: `GET https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-Oct` with `Accept: application/json` (XML is the default). Exploit status threats (Type 1) read like `Publicly Disclosed:No;Exploited:No;Latest Software Release:Exploitation Less Likely`; Type 3 is severity.

## Triage checklist
1. **Exploited = Yes or Publicly disclosed = Yes** -> candidate emergency track (check CISA KEV same day).
2. **Critical RCE in network-reachable services** (RDP, SMB, IIS/HTTP.sys, Exchange, SharePoint, DNS, LDAP) -> accelerate servers exposed to untrusted networks.
3. **Products you actually run**: filter `affected.csv` by your inventory; drop the rest.
4. **Known issues**: read Windows release health and each KB's "Known issues" section; note Known Issue Rollbacks and any manual steps (registry keys, hardening enforcement phases).
5. **SSU / prerequisites**, out-of-band follow-ups from last month, and anything superseded.
6. Third-party same-day releases (Adobe, SAP, Chrome/Edge) go in the same brief.

## Brief template
| Item | Content |
|---|---|
| Headline | N CVEs, X exploited, Y critical; recommended track |
| Must-act | CVE, product, exposure in our estate, deadline |
| Known issues | KB, symptom, workaround, affected rings |
| Schedule | Pilot date, broad date, servers window, deadline |
| Enforcement changes | Hardening phases that start this month |

## Gotchas
- Severity "Important" EoP bugs exploited in the wild often matter more than "Critical" ones nobody uses.
- Enforcement-phase changes break things months after you first patched; track the phase calendar.
- Re-check release health on day 3-5; issues surface after broad deployment elsewhere.

## Verify
Brief published with owner sign-off, ring dates set in the patch tool, and exploited CVEs tracked to closure in the next compliance report.

## Checked
Date: 2026-10-27. Documentation: live MSRC CVRF v3.0 data for 2026-Oct (document title "October 2026 Security Updates", Threat types 0, 1 and 3, exploit-status string format), MSRC swagger path `/cvrf/{id}`, microsoft/MSRC-Microsoft-Security-Updates-API repository (module install line; cmdlets Get-MsrcCvrfDocument and Get-MsrcCvrfAffectedSoftware exist). Removed the unconfirmed release time and the named hardening examples.
Method: documentation only; no commands were run.
