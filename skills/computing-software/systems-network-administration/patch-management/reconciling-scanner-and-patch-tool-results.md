---
id: computing-software.systems-network-administration.patch-management.reconciling-scanner-and-patch-tool-results
name: reconciling-scanner-and-patch-tool-results
category: computing-software
field: systems-network-administration
product: patch-management
tags: [scan-discrepancy, scanner-reconciliation, patch-verification, vulnerability-scanning, patch-management]
level: practitioner
status: draft
description: "Reconcile vulnerability scanner findings with patch tool compliance when they disagree: common causes (supersedence, reboot, detection logic, scope), triage steps and fixes."
sources:
  - https://docs.tenable.com/nessus/Content/CredentialedChecksOnWindows.htm
  - https://learn.microsoft.com/en-us/windows/deployment/update/how-windows-update-works
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reconciling scanner vs patch tool results

"WSUS says 99% compliant, Nessus says 4,000 missing patches." Both are often right about different things.

## Common causes
| Cause | Symptom | Fix |
|---|---|---|
| Pending reboot | Patch tool: Installed; scanner reads file versions still old | Reboot; report pending-reboot separately |
| Update not approved/targeted | Patch tool scope excludes the KB or product | Approve, or add product/classification |
| Detection logic differs | Scanner checks file version or registry; tool uses applicability rules | Check plugin output for the exact file/version it read |
| Superseded vs cumulative | Scanner flags old KB though newer cumulative installed | Usually scanner bug or partial install; check plugin output |
| Manual fix steps | CVE needs registry key or config after patch (e.g. enabling mitigation) | Apply the step; tools never do it |
| Third-party software | Patch tool only manages OS | Bring apps into a third-party catalog |
| Uncredentialed scan | Banner-based guessing | Fix credentials; uncredentialed results are low confidence |
| Asset scope mismatch | Machines missing from patch tool entirely | Client health and discovery reconciliation |
| Backports (Linux) | Scanner compares upstream versions | Use distro OVAL-based checks |

## Triage process
1. Pick the top 10 plugins/QIDs by count of disagreement.
2. For each, open the plugin output on one host: path, found version, fixed version.
3. On the host, verify: `Get-HotFix`, `Get-WindowsPackage -Online`, file version (`(Get-Item $env:windir\System32\ntoskrnl.exe).VersionInfo`), `rpm -q`.
4. Classify as one of the causes above; fix at the cause, not host by host.
5. Record known scanner issues with vendor ticket numbers.

## Gotchas
- Scanner credential failures show as fewer findings, not errors; watch "credentialed checks: no" in scan info.
- Different scan times: scanner ran before the window ended.

## Verify
Disagreement count per cause tracked monthly and shrinking; executive reporting uses one agreed source with the other as a check.
