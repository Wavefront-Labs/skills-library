---
id: social-sciences.social-research-methods.qualitative-software.qda-project-setup-coding-queries-and-team-coding
name: qda-project-setup-coding-queries-and-team-coding
category: social-sciences
field: social-research-methods
product: qualitative-software
tags: [qualitative-software, qdas, caqdas, nvivo, atlas-ti, maxqda, dedoose, taguette, qda-miner, coding, codes, nodes, code-system, cases, attributes, classifications, document-variables, matrix-coding-query, code-relations, code-co-occurrence, memos, team-coding, project-merge, inter-coder-agreement, refi-qda, qdpx, transcripts, auto-coding, ai-coding]
level: practitioner
status: draft
description: "Set up and run a project in NVivo, ATLAS.ti or MAXQDA: import and case structure, code system, attributes, matrix/co-occurrence queries, memos, and team coding without merge disasters."
sources: ["Lumivero NVivo help documentation", "ATLAS.ti user manual", "MAXQDA online manual", "REFI-QDA Project exchange standard (qdasoftware.org)", "Silver & Lewins, Using Software in Qualitative Research (2nd ed., Sage 2014)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QDA software — set up so the queries work later

**Goal:** a project whose structure lets you ask comparative questions ("how do
managers vs staff talk about workload?") at the end, and that survives several coders.
The software does not analyse; it stores coding so you can retrieve and compare.
Method choices are in
social-sciences.social-research-methods.qualitative-coding-analysis.thematic-analysis-codebooks-and-saturation.

## 1. Vocabulary across the three
| Concept | NVivo | ATLAS.ti | MAXQDA |
|---|---|---|---|
| Code | Code (formerly node) | Code | Code |
| Coded segment | Reference | Quotation | Coded segment |
| Participant-level data | Case + classification attributes | Document groups / document variables | Document variables |
| Comparison table | Matrix coding query / crosstab | Code-Document table | Crosstabs, Code Matrix Browser |
| Co-occurrence | Coding query / framework matrix | Code co-occurrence table | Code Relations Browser |

## 2. Before importing
- Clean transcripts in a word processor: consistent speaker labels (`INT:`, `P07:`), headings
  for guide sections (Heading 1/2 styles enable **auto-coding** by structure or speaker),
  anonymised names and places, a file name that contains the participant ID.
- Prepare a spreadsheet of participant attributes (ID, role, site, gender, age band) with the
  ID column matching file names exactly.

## 3. Setup sequence
1. Create project; store it in a backed-up location — but **not** in a live-syncing folder
   (Dropbox/OneDrive) for single-file projects, which risk corruption mid-save; vendor cloud
   or team editions are the exception.
2. Import documents (and audio/video with timestamps if you want to code media).
3. Create cases/document variables and import the attribute spreadsheet.
4. Build the starting code system (deductive codes from the guide or framework); add a
   "parking" code for promising-but-unclear segments.
5. Write a project memo for decisions and a memo per document.

## 4. Coding practice in the tool
- Code meaningful units with enough context; it is easy to extend later by viewing context.
- Keep **code descriptions** filled in — they export into the codebook.
- Hierarchies two to three levels deep; deeper trees become unnavigable.
- Use colours or sets for analytic status (draft, stable, theme-candidate) instead of
  overloaded names.

## 5. Queries that answer research questions
- **Matrix/crosstab:** codes × attribute values (e.g. role) → counts of cases coded, then
  click into cells to read the actual segments. Report what the segments say, not just counts.
- **Co-occurrence:** which codes overlap within segments — useful for theme building.
- **Text search / word frequency:** for checking coverage and finding uncoded mentions; treat
  as exploratory.
- Save queries so they rerun after more coding.
- **AI-assisted coding** now offered by all three (and by many web tools): treat suggestions as
  a first pass needing human review, check data-protection terms before sending transcripts to
  a cloud model, and report its use in the methods.

## 6. Team coding without losing work
- NVivo/ATLAS.ti/MAXQDA desktop: each coder works on a **copy**, coded against an identical
  master code system; merge periodically. Never let coders add codes independently between
  merges — duplicate near-identical codes are the usual result. Agree code changes centrally.
- Use user/coder identity in the software so agreement can be computed (NVivo coding
  comparison query; MAXQDA intercoder agreement; ATLAS.ti intercoder agreement module).
- Server/cloud editions allow simultaneous work but check licence and institution policy.
- **REFI-QDA (.qdpx)** export lets you move projects between packages; codes and segments
  transfer, some features (queries, certain memos) may not — test on a copy.

## Gotchas
- Editing a document's text after coding can shift or drop coded segments.
- Attributes imported with a mismatched ID silently create new empty cases.
- Version mismatch: older desktop versions cannot open projects saved by newer ones.

## Verify
- [ ] Every document linked to a case with complete attributes.
- [ ] Code system has descriptions; exported codebook matches.
- [ ] At least one saved matrix query aligned to each comparative research question.
- [ ] Team merge procedure written down and tested on copies; backups dated.
- [ ] Any AI-assisted coding disclosed and checked by a human.

*Draft: feature names change between releases; confirm against the current version you license.*
