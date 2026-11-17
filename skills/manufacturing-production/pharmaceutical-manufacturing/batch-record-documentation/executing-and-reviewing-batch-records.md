---
id: manufacturing-production.pharmaceutical-manufacturing.batch-record-documentation.executing-and-reviewing-batch-records
name: executing-and-reviewing-batch-records
category: manufacturing-production
field: pharmaceutical-manufacturing
product: batch-record-documentation
tags: [batch-record-documentation, batch-record, mbr, master-batch-record, bmr, batch-manufacturing-record, ebr, electronic-batch-record, mes, pas-x, syncade, pharmasuite, review-by-exception, rbe, batch-release, qp-release, good-documentation-practice, gdp, alcoa, exceptions, reconciliation, yield, gmp, 21-cfr-211-188, pharmaceutical-manufacturing]
level: practitioner
status: docs-checked
description: "Execute a pharma batch record step by step (paper or EBR), document exceptions properly, reconcile materials and yields, and review the record so it supports release first time."
sources:
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-J/section-211.188"
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-G/section-211.130"
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-J/section-211.192"
  - "https://www.ecfr.gov/current/title-21/part-11/subpart-C/section-11.100"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Executing and reviewing batch records

**Goal:** the executed batch record is a complete, contemporaneous story of exactly this
batch, so QA can release it without sending it back. Right-first-time is the metric most
sites track.

## 1. Before you start a step
- Confirm you have the **issued** record for this batch: correct product, batch number,
  version, and page count (paper) or the right order/recipe in the MES.
- Read the whole step, including any "verify" or "second person" boxes, before acting.
- Have the equipment IDs, material lot numbers and calibrated instruments to hand.

## 2. Executing (paper MBR/BMR)
- Fill each field **as you do it**: actual time from the room clock (sites usually
  specify which clock), actual weights from the balance printout, equipment ID from the tag.
- Attach printouts (balance tickets, chart recorder traces) where the record says and
  sign/date across the printout edge so it can't be swapped (site practice varies).
- Unused fields: line through, "N/A", initials, date. Never leave blanks.
- Second-person verifications (dispensing, critical additions, line clearance) are done
  **while watching**, not afterwards.
- If the instruction can't be followed as written, stop — that's a deviation (see
  manufacturing-production.pharmaceutical-manufacturing.gmp-practice.data-integrity-and-deviation-discipline-on-the-floor).
  Write in the comments field what happened and the deviation number.

## 3. Executing in an EBR / MES
- The system enforces sequence, limits and identity (barcode scans). **Don't fight it**:
  a scan that won't accept means wrong material, wrong lot or expired status — investigate,
  don't hand-key around it.
- Out-of-limit entries create an **exception** automatically. Add a clear, factual
  comment at the time (what, why, who was told). The comment is what the reviewer reads.
- Never share a login or let someone sign under your session — each electronic signature must be unique to one individual and cannot be reused or reassigned (21 CFR 11.100(a)), and the signer certifies it is the legally binding equivalent of a handwritten signature (11.100(c)).

## 4. Reconciliation and yield
Before closing:
- **Material reconciliation:** issued = used + returned + rejected/destroyed, within the
  limits stated in the MBR.
- **Labels/printed components:** reconcile exactly as the MBR states. 21 CFR 211.130 requires labelling materials to be examined before use and the packaging area to be inspected before use, both documented in the batch record.
- **Yield** at each stage against the stated range: the record must show actual yield and percentage of theoretical yield at the appropriate phases (21 CFR 211.188(b)), and unexplained discrepancies such as yield outside set limits must be thoroughly investigated (211.192).

## 5. Reviewing the record (production then QA)
Review in a fixed order so nothing is skipped:
1. Every page/step present and signed; no blanks.
2. Every value within limits — or there is a linked exception/deviation.
3. Corrections compliant (original visible, initials, date, reason).
4. Times run forward and are physically plausible (a 30 min blend logged as 5 min is a red flag).
5. Attachments present and match (balance ticket weights = recorded weights).
6. Deviations closed or assessed for release impact.

**Review by exception (RBE):** in a validated EBR, the reviewer looks only at flagged
exceptions, not every field. It only works if the system's limit checks were validated —
so data entered *outside* the system (free-text comments, paper attachments) still gets
full review. Exact RBE scope is defined by each site's validation; treat my description
as the general pattern.

## Gotchas
- Using the clock on your phone or a different room — times across steps don't line up.
- Copying a weight from the previous batch's page by habit.
- Recording "OK" or a tick where a value was asked for.
- Closing an EBR step with an open exception you meant to comment on later — you often can't edit afterwards.
- The record isn't done when manufacturing ends: QA review findings come back to the
  signer, so clear answers up front save cycles.

## Verify
- [ ] Batch number, product and MBR version match on every page/screen.
- [ ] No blank fields; every N/A initialled.
- [ ] All out-of-limit values have an exception comment or deviation number.
- [ ] Materials and labels reconciled within limits; yield in range or investigated.
- [ ] Attachments present, signed and consistent with entries.
- [ ] Review comments from QA answered with facts, not re-signatures.

## Checked

Date: 2026-10-25. Jurisdiction: United States (FDA, 21 CFR Parts 211 and 11, eCFR current text checked 20 October 2026). Site SOPs govern the practice steps.

Confirmed in the eCFR: 211.188(b) record contents (dates, equipment, component lots, weights, in-process results, packaging area inspection, actual and percent theoretical yield, who performed and checked each significant step, investigations under 211.192); 211.130 labelling controls and area inspection; 211.192 investigation of yield and specification discrepancies and quality-unit review of records; 11.100(a) and (c) on electronic signatures. Removed as unconfirmed: the EU Annex 11 statement, the list of MES vendors and the "usually 100 %" reconciliation figure. Review by exception is described as a general pattern, with site validation defining scope.

Method: documentation only; no commands were run.
