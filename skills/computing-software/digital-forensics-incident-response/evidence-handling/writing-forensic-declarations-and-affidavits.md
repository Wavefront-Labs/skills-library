---
id: computing-software.digital-forensics-incident-response.evidence-handling.writing-forensic-declarations-and-affidavits
name: writing-forensic-declarations-and-affidavits
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [affidavit, declaration, expert-witness, forensic-reporting, dfir]
level: advanced
status: draft
description: "Write a forensic examiner's declaration or affidavit with counsel: structure, qualifications, facts versus opinions, precise language, exhibits and the duty of candour."
sources: ["https://www.law.cornell.edu/uscode/text/28/1746", "https://www.law.cornell.edu/rules/frcp/rule_26", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing forensic declarations and affidavits

Declarations and affidavits put your findings under oath, often for preliminary injunctions (e.g. trade-secret theft), preservation orders or search warrants. An **affidavit** is sworn before a notary or officer; in US federal practice a **declaration** under 28 U.S.C. 1746 ("I declare under penalty of perjury...") has the same effect without a notary. Counsel drafts the legal framing; the facts and opinions must be yours.

## Structure
1. Identity and engagement: who you are, who retained you, compensation if expert.
2. Qualifications: training, certifications, experience relevant to the specific analysis (attach a CV).
3. Materials examined: each evidence item with identifiers and hashes, and what you did not have.
4. Methodology: tools and versions, steps, validation; enough to be reproduced.
5. Findings: numbered paragraphs, one fact per paragraph, each tied to an exhibit.
6. Opinions (if acting as expert): clearly separated from facts, with the basis for each.
7. Reservation to supplement if new evidence arrives.
8. Attestation, date, place, signature.

## Language
- Precise and qualified: "The USB device with serial X was first connected at 14:02 UTC on 3 May 2026 according to the SYSTEM hive", not "the employee copied files to a USB".
- Separate what the artefact shows from inference about a person's actions; if you infer, say "consistent with" and explain alternatives considered.
- Avoid adjectives and advocacy ("clearly malicious", "massive theft").

## Process
- Review every draft line by line; counsel may propose wording, but you must be able to defend each sentence in cross-examination. Refuse statements you cannot support.
- Keep drafts and notes as your jurisdiction's disclosure rules require (FRCP 26 protects some draft communications for testifying experts; other jurisdictions differ, e.g. CPR Part 35 duty to the court in England and Wales).
- Confirm exhibits attached are exactly the ones referenced.

## Gotchas
- Declarations filed early in a case get compared to your later report and testimony; inconsistencies are exploited.
- Do not overstate certainty to support an urgent motion.

## Verify
Each factual paragraph cites an exhibit or evidence item, each opinion states its basis, and you could reproduce every finding from your notes.
