---
id: transportation-logistics.trade-compliance-customs-brokerage.valuation-rules-of-origin.transaction-value-adjustments-and-fta-origin
name: transaction-value-adjustments-and-fta-origin
category: transportation-logistics
field: trade-compliance-customs-brokerage
product: valuation-rules-of-origin
tags: [customs-valuation, transaction-value, wto-valuation-agreement, assists, royalties, license-fees, selling-commission, buying-commission, related-party, first-sale, rules-of-origin, preferential-origin, non-preferential-origin, fta, usmca, tca, tariff-shift, regional-value-content, de-minimis-tolerance, cumulation, statement-on-origin, certificate-of-origin, supplier-declaration]
level: advanced
status: gated
description: "Determining customs value under the WTO method hierarchy (additions, deductions, related parties) and qualifying goods for FTA preference (tariff shift, RVC, cumulation, origin evidence)."
sources: ["https://www.ecfr.gov/current/title-19/section-152.103", "https://www.ecfr.gov/current/title-19/section-152.101", "https://www.wto.org/english/docs_e/legal_e/20-val_e.htm", "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title19-section1401a&num=0&edition=prelim", "https://ustr.gov/trade-agreements/free-trade-agreements/united-states-mexico-canada-agreement/agreement-between"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction-value adjustments and FTA origin

**Goal:** declare the right customs value and claim preference only when the goods
truly qualify — the two areas where audits find the most money.

## Part A — Customs value
### 1. Method hierarchy (WTO Valuation Agreement)
1. **Transaction value** — price actually paid or payable for goods sold for export,
   adjusted. Used for the vast majority of entries.
2. Transaction value of identical goods → 3. similar goods → 4. deductive
   (resale price minus costs) → 5. computed (cost of production plus profit) →
   6. fallback (reasonable means). Use them **in order**; skipping requires reasons.

### 2. Additions to the price (if not already included)
- **Assists:** materials, tools, dies, moulds, engineering/design work done outside the
  importing country supplied free or at reduced cost by the buyer. Apportion the
  value across the production (e.g. mould value ÷ planned units).
- **Royalties and licence fees** related to the goods and paid as a condition of sale.
- **Selling commissions** (paid by buyer to the seller's agent) and brokerage.
- **Proceeds** of resale accruing to the seller.
- **Packing** costs and containers.
- EU/UK: freight and insurance to the border; US: excluded.
### 3. Deductions/exclusions
**Buying commissions** (bona fide buyer's agent), post-importation assembly,
duties/taxes of the importing country, and (US) international freight when separately
identified.

### 4. Related parties
Transaction value is acceptable only if the relationship **did not influence the
price** — show it by circumstances of sale (arm's-length pricing, profit levels) or test
values. Transfer-pricing adjustments after import may require value corrections.

## Part B — Origin
### 1. Two kinds
- **Non-preferential** (marking, trade remedies, quotas): last substantial
  transformation (US) or last substantial, economically justified processing (EU).
- **Preferential** (FTA duty reduction): the agreement's own product-specific rules.

### 2. Qualifying under an FTA
1. Find the **product-specific rule** for the final product's HS code.
2. Typical tests:
   - **Wholly obtained** (minerals mined, crops grown there).
   - **Tariff shift** (CTC): each non-originating input must be classified in a
     different chapter/heading/subheading than the product.
   - **Regional value content (RVC)**: e.g. build-down RVC = (AV − VNM)/AV × 100, or a
     maximum non-originating-material percentage (EU/UK MaxNOM, set per product rule in the agreement).
   - Specific processes (chemical reactions, textile double transformation).
3. Apply **tolerance/de minimis** (non-originating inputs failing the shift up to the
   percentage set in the agreement) and **cumulation** (inputs from the partner
   count as originating).
4. Check **non-qualifying operations** (simple packing, labelling, mixing cannot confer
   origin regardless).
5. Check direct transport/non-alteration rules for goods transiting third countries.

### 3. Evidence
- Claim with the agreement's proof: statement on origin on the invoice (EU-UK TCA,
  many EU FTAs), **certification of origin** data elements (USMCA), or a certificate
  (Form A-style, older agreements). Some allow "importer's knowledge".
- Hold supplier declarations and the costed bill of materials behind every claim;
  retention periods are set by each agreement and authority (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Assists are invisible on invoices — ask the buyer's engineering/sourcing teams.
- An FTA claim on a product that "is made in" the partner country but fails the rule
  is a duty underpayment plus penalties.
- Supplier declarations expire (often annual long-term declarations) — track them.
- *Percentages above are typical illustrations; use the exact agreement text.*

## Verify
- [ ] Price checked for assists, royalties, commissions, packing; deductions documented.
- [ ] Related-party acceptability documented.
- [ ] Product-specific rule identified by HS code and each input tested.
- [ ] Origin evidence and supplier declarations on file and current.

## Checked

Jurisdiction: WTO method with US (19 USC 1401a) and EU/UK notes. Checked 2026-10-25: removed illustrative percentages and retention periods not confirmed against the agreements. Confirmed in 19 CFR 152.101(b) (method order; importer may request computed before deductive), 152.103 (additions: packing, selling commissions, assists, royalties as condition of sale, resale proceeds; exclusions: post-importation costs, duties, ocean freight and insurance). Buying commissions, USMCA and TCA origin tests and retention were not confirmed and are marked gated or generalised.

Method: documentation only; no commands were run.
