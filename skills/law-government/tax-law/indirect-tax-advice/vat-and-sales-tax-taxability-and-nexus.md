---
id: law-government.tax-law.indirect-tax-advice.vat-and-sales-tax-taxability-and-nexus
name: vat-and-sales-tax-taxability-and-nexus
category: law-government
field: tax-law
product: indirect-tax-advice
tags: [indirect-tax-advice, vat, gst, sales-tax, use-tax, indirect-tax, taxability, place-of-supply, time-of-supply, exempt-supply, zero-rated, standard-rated, reverse-charge, input-tax-recovery, partial-exemption, economic-nexus, wayfair, marketplace-facilitator, exemption-certificates, resale-certificate, registration-threshold, vat-registration, refund-claim, voluntary-disclosure, oss, ioss, digital-services]
level: practitioner
status: docs-checked
description: "Indirect-tax analysis for a transaction: what is supplied, where and when, rate or exemption, who accounts (reverse charge), registration and nexus, exemption certificates and refunds."
sources: ["https://www.law.cornell.edu/supremecourt/text/17-494", "https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en", "https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a", "https://www.gov.uk/guidance/how-to-correct-vat-errors-and-make-adjustments-or-claims-vat-notice-70045", "https://www.gov.uk/guidance/vat-guide-notice-700"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VAT and sales tax: taxability and nexus

**Goal:** for any sale, determine whether tax applies, at what rate, in which jurisdiction,
who must collect or account for it, and whether the seller must register, then keep the
evidence to prove it.

Two families: **VAT/GST** (multi-stage, credit-invoice: EU, UK, Canada GST/HST, Australia,
India, most of the world) and **retail sales and use tax** (single-stage at retail: US states
and localities). Rates, thresholds and rules change frequently; always check the current
legislation and authority guidance. Jurisdiction: checked against US sales-tax nexus law, the EU
One Stop Shop and UK VAT guidance as of 2026-10-24; other countries differ. Not tax advice.

## 1. Characterise the supply
- **Goods or services?** Digital products, software, bundles and installed goods are often
  borderline; the classification drives place of supply and rate.
- **Single or multiple supply?** Is one element ancillary to another (one rate) or are there
  distinct supplies (apportion)?
- **Who is the customer?** Business (B2B) or consumer (B2C) changes place of supply and who
  accounts.

## 2. Where (place of supply / sourcing)
- VAT: goods generally where they are when dispatched or delivered; B2B services generally where
  the customer belongs; B2C services generally where the supplier belongs, with special rules for
  certain services taking priority (see HMRC VAT Notice 741A; other countries differ).
- US sales tax: most states source to the destination (where the buyer receives it); some
  intrastate origin rules.

## 3. Rate or exemption
Standard, reduced, **zero-rated** (taxable at 0%, input tax recoverable) vs **exempt** (no tax,
input tax generally not recoverable). The difference matters hugely to the supplier's costs.
US: exemptions by product (food, clothing in some states) and by buyer (resale, manufacturing,
nonprofit, government) evidenced by certificates.

## 4. Who accounts
- **Reverse charge:** for many cross-border B2B services and some domestic sectors, the
  customer self-accounts. Invoices must say so.
- **Marketplace facilitator rules** (US) and platform deemed-supplier rules (VAT) shift
  collection to the platform.
- **Use tax:** US buyers owe it when the seller didn't collect.

## 5. Registration and nexus
- VAT: registration thresholds and rules for non-established suppliers vary by country; check each. The EU
  One Stop Shop (OSS/IOSS) lets sellers report cross-border B2C VAT through one portal, and a single EUR 10,000 EU-wide
  threshold applies to distance sales of goods and e-services for suppliers established in one Member State.
- US: after *South Dakota v. Wayfair* (2018), states impose **economic nexus** based on sales
  revenue and/or transaction counts in the state (South Dakota's law, upheld in *Wayfair*, used USD 100,000 of sales or 200 transactions; each state sets its own
  thresholds). Physical presence (employees, inventory, including in
  third-party warehouses) still creates nexus.
Track sales by jurisdiction monthly; register before the threshold-crossing date's deadline.

## 6. Certificates and evidence
Collect valid exemption/resale certificates at the time of sale (correct form, complete,
unexpired). Keep proof of export, customer VAT numbers (validated), and place-of-supply evidence.

## 7. Fixing the past and refunds
- Exposure from unregistered periods: voluntary disclosure agreements may limit look-back
  and penalties; terms vary by state.
- Overpaid tax: refund claims within limitation periods (UK VAT error corrections and refund claims: four years, not
  available for deliberate errors, per HMRC); in VAT, consider unjust-enrichment
  rules and whether customers must be reimbursed.

## Gotchas
- Treating zero-rated and exempt as the same.
- Missing reverse-charge wording on invoices.
- Not collecting certificates up front; retroactive collection often fails.
- Inventory in marketplace warehouses creating nexus unnoticed.

## Verify
- [ ] Supply characterised and customer type known.
- [ ] Place of supply/sourcing and rate determined with citation.
- [ ] Accounting party identified (supplier, reverse charge, marketplace).
- [ ] Registration/nexus position tracked by jurisdiction.
- [ ] Certificates and evidence held for each exempt or zero-rated sale.

## Checked

Checked 2026-10-24. Jurisdiction: US state sales tax (nexus), EU VAT (One Stop Shop) and UK VAT. Sources: *South Dakota v. Wayfair* opinion (Cornell LII); European Commission One Stop Shop page; HMRC VAT Notices 741A, 700 and 700/45.

Confirmed: Wayfair overruled the physical-presence rule and South Dakota's thresholds were USD 100,000 or 200 transactions; EU single EUR 10,000 threshold since 1 July 2021 for distance sales and e-services by suppliers established in one Member State; UK general place-of-supply rules (B2B where the customer belongs, B2C where the supplier belongs, special rules first) and the reverse charge; UK four-year limit for VAT error corrections and refund claims. Removed as unconfirmed: statements that some states dropped transaction counts, that VDAs usually waive penalties, and the list of exceptions to the general place-of-supply rule.

Method: documentation only; no commands were run.
