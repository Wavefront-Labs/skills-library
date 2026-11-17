---
id: law-government.tax-law.indirect-tax-advice.vat-gst-sales-tax-taxability-and-nexus
name: vat-gst-sales-tax-taxability-and-nexus
category: law-government
field: tax-law
product: indirect-tax-advice
tags: [indirect-tax-advice, tax-law, indirect-tax, vat, value-added-tax, gst, goods-and-services-tax, sales-tax, use-tax, taxability-matrix, nexus, economic-nexus, wayfair, marketplace-facilitator, place-of-supply, reverse-charge, zero-rated, exempt-supply, input-tax-recovery, partial-exemption, vat-registration, one-stop-shop, oss, exemption-certificate, resale-certificate, refund-claim, voluntary-disclosure-agreement, vda]
level: practitioner
status: docs-checked
description: "Indirect-tax advice method: build a taxability matrix, test nexus and registration, apply place-of-supply and exemption rules, manage certificates and file refund claims."
sources: ["https://www.law.cornell.edu/supremecourt/text/17-494", "https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en", "https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a", "https://www.gov.uk/guidance/how-to-correct-vat-errors-and-make-adjustments-or-claims-vat-notice-70045", "https://www.gov.uk/guidance/vat-guide-notice-700"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VAT, GST and sales-tax taxability and nexus

**Goal:** tell a business, transaction by transaction, whether indirect tax applies,
who must collect it, at what rate and where — and recover tax overpaid. Two model systems
are used: the **EU/UK VAT** family (also most GST systems) and **US state sales and use
tax**. Rates, thresholds and product rules change often and differ by state or country:
treat every figure as "check current". Jurisdiction: checked against US sales-tax nexus law, the EU One
Stop Shop and UK VAT guidance as of 2026-10-24. Not tax advice.

## 1. Map the business
- What is sold (goods, digital services, SaaS, professional services, bundles), to whom
  (business or consumer, exempt bodies), from where to where, through which channel
  (own site, marketplace, distributor).
- Pull 12–48 months of sales data by destination, product code and customer type.

## 2. Nexus / registration
**US sales tax:** physical presence (staff, inventory, offices) or **economic nexus**
after *Wayfair* — thresholds per state, set by each state (South Dakota's law, upheld in *Wayfair*,
used $100,000 of sales or 200 transactions).
Marketplace-facilitator laws may shift collection to the platform.
**VAT/GST:** register where you make taxable supplies above the local threshold; rules for non-established suppliers
vary by country. EU B2C cross-border
distance sales and e-services use the **One Stop Shop (OSS)**; a single EUR 10,000 EU-wide threshold applies to suppliers established in one Member State.
Record the date each threshold was crossed; liability usually runs from then.

## 3. Taxability matrix
Build a table, one row per product × jurisdiction:

| Product | Jurisdiction | Taxable / exempt / zero-rated | Rate | Authority (statute, ruling) | Notes |
|---|---|---|---|---|---|

- **VAT:** distinguish *zero-rated* (taxable at 0%, input tax recoverable) from *exempt*
  (no output tax, input tax generally irrecoverable — triggers partial-exemption
  calculations).
- **Place of supply:** B2B services generally taxed where the customer belongs, often via
  **reverse charge**; B2C services generally where the supplier belongs (UK general rules; special rules for certain services take
  priority — see VAT Notice 741A).
- **US:** tangible personal property presumptively taxable; services and SaaS vary
  sharply by state; bundling rules can tax the whole bundle.

## 4. Exemptions and certificates
- Collect valid **exemption/resale certificates** at or before the sale (state form or
  multistate/SST form); check completeness and expiry. Missing certificates make the
  seller liable on audit.
- VAT: hold customer VAT numbers (validate them with the tax authority's checking service) for reverse-charge
  supplies; keep evidence of export for zero-rating.

## 5. Fix the past
- Quantify exposure by year and jurisdiction, with interest and penalties.
- US: **voluntary disclosure agreements** may limit look-back and penalties (terms vary by state);
  approach anonymously through counsel where the programme allows.
- VAT: correct prior errors via return adjustments or voluntary disclosure; mind
  reporting thresholds for errors.

## 6. Refund claims
- Identify overpayment cause (exempt sale taxed, wrong rate, unclaimed input tax).
- File within the limitation period (UK VAT: four years per HMRC; US states vary — check). If the tax was passed to customers, some systems require
  you to refund them first (unjust-enrichment rules).
- Support each line with invoices and the authority relied on.

## Gotchas
- Treating "exempt" and "zero-rated" as the same thing.
- Use tax on purchases where the vendor did not charge sales tax.
- Marketplace sales still count toward some states' thresholds.
- Invoices missing mandatory VAT content, defeating the customer's input-tax claim.

## Verify
- [ ] Nexus/registration analysis dated per jurisdiction.
- [ ] Taxability matrix cites an authority for every row.
- [ ] Certificates/VAT numbers on file for every untaxed sale sampled.
- [ ] Past exposure quantified; VDA or disclosure decision recorded.
- [ ] Refund claims filed within limitation periods with supporting evidence.

## Checked

Checked 2026-10-24. Jurisdiction: US state sales tax (nexus), EU VAT (One Stop Shop) and UK VAT. Sources: *South Dakota v. Wayfair* opinion (Cornell LII); European Commission One Stop Shop page; HMRC VAT Notices 741A, 700 and 700/45.

Confirmed: Wayfair holding and South Dakota thresholds; EUR 10,000 EU-wide OSS threshold; UK B2B and B2C place-of-supply rules and reverse charge; UK four-year refund and error-correction limit. Removed as unconfirmed: the claims that several states dropped transaction counts, that VDAs usually look back three to four years and waive penalties, that US refund limits are commonly three to four years, and the VIES example.

Method: documentation only; no commands were run.
