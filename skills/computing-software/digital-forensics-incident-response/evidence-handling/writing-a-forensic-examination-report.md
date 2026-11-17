---
id: computing-software.digital-forensics-incident-response.evidence-handling.writing-a-forensic-examination-report
name: writing-a-forensic-examination-report
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [forensic-report-writing, forensic-report, expert-report, documentation, swgde, dfir]
level: practitioner
status: draft
description: "Write a forensic examination report: structure, evidence description, methods, findings with artefact citations, opinions with basis, limitations and reproducibility."
sources: ["https://www.swgde.org/documents/published-complete-listing/", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a forensic examination report

**Goal:** a report another examiner could reproduce and a court or tribunal could rely on.
Unlike the incident report (business focus), this documents the examination of specific
evidence (SWGDE Requirements for Report Writing in Digital and Multimedia Forensics).

## Structure
1. Title, case number, examiner, organisation, report date, version.
2. **Request and scope**: who asked, questions to answer, authority (warrant, consent,
   policy), limits.
3. **Evidence examined**: ID, description, serials, hashes, acquisition details, chain of
   custody reference.
4. **Methods and tools**: procedures, tool names and versions, validation status.
5. **Findings**: factual, each tied to artefact path/record and evidence ID; tables and
   screenshots with captions; timestamps in UTC (and local where relevant).
6. **Analysis / opinions**: interpretation, with basis and confidence; alternative
   explanations considered and why rejected.
7. **Limitations**: unexamined areas, encryption, data not available, tool limits.
8. **Conclusion** answering each question from the scope.
9. Appendices: detailed listings, hash lists, glossary.
10. Signature and declaration (where required by jurisdiction, e.g. expert's statement of
    truth under UK CPR Part 35 or FRCP 26 requirements in the US).

## Writing rules
- Distinguish **fact** ("The LNK file records target path \Q3\pricing.xlsx") from
  **inference** ("This indicates the file was opened from a removable drive").
- Never say "the user did X" when the evidence shows "the account did X"; attribution to a
  person needs more evidence.
- Define technical terms on first use; keep a glossary.
- Report exculpatory findings as diligently as inculpatory ones.

## Verify
A peer reproduces two key findings from the report alone using the evidence and stated
tools, and every opinion has a stated basis.
