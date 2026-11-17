---
id: computing-software.it-support-helpdesk.device-provisioning.security-baseline-for-the-standard-build
name: security-baseline-for-the-standard-build
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, standard-build, security-baseline, cis-benchmarks, intune-security-baselines, microsoft-security-baseline, policy-analyzer, lgpo, hardening]
level: practitioner
status: draft
description: "Define the standard build's security baseline: Intune or Microsoft security baselines vs CIS Benchmarks, exceptions, testing in a pilot ring, and detecting drift."
sources:
  - "https://learn.microsoft.com/en-us/intune/intune-service/protect/security-baselines"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines"
  - "https://www.cisecurity.org/cis-benchmarks"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# security-baseline-for-the-standard-build

Goal: every new device lands with the same, documented hardening, and the
exceptions are deliberate and recorded.

## Pick a source baseline
- **Intune security baselines** (Windows, Defender for Endpoint, Edge,
  Microsoft 365 Apps): Microsoft-recommended settings deployable as a
  profile; versioned, with "compare" between versions.
- **Microsoft Security Compliance Toolkit** baselines for GPO estates
  (import with LGPO / GPO backups; compare with Policy Analyzer).
- **CIS Benchmarks** (Level 1 = practical, Level 2 = high security) — often
  required by auditors/cyber insurance; CIS publishes Intune and GPO builds
  for members.
Choose one as the master; layer org-specific settings on top. Don't apply
two overlapping baselines — conflicts are hard to untangle.

## Build it
1. Start with the baseline in **audit/report** where possible; deploy to a
   pilot ring (IT + volunteers from each department).
2. Collect breakage: legacy auth, old printers (SMB signing, NTLM), USB
   restrictions, PowerShell constrained language, ASR rules blocking
   macros.
3. Record each **exception**: setting, reason, owner, review date. Prefer
   scoped exceptions (one group) over weakening the whole baseline.
4. Promote to broad deployment by ring.

## Typical baseline content (Windows)
BitLocker with TPM, Secure Boot, Credential Guard/VBS, Defender AV + ASR
rules + tamper protection, firewall on all profiles, LAPS, SMB signing,
LSA protection, disabled legacy protocols (SMB1, LLMNR, NetBIOS where
possible), screen lock timeout, Windows Hello for Business, audit policy,
no local admin for users.

## Drift
- Intune: baseline profile → per-setting status (Conflict, Error,
  Not applicable).
- Defender Vulnerability Management "Security baselines assessment"
  compares devices to CIS/STIG.
- GPO estates: periodic `gpresult /h` and Policy Analyzer against the
  baseline.

## Gotchas
- Baseline version upgrades change defaults — review the diff before
  switching.
- Settings applied both by GPO and MDM on hybrid devices: MDM wins only if
  "MDMWinsOverGP" is set; otherwise you get conflicts.

## Verify
A freshly built pilot device reports 100 % "Succeeded" on the baseline
profile (or listed exceptions only), and the exception register is current.
