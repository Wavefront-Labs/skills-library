---
id: computing-software.systems-network-administration.patch-management.disa-stig-baselines
name: disa-stig-baselines
category: computing-software
field: systems-network-administration
product: patch-management
tags: [stig, configuration-baseline, scap, stig-viewer, openscap, compliance]
level: practitioner
status: gated
description: "Apply and assess DISA STIGs: finding the right STIG, CAT I/II/III severities, SCAP benchmark scans, STIG Viewer checklists, automation content and documenting deviations."
sources:
  - https://www.cyber.mil/stigs/
  - https://www.open-scap.org/
  - https://github.com/ComplianceAsCode/content
  - https://github.com/microsoft/PowerStig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DISA STIG baselines

Security Technical Implementation Guides are the US DoD configuration baselines; widely
used outside DoD as a strict hardening reference.

## Pieces
- **STIG** (XCCDF) per product/version (e.g. RHEL 9 STIG, Windows Server 2022 STIG,
  VMware vSphere 8 STIG), released on DISA's schedule (quarterly cadence (gated: unconfirmed, source is paywalled or blocked)).
- **SCAP benchmark** for automated checks of a subset (OS mostly); remaining rules are manual.
- **STIG Viewer** to create checklists and record status per rule (checklist file formats and status names (gated: unconfirmed, source is paywalled or blocked)).
- Severities: **CAT I** (high, fix immediately), CAT II (medium), CAT III (low) (gated: unconfirmed, source is paywalled or blocked).

## Assess
```sh
# RHEL with SCAP Security Guide (contains a STIG profile)
dnf install openscap-scanner scap-security-guide
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_stig \
  --results stig-results.xml --report stig-report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```
Windows: DISA's SCAP Compliance Checker (SCC) with the Windows benchmarks (gated: unconfirmed, source is paywalled or blocked); import results into
STIG Viewer to prefill the checklist.

## Remediate
- RHEL: `oscap xccdf generate fix --profile ..._stig --fix-type ansible` or the
  `ansible-lockdown` RHEL9-STIG role (the repository exists); at install time, the Anaconda security profile.
- Windows: DISA GPO packages (import into GPMC) or PowerSTIG (the microsoft/PowerSTIG repository, DSC based).
- Apply in a test environment first: STIGs break things (FIPS mode, banner requirements,
  SSH ciphers, auditd load, disabled services).

## Deviations
Rules you can't meet: document in the checklist with justification, compensating control
and risk acceptance (ties to exceptions process). Mark Not Applicable only when the
feature truly isn't present.

## Gotchas
- STIG versions are updated periodically; pin a release per baseline version and plan updates.
- Automated scan "pass" ≠ STIG compliant: manual rules remain.
- CIS and STIG overlap but differ; choose one primary per platform.

## Verify
Checklist per system with zero Open CAT I, documented CAT II/III deviations; scan score
trend after each STIG release.

## Checked
Date: 2026-10-27. Documentation: ComplianceAsCode content repository (RHEL 9 `stig` profile exists), OpenSCAP oscap(8) manual (generate fix, --fix-type ansible), ansible-lockdown RHEL9-STIG and microsoft/PowerSTIG repositories exist. The DISA STIG site (public.cyber.mil, redirected to cyber.mil) is script-rendered and could not be read, so the cadence, checklist formats, severity labels and SCC claims are gated.
Method: documentation only; no commands were run.
