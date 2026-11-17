---
id: computing-software.cybersecurity-defensive.system-hardening.stig-viewer-checklists
name: stig-viewer-checklists
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [stig-checklist, stig-viewer, disa-stig, ckl, cklb, scap-compliance-checker, evaluate-stig]
level: practitioner
status: draft
description: "Produce DISA STIG checklists: load STIGs in STIG Viewer 3, create CKLB files per asset, import SCAP results, finish manual checks, and report status and POA&M items."
sources: ["https://public.cyber.mil/stigs/srg-stig-tools/", "https://public.cyber.mil/stigs/scap/", "https://public.cyber.mil/stigs/downloads/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STIG Viewer checklists

DoD and many government-adjacent environments must show STIG compliance per asset in **checklist** files.
STIG Viewer (version 2.x uses `.ckl` XML; version 3 uses `.cklb` JSON and can import `.ckl`) is the standard
tool.

## Workflow
1. **Download** current STIG/SRG zips (quarterly release cycle) from the DoD Cyber Exchange; import the XCCDF
   into STIG Viewer.
2. **Create a checklist** per asset (or per asset + application/database STIG): fill target data (hostname,
   IP, MAC, FQDN, role, technology area).
3. **Automate what you can**:
   - SCAP Compliance Checker (SCC) runs SCAP benchmarks and outputs XCCDF results, imported into the
     checklist ("Import XCCDF results").
   - Evaluate-STIG (PowerShell, available to DoD) or vendor tools (Ansible Lockdown, PowerSTIG) can produce
     checklists with many manual checks answered.
4. **Manual checks**: SCAP covers only a portion of rules; for the rest, follow each rule's Check Text, record
   evidence in Finding Details and Comments.
5. **Status per rule**: Open, Not a Finding, Not Applicable, Not Reviewed. Severity override needs
   justification (e.g. mitigations lowering CAT I to CAT II).
6. **Export**: CKL/CKLB per asset; aggregate in eMASS or a dashboard; open findings go into the POA&M with
   milestones.

## Categories
- CAT I: high (direct loss of confidentiality, availability or integrity) - fix immediately.
- CAT II: medium. CAT III: low.

## Tips
- Keep checklists in version control or a central repository with naming `host_STIG-name_Vversion-Rrelease`.
- When a new STIG release arrives, use STIG Viewer's checklist upgrade so answers carry over by rule ID;
  re-review rules whose content changed.
- Many manual answers are identical across an image; generate from a golden image's evidence and override per
  host only where needed.

## Gotchas
- "Not a Finding" without evidence fails assessments; Finding Details must show the command and output.
- Not Applicable must cite why (e.g. role not installed).
- Benchmark versions in SCC must match the STIG release in the checklist.

## Verify
Every asset has a current-release checklist, no rules remain Not Reviewed, every Open CAT I has a POA&M entry
with a date.
