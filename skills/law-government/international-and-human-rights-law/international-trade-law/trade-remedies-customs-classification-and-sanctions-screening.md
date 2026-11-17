---
id: law-government.international-and-human-rights-law.international-trade-law.trade-remedies-customs-classification-and-sanctions-screening
name: trade-remedies-customs-classification-and-sanctions-screening
category: law-government
field: international-and-human-rights-law
product: international-trade-law
tags: [international-and-human-rights-law, international-trade-law, wto, gatt, dispute-settlement, appellate-body, mpia, anti-dumping, countervailing-duties, safeguards, dumping-margin, normal-value, export-price, material-injury, causation, harmonized-system, hs-code, tariff-classification, general-rules-of-interpretation, gri, binding-ruling, rules-of-origin, fta, sanctions, ofac, sdn-list, 50-percent-rule, export-controls, dual-use, customs-valuation]
level: advanced
status: gated
description: "Core trade-law workflows: WTO and FTA disputes, anti-dumping and countervailing proceedings, HS tariff classification via the GRIs, origin, and sanctions and export-control screening."
sources: ["https://www.wto.org/english/tratop_e/dispu_e/appellate_body_e.htm", "https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx", "https://ofac.treasury.gov/faqs/401", "https://www.wto.org/english/docs_e/legal_e/19-adp_01_e.htm", "https://www.wto.org/english/docs_e/legal_e/24-scm_01_e.htm", "https://www.wto.org/english/docs_e/legal_e/gatt47_02_e.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trade remedies, customs classification and sanctions screening

**Goal:** handle the four everyday problems of trade-law practice — state-to-state
trade disputes, trade-remedy investigations against a client's exports or imports,
classifying goods for duty, and keeping transactions clear of sanctions and export
controls. Treaties (WTO, FTAs, HS Convention) are shared; investigating authorities,
customs administrations and sanctions regimes are national (or EU-level) with their own
procedures and very short deadlines. Sanctions lists change daily — always check live.

## 1. WTO and FTA disputes (state-to-state)
- Private companies can't sue; they persuade their government. Build the factual record
  and the legal theory (e.g. GATT Art I MFN, Art III national treatment, Art XI
  quantitative restrictions; defences under Art XX general exceptions and Art XXI
  security exceptions).
- Process: consultations → panel → appeal. The WTO **Appellate Body** is unable to
  review appeals because of ongoing vacancies (WTO website; the last sitting member's term expired on 30 November 2020). The binding effect of a panel report appealed "into the void" and the interim **MPIA** arbitration arrangement
  (gated: unconfirmed, source is paywalled or blocked) should be checked at the WTO.
- FTAs have their own state-to-state chapters, and some include investor-state mechanisms
  (see law-government.international-and-human-rights-law.international-arbitration).

## 2. Trade remedies (anti-dumping, countervailing, safeguards)
- **Anti-dumping**: dumping (export price below **normal value**, usually home-market
  price or constructed value) + **material injury** (or threat) to the domestic industry
  + **causal link**. Remedy: duties up to the dumping margin (some systems apply a
  "lesser duty").
- **Countervailing**: specific subsidies (financial contribution + benefit + specificity)
  causing injury.
- **Safeguards**: import surges causing serious injury, no unfair-trade finding needed.
- For a respondent exporter: questionnaire responses are due fast, must be complete and
  verifiable — the authority may use **facts available** (often adverse) for gaps.
  Prepare for on-the-spot verification of sales and cost data.
- Track: initiation notice, questionnaire deadlines, preliminary determination,
  verification, final determination, review cycles (administrative/expiry reviews),
  and appeal routes (domestic courts; WTO challenge by government).

## 3. Tariff classification (HS)
The Harmonized System is uniform internationally to **6 digits**; national extensions
(8–10 digits) differ. Classify by the **General Rules of Interpretation (GRI)**, in order (gated: unconfirmed, source is paywalled or blocked):
1. **GRI 1**: headings' terms and Section/Chapter Notes govern; titles are for reference only.
2. GRI 2: incomplete/unassembled goods with essential character; mixtures.
3. GRI 3: when two headings apply — (a) most specific description, (b) essential character
   for mixtures/sets, (c) last in numerical order.
4. GRI 4: most akin goods. GRI 5: packaging. GRI 6: subheading level, same method.
Use the WCO Explanatory Notes and classification opinions, plus national rulings. Where
duty exposure is material, obtain a **binding ruling** from customs.

## 4. Origin and valuation
- **Preferential origin** under an FTA: wholly obtained, tariff-shift, regional value
  content or specific process rules — product-specific rules in the annex. Keep supplier
  declarations and cost records for verification.
- Non-preferential origin matters for marking, quotas and trade remedies.
- **Customs valuation**: transaction value with adjustments (assists, royalties, commissions)
  under the WTO Valuation Agreement; related-party pricing must be shown not to influence price.

## 5. Sanctions and export controls
- Screen counterparties, owners, banks, vessels and end-users against lists (e.g. US OFAC
  SDN, EU and UK consolidated lists, UN lists).
- Ownership rules: US OFAC treats entities **50% or more owned** (aggregate) by blocked
  persons as blocked; EU/UK use ownership *and control* tests (gated: unconfirmed, source is paywalled or blocked). Run ownership traces.
- Sectoral and country-wide sanctions restrict activity even without listed parties.
- **Export controls** (dual-use lists, military lists, end-use/end-user controls): classify
  the item's control number, check licence requirements by destination and end use.
- Red flags: unusual routing, reluctance about end use, cash payments, transshipment hubs.
- Voluntary self-disclosure regimes can reduce penalties — escalate promptly.

## Gotchas
- Classification by product marketing name instead of objective characteristics.
- Missing a trade-remedy questionnaire extension window; extensions are discretionary.
- Relying on screening software without reviewing fuzzy matches and ownership.

## Verify
- [ ] For disputes: legal theory mapped to specific agreement articles and current dispute-settlement availability checked.
- [ ] Trade-remedy deadlines docketed; responses complete and verifiable.
- [ ] HS classification reasoned through GRIs in order with Notes cited.
- [ ] Origin claims backed by product-specific rule analysis and records.
- [ ] Sanctions/export-control screening done on current lists including ownership.

## Checked

Checked 2026-10-25. Jurisdiction: International trade rules (WTO, HS) and United States OFAC sanctions; national customs and trade-remedy rules differ.

Confirmed: WTO website (the Appellate Body is currently unable to review appeals given its ongoing vacancies; the term of the last sitting member expired on 30 November 2020). WCO (the HS uses six-digit codes and is used by more than 200 countries and economies). OFAC FAQ 401 (entities owned 50 percent or more in the aggregate, directly or indirectly, by one or more blocked persons are blocked; stakes are aggregated; ownership, not control, is the test). Gated: the order of the General Rules of Interpretation, the MPIA description and the EU and UK ownership-and-control tests were not confirmed because the WCO Explanatory Notes are sold, the WTO page did not mention the MPIA and the gov.uk guidance page returned 404. GATT 1947 Articles I, III and XI titles on wto.org (Articles XX and XXI appear in the contents list); Anti-Dumping Agreement Art. 2.1, 3 and 6.8 (dumping, material injury, threat, causal link, facts available); SCM Agreement Art. 1 and 2 (financial contribution, benefit, specificity).

Method: documentation only; no commands were run.
