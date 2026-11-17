---
id: computing-software.cybersecurity-defensive.nessus.compliance-audit-files
name: compliance-audit-files
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, compliance-audit-files, audit-files, cis-benchmark, configuration-audit, policy-compliance]
level: practitioner
status: draft
description: "Run Nessus configuration compliance audits with .audit files: choosing CIS/DISA audits, credential needs, customising checks and reading compliance results."
sources: ["https://docs.tenable.com/nessus/Content/ComplianceChecks.htm", "https://www.tenable.com/audits", "https://docs.tenable.com/nessus/compliance-checks-reference/Content/Welcome.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compliance audits with .audit files

**Goal:** measure hosts against a hardening baseline (CIS Benchmarks, DISA STIG, vendor
guides) with the same scanner you use for vulnerabilities.

## Setup
1. New Scan > **Policy Compliance Auditing** (or add Compliance to an Advanced scan;
   Nessus Professional/Manager or Tenable platform licences).
2. Compliance tab: pick audits by platform, e.g. *CIS Microsoft Windows Server 2022
   Benchmark L1 Member Server*, *CIS Ubuntu Linux 22.04 L1 Server*, *DISA STIG Windows 11*.
   Download others from tenable.com/audits and upload.
3. Credentials are mandatory: Windows (SMB, admin), SSH (root or sudo), database
   credentials for DB audits, API/SSH for network devices.
4. Plugins: only the compliance plugin families are needed for a pure compliance scan,
   which keeps it fast.

## Customising an audit
Audit files are XML-like text with checks:
```
<custom_item>
  type        : PASSWORD_POLICY
  description : "1.1.1 Ensure 'Enforce password history' is set to '24 or more password(s)'"
  value_type  : POLICY_DWORD
  value_data  : [24..MAX]
  password_policy : ENFORCE_PASSWORD_HISTORY
</custom_item>
```
- Change `value_data` to match your approved deviation rather than accepting permanent
  failures; keep a changelog and the original reference.
- Many CIS audits expose variables (Compliance tab > audit > variables) such as allowed
  admin group names; set these instead of editing the file.

## Reading results
Each check returns PASSED, FAILED or WARNING (manual check or could not determine) with
actual vs expected values. Report pass rate per benchmark section and per host group.
Track exceptions (approved deviations) separately so the pass rate reflects real drift.

## Gotchas
- Level 2 and domain-controller profiles differ; using a member-server audit on a DC yields
  false failures.
- Audit content updates with plugin feeds; a new benchmark version changes scores.
- WARNING results often mean insufficient privilege; fix credentials before arguing about
  findings.

## Verify
Change one setting on a test host to a non-compliant value, rescan, and confirm that single
check flips to FAILED with the actual value shown.
