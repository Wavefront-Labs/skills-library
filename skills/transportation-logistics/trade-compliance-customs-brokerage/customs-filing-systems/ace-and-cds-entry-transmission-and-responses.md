---
id: transportation-logistics.trade-compliance-customs-brokerage.customs-filing-systems.ace-and-cds-entry-transmission-and-responses
name: ace-and-cds-entry-transmission-and-responses
category: transportation-logistics
field: trade-compliance-customs-brokerage
product: customs-filing-systems
tags: [customs-filing, ace, abi, cbp, cbp-7501, cbp-3461, entry-summary, cargo-release, isf, 10-plus-2, pga, post-summary-correction, psc, liquidation, cds, customs-declaration-service, hmrc, eori, ucc, ics2, customs-broker-software, entry-rejection, edi]
level: practitioner
status: gated
description: "Transmitting entries in electronic customs systems (US ACE via ABI, UK CDS): filing sequence, deadlines, reading accept/reject and hold messages, and correcting entries after release."
sources: ["https://www.ecfr.gov/current/title-19/section-149.2", "https://www.ecfr.gov/current/title-19/section-142.12", "https://www.ecfr.gov/current/title-19/section-159.11", "https://www.ecfr.gov/current/title-19/section-174.12", "https://www.ecfr.gov/current/title-19/section-163.4", "https://www.cbp.gov/sites/default/files/assets/documents/2018-Nov/Updated%20ISF%20FAQ%20FINAL%2011282018.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACE and CDS: entry transmission and responses

**Goal:** get a correct declaration into the customs system on time, read what comes
back, and fix problems without triggering penalties. Examples: US ACE (via ABI, the
broker interface) and UK CDS. EU member-state systems under the UCC follow similar
logic. *Software screens differ by vendor; the message flow below is the constant.*

## 1. US ACE filing sequence (ocean import example)
1. **ISF (10+2)** — Importer Security Filing most data elements at least **24 h before lading** aboard the vessel at the
   foreign port (19 CFR 149.2); container stuffing location and consolidator no later than 24 h before arrival at a US port. CBP guidance says late or inaccurate ISFs draw liquidated damages of $5,000 per violation (CBP ISF FAQ, 2018 edition; confirm the current mitigation guidelines).
2. **Cargo release / entry (CBP 3461 data)** — request release when cargo arrives or
   pre-file before arrival. Include PGA data (FDA, USDA/APHIS, EPA, CPSC, etc.) for
   regulated goods, or the shipment will hold.
3. **Entry summary (CBP 7501 data)** — within **10 working days after entry** (19 CFR 142.12(b)), with
   classification, value, origin, duties and fees (MPF, HMF). Duty is paid with the
   summary (ACH or periodic monthly statement).
4. **Liquidation** — occurs within one year of entry or the entry is deemed liquidated as entered (19 CFR 159.11); until then corrections go in as a
   **Post Summary Correction (PSC)**. After liquidation you need a protest (within 180
   days of liquidation, 19 CFR 174.12) or a prior disclosure for errors.

## 2. Reading responses
- **Accept** of the summary ≠ correct; it only means the data passed edits.
- **Reject** messages carry an error code and narrative — fix the data and
  retransmit the same entry number; don't open a new entry.
- **Holds:** CBP exam (intensive/VACIS), PGA "may proceed" vs. "hold", or document
  review requests. Track each separately — release requires all agencies cleared.
- Monitor **ACE Reports** daily for entries pending summary, unpaid statements and
  PGA status. Missed 10-day summaries lead to liquidated damages claims.

## 3. UK CDS essentials
- Every trader needs an **EORI** (gated: unconfirmed, source is paywalled or blocked) HMRC pages were not read (GB… for Great Britain; XI… for Northern Ireland
  movements).
- Declarations are built from **data elements** (gated: unconfirmed, source is paywalled or blocked) (DE 1/1 declaration type, DE 6/14
  commodity code, DE 4/14 item price, etc.) rather than the old CHIEF boxes.
- Choose declaration category (e.g. H1 standard import) and procedure codes (e.g.
  4000 000 release for free circulation). Wrong CPC is the most common rejection
  and can claim the wrong relief.
- Duty deferment account or cash; check the Duty Deferment Account limit before
  peak periods.
- Amendments before clearance in CDS; after clearance, use the post-clearance
  amendment route (C285 claims for overpayments).

## 4. Good habits
- Pre-validate data before transmit: HS code valid for the date, origin, quantity units
  required for the code, value currency and exchange-rate date.
- Keep the **audit trail**: commercial invoice, packing list, B/L/AWB, classification
  notes, and the transmitted message ID per entry (US retention: 5 years from date of entry, 19 CFR 163.4(a); UK period: confirm with HMRC (gated: unconfirmed, source is paywalled or blocked)).
- Use test/certification environments when changing software or adding a new PGA.

## Gotchas
- Duplicate entries from retransmitting as new after a reject.
- Bond sufficiency (US continuous bond) exhausted mid-year halts releases.
- Wrong importer of record number/EORI attaches liability to the wrong party.
- *Deadlines and penalty amounts quoted are standard figures; confirm current values.*

## Verify
- [ ] ISF filed ≥ 24 h before foreign loading (ocean US).
- [ ] All agency holds cleared before telling the client goods are released.
- [ ] Entry summary transmitted and paid within 10 working days after entry.
- [ ] Reject codes resolved on the same entry number.
- [ ] Documents and message IDs archived per entry.

## Checked

Jurisdiction: United States (CBP, 19 CFR) with EU/UK notes. Checked 2026-10-25 against current eCFR: 149.2 (ISF 24 h before lading), 142.12 (summary within 10 working days after entry), 159.11 (one year liquidation), 174.12 (protest 180 days), 163.4 (5 years). ISF damages of $5,000 per violation from the CBP ISF FAQ (Nov 2018) and Mitigation Guidelines. Corrected: the draft said 10 days of release and a 314-day liquidation figure that is not in the regulation. UK CDS specifics were not confirmed and are marked gated.

Method: documentation only; no commands were run.
