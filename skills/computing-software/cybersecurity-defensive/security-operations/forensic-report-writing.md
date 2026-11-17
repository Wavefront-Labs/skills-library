---
id: computing-software.cybersecurity-defensive.security-operations.forensic-report-writing
name: forensic-report-writing
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [forensic-report, digital-forensics, report-writing, expert-witness, chain-of-custody, dfir]
level: advanced
status: draft
description: "Write a digital forensic report: scope and questions, evidence and methods, findings tied to artefacts, limitations, opinion vs fact, and reproducibility for legal review."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.swgde.org/documents/published-complete-listing", "https://www.iso.org/standard/44381.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Forensic report writing

A forensic report must let another examiner reproduce every finding and let a non-technical
reader understand what is proven and what is not.

## Structure
1. **Summary**: questions asked and short answers, with confidence.
2. **Scope and authority**: who requested, legal basis, what was in/out of scope, dates.
3. **Evidence**: item list with identifiers, acquisition method, hashes (acquisition and
   verification), custody references.
4. **Tools and methods**: tool names and versions, procedures (e.g. "Parsed $MFT with MFTECmd
   1.2.2.1"), validation of tools where relevant.
5. **Findings**: one finding per section: statement, supporting artefacts (path, record number,
   timestamp with time zone), screenshot or excerpt, interpretation.
6. **Timeline**: consolidated, UTC, citing artefact per entry.
7. **Limitations**: missing logs, encrypted data, anti-forensics, time skew, things not examined.
8. **Conclusions**: answer each question; distinguish fact ("file X was created at T") from
   inference ("consistent with the user executing X").
9. **Appendices**: hash lists, full artefact exports, glossary.

## Language
- Precise and neutral: "The artefacts indicate", "consistent with", "no evidence was found of"
  (not "did not happen").
- Avoid jargon in summary; define it in the glossary.
- No speculation about intent unless asked and supported.

## Quality
- Peer review by a second examiner against the evidence.
- Timestamps: state source (MFT $SI vs $FN, event log TimeCreated) and time zone handling.
- Version-control drafts; final PDF signed and hashed.

## Gotchas
- Mixing incident response notes with forensic conclusions confuses readers; keep IR actions in a
  separate section with timestamps (they also alter evidence).
- Over-claiming one artefact (e.g. Prefetch implies execution, not who executed).

## Verify
A peer examiner can locate each cited artefact from the report alone and reaches the same finding.
