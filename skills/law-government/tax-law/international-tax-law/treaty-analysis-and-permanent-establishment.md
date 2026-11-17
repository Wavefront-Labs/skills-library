---
id: law-government.tax-law.international-tax-law.treaty-analysis-and-permanent-establishment
name: treaty-analysis-and-permanent-establishment
category: law-government
field: tax-law
product: international-tax-law
tags: [international-tax-law, tax-treaty, double-tax-treaty, double-taxation-agreement, oecd-model, un-model, mli, multilateral-instrument, residence, tie-breaker, permanent-establishment, dependent-agent, fixed-place-of-business, service-pe, withholding-tax, beneficial-ownership, principal-purpose-test, lob, limitation-on-benefits, transfer-pricing, arms-length-principle, tp-documentation, master-file, local-file, foreign-tax-credit, mutual-agreement-procedure, pillar-two]
level: advanced
status: docs-checked
description: "Working a cross-border tax question: domestic law first, then the treaty (as modified by the MLI), residence tie-breakers, PE risk, withholding relief, transfer pricing and relief from double tax."
sources: ["https://www.oecd.org/en/publications/model-tax-convention-on-income-and-on-capital-2025-full-version_db32e18b-en.html", "https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/beps-mli/mli-frequently-asked-questions.pdf", "https://www.oecd.org/content/dam/oecd/en/publications/reports/2022/01/oecd-transfer-pricing-guidelines-for-multinational-enterprises-and-tax-administrations-2022_57104b3a/0e655865-en.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Treaty analysis and permanent establishment

**Goal:** answer "who taxes this income, how much, and how do we avoid paying twice" in a
repeatable order, and spot permanent-establishment and transfer-pricing exposure early.

Most treaties follow the OECD Model (some the UN Model, which gives source states more
taxing rights); article numbers below are OECD Model. The actual treaty text, its protocol,
the MLI positions of both states and domestic law always control. Checked 2026-10-24 against the OECD Model
(2025 edition) and OECD MLI materials; treaty-specific rules differ. Not tax advice.

## 1. Order of analysis
1. **Domestic law of the source state:** does it tax this income at all, and at what rate?
   If not, the treaty is irrelevant for that state.
2. **Domestic law of the residence state.**
3. **Treaty:** is it in force and effective for this period? Has the **MLI** modified it
   (check both states' MLI positions and synthesised text)?
4. **Treaty entitlement:** is the taxpayer a resident, a person, the beneficial owner
   (for dividends, interest, royalties)? Do anti-abuse rules (principal purpose test, LOB)
   deny benefits?
5. **Distributive article:** which article covers the income (business profits Art. 7,
   dividends 10, interest 11, royalties 12, capital gains 13, employment 15, other income 21)?
6. **Elimination of double tax** (Art. 23): exemption or credit in the residence state.

## 2. Residence and tie-breakers
Dual residents are resolved by the tie-breaker in the treaty's residence article; read the actual treaty (for
companies the rule differs between treaties and the MLI may change it).

## 3. Permanent establishment (Art. 5)
Business profits are taxable in the source state only if attributable to a PE. Test:
- **Fixed place** of business at the enterprise's disposal, with some permanence, through
  which business is carried on (offices, branches, sometimes a home office used regularly).
- **Construction/installation** projects beyond the treaty's time threshold (check the treaty and any anti-splitting rule).
- **Dependent agent:** someone habitually concluding contracts, or playing the principal role
  leading to contracts, on the enterprise's behalf (wider after MLI Art. 12 in adopting treaties).
- **Exceptions** for preparatory or auxiliary activities, subject after the MLI (Art. 13) to anti-fragmentation rules
  in adopting treaties.
- Some treaties have a **service PE**; check the treaty.
Remote workers abroad and sales staff with negotiating authority are the commonest accidental PEs.

## 4. Withholding taxes
Reduce source withholding by applying the treaty rate at source (with forms or residence
certificates) or by refund claim. Check beneficial ownership and holding thresholds.

## 5. Transfer pricing
Related-party transactions must be at **arm's length** (OECD Transfer Pricing
Guidelines). Accurately delineate the transaction, choose a method (CUP, resale price, cost
plus, TNMM, profit split), benchmark, and document under the documentation rules of each country (BEPS Action 13).

## 6. Disputes
Mutual agreement procedure (Art. 25) and arbitration where provided; keep domestic appeal
deadlines alive in parallel.

## Gotchas
- Applying the treaty before checking domestic law.
- Ignoring MLI modifications.
- Treaty-shopping structures failing the principal purpose test.

## Verify
- [ ] Domestic law of both states checked first.
- [ ] Treaty in force, MLI text applied, entitlement and anti-abuse tested.
- [ ] Correct distributive article identified.
- [ ] PE risk assessed for people and places in the source state.
- [ ] Transfer pricing documented; double-tax relief mechanism confirmed.

## Checked

Checked 2026-10-24. Jurisdiction: OECD Model Tax Convention and OECD MLI (treaty text always controls). Sources: OECD Model Tax Convention 2025 full version page and OECD MLI FAQ, via OECD search results; OECD Transfer Pricing Guidelines 2022.

Confirmed: OECD Model article numbers used (5, 7, 10, 11, 12, 13, 15, 21, 23, 25); fixed-place PE definition; MLI Art. 7 principal purpose test, Art. 12 dependent-agent changes and Art. 13 preparatory-or-auxiliary changes; five transfer-pricing methods (CUP, resale price, cost plus, TNMM, profit split). Removed as unconfirmed: Art. 4 and Art. 9 numbers, tie-breaker order for individuals and companies, time thresholds for construction PEs, the document names for transfer-pricing files and the Pillar Two sentence.

Method: documentation only; no commands were run.
