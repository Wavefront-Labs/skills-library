---
id: computing-software.systems-network-administration.patch-management.cis-benchmark-baselines
name: cis-benchmark-baselines
category: computing-software
field: systems-network-administration
product: patch-management
tags: [cis-benchmark, configuration-baseline, openscap, cis-cat, hardening, ansible-lockdown, config-baselines, openscap-oscap-xccdf, baseline-deviation]
level: practitioner
status: gated
description: "Adopt CIS Benchmarks as configuration baselines: Level 1 vs Level 2 profiles, assessment with CIS-CAT or OpenSCAP, automated remediation and documented deviations."
sources:
  - https://www.cisecurity.org/cis-benchmarks
  - https://www.open-scap.org/getting-started/
  - https://github.com/ansible-lockdown
  - https://github.com/ComplianceAsCode/content
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CIS benchmark baselines

**Goal:** every server type has a documented hardened baseline, applied automatically and measured continuously.

## Choose the profile
- **Level 1**: practical hardening with little functional impact; the default for most servers (gated: unconfirmed, source is paywalled or blocked).
- **Level 2**: defence in depth for high-security systems; more likely to break things (gated: unconfirmed, source is paywalled or blocked).
- Server vs workstation profiles differ; pick per role (the RHEL 9 SCAP Security Guide ships `cis_server_l1`, `cis_workstation_l1` and `cis_workstation_l2` profiles; Windows benchmark profile names are in each benchmark PDF).

## Assess
- CIS-CAT Pro Assessor assesses system conformance to CIS Benchmarks; licensing and output formats: check CIS SecureSuite terms (gated: unconfirmed, source is paywalled or blocked).
- OpenSCAP with SCAP Security Guide content for Linux:
```bash
dnf install openscap-scanner scap-security-guide
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis_server_l1 \
  --results results.xml --report report.html /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```

## Remediate
- Linux: `oscap xccdf generate fix --fix-type ansible --profile ... --output fix.yml results.xml`, or community roles (the ansible-lockdown GitHub organisation publishes RHEL9-CIS and UBUNTU22-CIS) with variables to toggle rules.
- Windows: CIS Build Kits (CIS describes them as a way to configure systems per a CIS Benchmark) or Microsoft security baselines plus CIS deltas via GPO/Intune.
- Apply at image build time and enforce at runtime (drift detection).

## Deviations
Some rules break applications (e.g. disabling services an app needs). Record each deviation: rule ID, systems, reason, compensating control, approver, review date. Implement deviations as variables in code, not manual reversals.

## Rollout
Pilot on representative systems with app owner testing, then by ring. Audit-mode first where available.

## Verify
Benchmark score per system type at or above target (your own target, for example 95% of applicable rules), with all failures matching approved deviations.

## Checked
Date: 2026-10-27. Documentation: ComplianceAsCode content repository (RHEL 9 profiles cis_server_l1, cis_workstation_l1, cis_workstation_l2 exist; datastream path pattern /usr/share/xml/scap/ssg/content/ssg-<product>-ds.xml), OpenSCAP oscap(8) manual (generate fix, --fix-type includes ansible), open-scap.org getting-started (openscap-scanner and scap-security-guide packages), ansible-lockdown RHEL9-CIS and UBUNTU22-CIS repositories exist, CIS Benchmarks page (CIS-CAT Pro Assessor and Build Kits exist). The CIS page does not define Level 1 and Level 2 or CIS-CAT licensing, so those two claims are gated.
Method: documentation only; no commands were run.
