---
id: computing-software.cybersecurity-defensive.system-hardening.cis-cat-benchmark-assessment
name: cis-cat-benchmark-assessment
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [cis-cat, cis-benchmarks, compliance-scan, benchmark-assessment, system-hardening]
level: practitioner
status: draft
description: "Assess hosts against CIS Benchmarks with CIS-CAT Pro Assessor: choose the benchmark and profile, run in CLI, read and trend the reports."
sources: ["https://www.cisecurity.org/cis-cat-pro"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CIS-CAT assessment

**Goal:** a repeatable score and per-recommendation pass/fail for a host against its CIS Benchmark.

## Choose
- CIS-CAT Pro Assessor (CIS SecureSuite membership) ships with benchmark content as XCCDF/OVAL; a limited Lite edition exists for a few platforms. Check current entitlement.
- Match benchmark to OS and version exactly, then profile: Level 1 (practical baseline) or Level 2 (defence in depth, may break functions); Server vs Workstation; STIG profiles where offered.

## Run
GUI for single hosts; CLI for fleets (script `Assessor-CLI` for the platform; flags differ per version, use `--help`):
- pass the benchmark file and profile, an output directory, and the report formats (HTML, CSV, text, JSON/XML).
- Run as administrator/root, because many checks read protected config.
- Dashboard/Assessor service can aggregate results centrally.

## Interpret
- Each recommendation: pass, fail, error, not applicable, manual. Resolve `error` first (usually permissions or missing tool).
- Score is per benchmark profile; do not compare scores across profiles.
- Record accepted deviations as exceptions with owner and expiry; do not disable the check.

## Fleet workflow
1. Baseline-scan a golden image; fix the image, not each host.
2. Re-scan after patch cycles and image builds; keep CSVs and trend failures by recommendation.
3. Feed remediation into config management (Ansible Lockdown, GPO, Intune) and re-scan to confirm.

## Verify
Fixing a failed recommendation and re-scanning flips it to pass without new failures elsewhere.
