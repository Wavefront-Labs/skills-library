---
id: computing-software.systems-network-administration.patch-management.rescan-to-verify-remediation
name: rescan-to-verify-remediation
category: computing-software
field: systems-network-administration
product: patch-management
tags: [remediation-verification, rescan, patch-verification, authenticated-scan, needs-restarting, backported-fix, vulnerability-scanner]
level: practitioner
status: draft
description: "Prove patches fixed vulnerabilities: authenticated and targeted rescans, version checks for backported fixes, and finding hosts still running old code until reboot."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://man7.org/linux/man-pages/man1/needs-restarting.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rescan to confirm remediation

**Goal:** close vulnerability tickets on evidence, not on "the patch job said success".

## Steps
1. **Confirm installation** on each host:
   - Windows: `Get-HotFix -Id KB5040442` or `Get-WindowsPackage -Online | Where-Object PackageName -like '*KB5040442*'`.
   - RHEL: `rpm -q openssl` compared with the fixed release in the RHSA; `dnf updateinfo info RHSA-2026:1234`.
   - Debian/Ubuntu: `dpkg -l openssl` vs the USN/DSA fixed version.
2. **Confirm it is running.** Updated libraries and kernels are not active until restart:
```bash
needs-restarting -r          # RHEL: reboot required?
needs-restarting -s          # services still using old libraries
needrestart -b               # Debian/Ubuntu batch mode
```
   Windows: pending-reboot check.
3. **Authenticated rescan.** Credentialed scans read package versions; unauthenticated ones guess from banners and miss backports. Run a targeted scan (single plugin family or specific plugin IDs) against just the patched hosts for fast evidence.
4. **Compare.** Finding closed on rescan: close ticket with scan ID. Still open: check for backport false positives (scanner comparing upstream version) and either fix scanner logic or record a false-positive deviation with proof.

## Gotchas
- Scanner credential failures silently downgrade to unauthenticated checks; monitor "credentialed checks: no" in results.
- Some fixes need a config change after the patch (e.g. registry key to enable a mitigation); the advisory says so.

## Verify
Tickets show a rescan ID dated after deployment, and the scanner's credential success rate for patched hosts is 100%.
