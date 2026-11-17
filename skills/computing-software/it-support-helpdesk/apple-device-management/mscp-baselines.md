---
id: computing-software.it-support-helpdesk.apple-device-management.mscp-baselines
name: mscp-baselines
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, security-baselines, mscp-baselines, mscp, nist-800-53]
level: practitioner
status: docs-checked
description: "Generate baseline profiles, scripts and compliance checks from mSCP rules for CIS, NIST 800-53 or CMMC."
sources:
  - "https://github.com/usnistgov/macos_security"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mscp-baselines

Goal: consistent hardening of Apple devices from the macOS Security Compliance Project (mSCP, NIST with NASA, DISA and LANL).
It supports macOS, iOS/iPadOS and visionOS, and derives rules from NIST SP 800-53 Rev. 5.

Frameworks supported include NIST SP 800-53, NIST SP 800-171 r2 (CMMC) and r3, CIS Benchmarks (Level 1 and 2), CIS Controls
v8, CNSSI 1253, DISA STIG, BSI Indigo, NLMAPGOV and HICP.

## Steps
1. Clone `macos_security` and follow its `install.md`; the `./mscp.py` CLI is the entry point, and the `scripts/` wrappers
   (`generate_baseline.py`, `generate_guidance.py`) call the same CLI.
2. Build a baseline YAML: `generate_baseline.py -k <keyword>` collects rules for a keyword/tag (`-l` lists keywords,
   `-t` tailors a custom baseline interactively, `-m` migrates a pre-2.0 baseline).
3. Generate output: `generate_guidance.py -s -p <baseline>.yaml` writes the compliance script (`-s`) and configuration
   profiles (`-p`). Other options: `-x` Excel file, `-d` declarative device management artifacts, `-A` everything,
   `--no-docs` to skip the documents, `--consolidated-profile` or `--granular-profiles` to shape the profiles, and `-H`
   to sign profiles on macOS.
4. Deploy the profiles through your MDM and run the compliance script; the script verifies and enforces rules that
   profiles cannot.
5. Review exemptions with the control owners.

## Practice
- A custom directory (`custom/` in the repo, selectable by option) holds your own rules; keep customisations there and
  rebuild after each project update so changes are reviewed.
- Treat the generated script as evidence and keep remediation in MDM.
- Record the project release and the baseline name used so a later audit reproduces the exact rule set.

## Gotchas
Some rules reduce usability (for example a short screen lock); pilot on a test group first.

## Checked

2026-11-09: confirmed on the project's GitHub page (purpose, supported platforms, outputs, frameworks, NIST SP 800-53
Rev. 5 basis) and in the repository's `src/mscp/cli.py` and `scripts/` wrappers read from raw GitHub (baseline flags
`-k -l -t -m`; guidance flags `-s -p -x -d -A -H --no-docs --consolidated-profile --granular-profiles`; baseline YAML
positional argument). Removed: the unreadable CIS Benchmark page, the "audit mode" step, the spreadsheet output wording
and the separate exemptions YAML file claim.

Method: documentation only; no commands were run.

## Verify
The compliance script's score improves after deployment and exceptions are documented.
