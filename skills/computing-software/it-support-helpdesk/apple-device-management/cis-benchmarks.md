---
id: computing-software.it-support-helpdesk.apple-device-management.cis-benchmarks
name: cis-benchmarks
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, security-baselines, cis-benchmarks, cis-benchmark, hardening]
level: practitioner
status: docs-checked
description: "Apply CIS macOS benchmarks via MDM profiles and remediation scripts and track score drift."
sources:
  - "https://github.com/usnistgov/macos_security"
  - "https://www.cisecurity.org/benchmark/apple_os"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cis-benchmarks

Goal: apply a recognised, community-consensus baseline to Macs.

- Get the CIS Apple macOS Benchmark for your macOS version from the CIS benchmark page. Versions are per OS release (for
  example separate benchmarks for macOS 26 Tahoe, 15 Sequoia and 14 Sonoma) and there are also Cloud-tailored versions
  for some releases. The PDFs are free for non-commercial use.
- CIS-CAT Pro (the scanner) and CIS Build Kits are for CIS SecureSuite members only. The mSCP project
  (`usnistgov/macos_security`) is an open-source alternative that builds profiles and compliance scripts for CIS
  Benchmarks Level 1 and Level 2 (see the mscp-baselines skill).
- Use Level 1 as the general starting point and Level 2 where the risk justifies the extra restrictions.
- Prefer configuration-profile controls over scripts; use scripts only for settings profiles cannot express.
- Map each recommendation to a profile or script with an owner, accept documented exceptions with a justification and
  review date, and version-control that mapping so audits can see why settings differ from the benchmark.
- Review the mapping after each OS release, since benchmarks are published per OS version, and compare benchmark
  versions to explain score changes.

## Checked

2026-11-09: confirmed on the CIS Apple macOS Benchmarks page (free non-commercial PDFs, per-OS versions and
Cloud-tailored variants, CIS-CAT Pro and Build Kits are SecureSuite-member only) and the mSCP GitHub page (CIS
Benchmarks Level 1 and 2 supported). Removed: the claim that CIS-CAT can be used to track score without membership, and
the remark that benchmarks lag OS versions beyond what the page shows (the page lists a benchmark for the newest OS).

Method: documentation only; no commands were run.

## Verify
A score is recorded per OS release and deviations are approved by the control owner.
