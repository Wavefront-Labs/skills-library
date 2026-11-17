---
id: law-government.intellectual-property-law.ip-litigation.infringement-contentions-claim-construction-and-remedies
name: infringement-contentions-claim-construction-and-remedies
category: law-government
field: intellectual-property-law
product: ip-litigation
tags: [intellectual-property-law, ip-litigation, patent-litigation, trademark-litigation, copyright-litigation, infringement, claim-chart, infringement-contentions, invalidity-contentions, claim-construction, markman, phillips, doctrine-of-equivalents, prior-art, ipr, ptab, preliminary-injunction, ebay-factors, damages, reasonable-royalty, georgia-pacific, lost-profits, willfulness, upc, pre-suit-investigation, rule-11]
level: advanced
status: docs-checked
description: "Run the core of an IP case: pre-suit claim charts, infringement and invalidity contentions, claim construction, parallel validity challenges, and injunction and damages theory."
sources: ["Federal Rule of Civil Procedure 11 (https://www.law.cornell.edu/rules/frcp/rule_11)", "35 U.S.C. 311 (https://www.law.cornell.edu/uscode/text/35/311)", "35 U.S.C. 315 (https://www.law.cornell.edu/uscode/text/35/315)", "35 U.S.C. 316 (https://www.law.cornell.edu/uscode/text/35/316)", "35 U.S.C. 284 (https://www.law.cornell.edu/uscode/text/35/284)", "eBay v. MercExchange, No. 05-130 (https://www.law.cornell.edu/supremecourt/text/05-130)", "EPC Article 99 (https://www.epo.org/en/legal/epc/2020/a99.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infringement contentions, claim construction and remedies

**Goal:** frame an IP dispute so that the decisive issues — what the right covers, whether
the accused product falls within it, whether the right is valid, and what the remedy is
worth — are won early. Patent cases (US district courts with local patent rules,
Federal Circuit; Europe's Unified Patent Court) are the main frame; trademark and
copyright cases follow the same "scope → infringement → validity → remedy" spine.
Procedure is highly forum-specific; read the local rules first.

## 1. Pre-suit investigation (plaintiff)
- Obtain and test the accused product; build a **claim chart**: each claim element in
  one column, evidence (photos, teardown, source code, documentation) in the next, with
  pin cites. A chart with gaps is a warning, not a draft.
- Pre-suit diligence matters: under US Federal Rule of Civil Procedure 11(b)(3) factual
  contentions must have evidentiary support after reasonable inquiry, and a court may
  sanction a violation after notice (Rule 11(c)).
- Check standing (ownership, recorded assignments, exclusive licensee rights), patent
  term and maintenance fees, and forum/venue.
- Assess the counterattack: validity challenges, counterclaims on the defendant's patents,
  licence or exhaustion defences.

## 2. Contentions
Many US districts require early, detailed contentions:
- **Infringement contentions**: each asserted claim, each accused instrumentality, element-
  by-element chart, literal vs **doctrine of equivalents** theory, and any indirect
  infringement theory (inducement or contributory infringement).
- **Invalidity contentions**: prior art charts per claim (anticipation / obviousness
  combinations), §112 and §101 grounds. Amending contentions later often needs good cause.
- Trademark/copyright analogues: likelihood-of-confusion factor evidence; access plus
  substantial similarity analysis (filter out unprotectable elements first).

## 3. Claim construction
- Identify terms that decide infringement or validity — usually a handful. Propose
  constructions that win on *both* fronts; broad readings help infringement but invite
  invalidity, and vice versa.
- Read the claims themselves, the specification and the prosecution history (disclaimers,
  estoppel) first, with extrinsic evidence (dictionaries, experts) as secondary; confirm
  the current Federal Circuit approach.
- Claim-construction (**Markman**) briefing and hearing can decide the case. Prepare a
  tutorial for the judge and plain-language explanations of the technology.

## 4. Parallel validity challenges
- US **inter partes review** (PTAB): grounds limited to anticipation and obviousness
  (35 U.S.C. 102, 103) on patents or printed publications (35 U.S.C. 311(b)); the
  petitioner must prove unpatentability by a preponderance of the evidence (35 U.S.C.
  316(e)); a petition filed more than 1 year after service of an infringement complaint is
  barred (35 U.S.C. 315(b)); after a final written decision the petitioner is estopped
  from asserting grounds it raised or reasonably could have raised (35 U.S.C. 315(e)).
- Consider stays of litigation pending review; discretionary denial practice changes
  frequently — check current PTAB policy.
- Europe: oppositions at the EPO within 9 months of the publication of the mention of
  grant (Art. 99(1) EPC); revocation actions/counterclaims at the UPC or national courts.

## 5. Remedies
- **Injunctions**: in US patent cases a plaintiff seeking a permanent injunction must show
  irreparable injury, inadequacy of legal remedies, that the balance of hardships
  warrants equitable relief and that the public interest would not be disserved
  (*eBay v. MercExchange*); it is not automatic. Other courts differ.
- **Damages** (US, 35 U.S.C. 284): adequate to compensate, in no event less than a
  reasonable royalty, plus interest and costs; the court may increase damages up to three
  times.
- Trademark: defendant's profits, damages, corrective advertising; copyright: actual or
  statutory damages (if registered in time — see copyright practice skill).

## Gotchas
- Plan privilege strategy early for any opinion of counsel.
- Source-code review under protective orders is slow; schedule it.

## Verify
- [ ] Pre-suit claim chart covers every element with evidence and pin cites.
- [ ] Standing, marking, venue and patent status confirmed.
- [ ] Contentions served on time with every theory you'll rely on.
- [ ] Proposed constructions tested against both infringement and validity positions.
- [ ] IPR/opposition deadlines and estoppel effects analysed; remedy theory has an apportioned damages model.

## Checked
Checked 2026-10-24. Jurisdiction: United States federal courts and PTAB, with the EPO for the opposition line. Sources read 2026-10-24: FRCP 11(b)(3) and (c); 35 U.S.C. 311(b), 315(b), 315(e), 316(e), 284; eBay v. MercExchange (the four factors; not automatic); EPC Art. 99(1) (nine months from publication of the mention of grant). Removed unconfirmed statements on marking, Phillips, Georgia-Pacific, equivalents tests, indirect-infringement intent, attorney fees in exceptional cases, European injunction practice and discoverability of opinions. General information, not legal advice.
Method: documentation only; no commands were run.
