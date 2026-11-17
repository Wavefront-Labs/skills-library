---
id: transportation-logistics.trade-compliance-customs-brokerage.customs-declaration-filing.building-an-import-entry-and-calculating-duty
name: building-an-import-entry-and-calculating-duty
category: transportation-logistics
field: trade-compliance-customs-brokerage
product: customs-declaration-filing
tags: [customs-declaration, import-entry, entry-preparation, duty-calculation, ad-valorem, specific-duty, compound-duty, mpf, merchandise-processing-fee, hmf, vat, import-vat, cif, fob, customs-value, exchange-rate, antidumping, section-301, release, post-entry-correction, customs-broker, entry-checklist]
level: practitioner
status: gated
description: "Turning a commercial document set into an import declaration line by line, calculating duty, fees and import VAT (US and EU/UK bases differ), chasing release and correcting after entry."
sources: ["https://www.ecfr.gov/current/title-19/section-24.23", "https://www.ecfr.gov/current/title-19/section-24.24", "https://www.ecfr.gov/current/title-19/part-141", "https://www.gov.uk/government/organisations/hm-revenue-customs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building an import entry and calculating duty

**Goal:** produce a declaration whose every line ties back to the documents, with duty
and taxes calculated correctly on the right base, and see it through to release.

## 1. Gather and reconcile the documents
Commercial invoice, packing list, transport document (B/L or AWB), any certificate of
origin, licences/permits, and the classification record. Before keying anything:
- Invoice quantities = packing list = transport document (pieces, gross weight).
- Seller, buyer, importer of record and consignee identified; related-party status noted.
- Incoterm stated — it decides which freight/insurance costs go into the value.
- Currency and invoice date noted (exchange rate rules key off the export or
  declaration date).

## 2. Build the lines
One line per tariff code + origin + other distinguishing factor (preference claimed,
licence). For each: code, description, quantity in the code's statistical unit(s),
origin, value, preference indicator, and any agency data.

## 3. Calculate duty and taxes
Duty types: **ad valorem** (% of value), **specific** (per kg/litre/unit), **compound**
(both). Then add trade remedies (anti-dumping/countervailing, US Section 301/232) where
applicable.
**Value base differs:**
- **US:** duty on **FOB-type transaction value** — international freight and
  insurance are *excluded* (deducted if included in the price). Fees: MPF 0.3464 % ad
  valorem with a min/max per formal entry that CBP adjusts annually (19 CFR 24.23; the regulation text
  shows base figures of $25 and $485, not the current ones); HMF 0.125 % for ocean cargo (19 CFR 24.24).
  *Check the current MPF min/max in the CBP Federal Register notice.*
- **EU/UK (gated: unconfirmed, source is paywalled or blocked) EU and HMRC pages were not read:** duty on **CIF value** to the border (freight and insurance to the point
  of entry added). Import VAT on (customs value + duty + costs to destination in the
  country).
Worked example (UK, illustrative; the arithmetic is only an example): CIF £10,000, duty 4 % = £400; import VAT 20 % on
(£10,000 + £400) = £2,080. Total payable £2,480 (VAT usually reclaimable/postponed
for VAT-registered importers via postponed VAT accounting).
Worked example (US): invoice CIF $10,000 with $800 freight + $50 insurance → entered
value $9,150; duty 4 % = $366; MPF 0.3464 % ≈ $31.70 (within min/max); HMF 0.125 % ≈
$11.44.

## 4. Release follow-through
- Watch for holds: documentary checks, physical exams, other-agency holds. Respond to
  document requests the same day.
- Tell the client what is causing a hold and the realistic time — exams can add days
  and storage/demurrage charges.
- After release, confirm the declaration matches what was physically received (shortages,
  overages).

## 5. Post-entry corrections
- Errors in value, code or origin: correct promptly — US PSC before liquidation; EU/UK
  amendment or repayment claims (gated: unconfirmed, source is paywalled or blocked). Underpayments discovered later may
  need a voluntary/prior disclosure to mitigate penalties.
- Track overpayments for refunds; time limits apply; confirm with the authority.

## Gotchas
- Assists, royalties and buying vs. selling commissions change value — see
  valuation-rules-of-origin.
- Using the wrong exchange rate date; most systems fix the rate by rule — let the
  system apply it rather than using today's bank rate.
- Statistical units (e.g. "doz", "kg", "No.") required by the code; missing
  second quantity is a frequent reject.
- Preference claims without origin evidence on file are a later audit liability.

## Verify
- [ ] Quantities, weights and values reconcile across invoice, packing list and transport document.
- [ ] Value base correct for the jurisdiction (US FOB-type vs. EU/UK CIF).
- [ ] Duty, trade remedies, fees and import VAT calculated and cross-checked against the system.
- [ ] All holds cleared and release confirmed.
- [ ] Any correction filed within the applicable time limit.

## Checked

Jurisdiction: United States (CBP, 19 CFR) with EU/UK notes. Checked 2026-10-25 against current eCFR: 19 CFR 24.23 (MPF 0.3464 percent, min/max adjusted annually, current amounts published by CBP), 24.24 (HMF 0.125 percent). US worked example arithmetic recomputed (9,150 entered value, duty 366, MPF 31.69, HMF 11.44). The EU/UK valuation basis and UK repayment route were not confirmed (HMRC and EUR-Lex pages unavailable) and are marked gated.

Method: documentation only; no commands were run.
