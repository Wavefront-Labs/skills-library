---
id: manufacturing-production.pharmaceutical-manufacturing.gmp-practice.data-integrity-and-deviation-discipline-on-the-floor
name: data-integrity-and-deviation-discipline-on-the-floor
category: manufacturing-production
field: pharmaceutical-manufacturing
product: gmp-practice
tags: [gmp-practice, gmp, cgmp, good-manufacturing-practice, alcoa, alcoa-plus, data-integrity, good-documentation-practice, gdp, deviation, capa, gowning, hygiene, audit-readiness, inspection-readiness, 21-cfr-211, 21-cfr-part-11, eu-gmp, eudralex, pic-s, mhra, fda-483, line-clearance, right-first-time, pharmaceutical-manufacturing, pharma-operator]
level: practitioner
status: docs-checked
description: "How an operator works to GMP on a pharma floor: ALCOA+ entries, correcting errors properly, raising deviations fast, gowning discipline, and behaving well when an inspector walks in."
sources:
  - "https://www.ecfr.gov/current/title-21/part-11/subpart-B/section-11.10"
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-D/section-211.68"
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-J/section-211.192"
  - "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers"
  - "https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data integrity and deviation discipline on a GMP floor

**Goal:** every record you touch would survive an inspector reading it cold, and every
time reality departs from the procedure, a deviation exists before anyone "fixes" it.

## 1. ALCOA+ as habits, not a poster
| Letter | What it means at your bench |
|---|---|
| **A**ttributable | Your own initials/login, never a colleague's. Never share passwords or sign while someone else is logged in (FDA's 2018 data-integrity Q&A: shared login credentials mean a unique individual cannot be identified). |
| **L**egible | Permanent ink (usually blue or black per site SOP); no pencil, no correction fluid. |
| **C**ontemporaneous | Record at the time of the action. "I'll fill it in at break" is the single most common observation. |
| **O**riginal | The first capture is the record. Writing on a glove, a scrap or a whiteboard then transcribing is a finding. |
| **A**ccurate | Record what the display showed, including the decimals, not what you expected. |
| **+ Complete, Consistent, Enduring, Available** | No blank fields (line through and "N/A" with initials/date), time order makes sense, records stay readable and retrievable. |

**Correcting an error (paper):** single line through so the original stays readable, the
correct value beside it, initials, date and — at most sites — a short reason ("transcription
error"). Never overwrite, never obliterate. Exact format is site-SOP-specific; check yours.

**Electronic systems:** 21 CFR 11.10(e) calls for secure, computer-generated, time-stamped audit trails that record operator entries and actions, and 11.10(d) calls for limiting system access to authorised individuals; the audit trail records who changed what. Don't re-run a test or
re-weigh "to get a better number" — reprocessing or repeat measurements without a
documented reason is the classic "testing into compliance" finding.

## 2. Deviations: raise first, explain later
1. **Stop and make it safe** — don't continue a step whose conditions you know are wrong.
2. **Tell your supervisor / QA immediately** and note the time.
3. **Record the facts** in the batch record exactly as they happened.
4. **Raise the deviation** in the QMS (TrackWise, Veeva Vault QMS, MasterControl or paper —
   site-dependent) within the window your SOP sets.
5. **Don't** quietly redo, adjust or "correct" product before QA has assessed it.

Investigations then classify (minor/major/critical), find root cause and set **CAPA**. Your
part as an operator: give a factual account, keep evidence (labels, printouts, the
failed component), and don't speculate in the record. "Human error" as a root cause is
weak and inspectors push back on it — say what made the error likely (confusing SOP,
similar labels, time pressure).

## 3. Gowning and hygiene
- Follow the posted gowning sequence exactly; the order (e.g. hair cover before gown) is
  part of the validated process. Grade-specific gowning for sterile areas is covered in
  manufacturing-production.pharmaceutical-manufacturing.sterile-aseptic-processing.aseptic-technique-and-cleanroom-behaviour.
- No jewellery, make-up, nail varnish or phones beyond the change room unless permitted.
- Report illness, open wounds or skin conditions before entering — that's an obligation, not optional.
- Line clearance before every batch/product change: remove all previous materials, labels
  and documents, then get the second-person check signed.

## 4. When an auditor or inspector walks in
- Keep working to the SOP; don't stop or speed up.
- Answer the question asked, truthfully and briefly. "I don't know, but I know who does"
  is a fine answer; guessing is not.
- Show where a document is; don't hand over uncontrolled copies or personal notes.
- Never tidy, sign or backdate anything because someone is watching.

## Gotchas
- **Pre-filling** entries (times, weights) before doing the step is falsification even if
  the numbers come out right.
- **Uncontrolled copies** of SOPs pinned at a station drift out of date — use the issued version.
- **Second-person verification** means actually watching the step, not signing afterwards.
- Regulation differs by region. US: 21 CFR 211 (including 211.68 on computer controls and 211.192 on investigations) and Part 11; the EU
  computerised-systems rules are in EudraLex Volume 4 Annex 11 (revision January 2011). Specific wording comes from your site SOPs.

## Verify
- [ ] Every entry you made today was written at the time, in your own name, in permanent ink or your own login.
- [ ] Every correction shows the original value, the new value, initials, date (and reason if the SOP asks).
- [ ] No blank fields left without N/A.
- [ ] Every departure from procedure today has a deviation number or has been reported to QA.
- [ ] You can name the SOP that governs the step you are doing right now.

## Checked

Date: 2026-10-25. Jurisdiction: United States (FDA 21 CFR Parts 211 and 11, eCFR current text checked 20 October 2026; FDA data-integrity Q&A, December 2018) with the EU Annex 11 title and revision date from the European Commission EudraLex page.

Confirmed: 11.10(d) and (e); 211.68 computer controls; 211.192 investigations; FDA Q&A position on shared logins (via a search of the FDA guidance text; the PDF could not be read directly). ALCOA is described as FDA frames it (attributable, legible, contemporaneous, original, accurate). Removed as unconfirmed: the 24 hour deviation window, the PIC/S reference and the exact QMS vendor behaviour. Ink colour, gowning order and similar items are site practice that the skill already defers to SOPs.

Method: documentation only; no commands were run.
