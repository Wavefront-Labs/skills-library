---
id: law-government.tax-law.estate-and-gift-tax-planning.transfer-tax-planning-instruments
name: transfer-tax-planning-instruments
category: law-government
field: tax-law
product: estate-and-gift-tax-planning
tags: [estate-and-gift-tax-planning, estate-tax, gift-tax, inheritance-tax, transfer-tax, unified-credit, exemption, annual-exclusion, marital-deduction, qtip, portability, dsue, form-706, form-709, gst-tax, generation-skipping, grat, ilit, crummey-powers, valuation-discounts, family-limited-partnership, charitable-remainder-trust, potentially-exempt-transfer, seven-year-rule, nil-rate-band, residence-nil-rate-band, step-up-in-basis]
level: advanced
status: docs-checked
description: "Transfer-tax planning: compute the exposure, use exemptions and annual exclusions, marital and charitable deductions, freezes (GRATs, sales to trusts), valuation discounts and timely returns."
sources: ["https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax", "https://www.law.cornell.edu/uscode/text/26/2035", "https://www.law.cornell.edu/uscode/text/26/2056", "https://www.law.cornell.edu/uscode/text/26/2503", "https://www.law.cornell.edu/uscode/text/26/6075", "https://www.gov.uk/inheritance-tax", "https://www.gov.uk/inheritance-tax/gifts", "https://www.gov.uk/valuing-estate-of-someone-who-died/pay-inheritance-tax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer-tax planning instruments

**Goal:** reduce estate, gift or inheritance tax lawfully while keeping the client's
control, liquidity and family objectives intact, with returns and elections filed on time.

Jurisdiction: examples are mostly US federal (unified estate and gift tax, GST tax), checked current on
2026-10-24, with UK inheritance tax points for contrast. Thresholds change with legislation and inflation indexing; check the
current figures every time. (US: basic exclusion USD 15,000,000 per person for 2026 (USD 13,990,000 for 2025), indexed thereafter;
annual exclusion USD 19,000 per donee for 2025 and 2026, per the IRS. UK: nil-rate band GBP 325,000 listed to
5 April 2031, 40% standard rate, per gov.uk. Verify before use.) State and other-country taxes may apply separately.

## 1. Measure the exposure
Gross estate (worldwide for residents/citizens; situs-based for non-residents), less debts,
expenses and deductions; add back lifetime taxable gifts (US) or gifts within 7 years (UK
PETs, with taper relief for years 3 to 7). Compare to available exemptions. Model the tax at death today and in 10–20 years with
growth assumptions; also model income-tax effects (loss of basis step-up for lifetime gifts).

## 2. Free tools first
- **Annual exclusion gifts** (per donee per year); direct payment of tuition and medical
  expenses (US: excluded without limit only if paid directly to the school or provider, §2503(e)).
- **UK:** normal-expenditure-out-of-income exemption (keep records), £250 small gifts and the £3,000 annual exemption.
- **Marital deduction:** transfers to a spouse are generally untaxed if the spouse is a
  citizen (US); a non-citizen surviving spouse needs a QDOT (US, §2056(d)); UK limits can apply to non-UK-domiciled spouses (confirm on gov.uk).
- **Portability (US):** elect on a timely estate return at the first death to pass unused
  exemption (DSUE) to the survivor, even when no tax is due.
- **Charitable deduction** and split-interest trusts (CRTs, CLTs).

## 3. Freezing and shifting growth
- **GRAT:** grantor retains an annuity; appreciation above the statutory rate passes to
  beneficiaries with minimal gift tax. Mortality risk during the term.
- **Sale to an intentionally defective grantor trust:** freeze value at sale price; growth
  outside the estate; grantor pays income tax (a further tax-free transfer).
- **ILIT:** keep life insurance proceeds out of the estate; Crummey withdrawal powers to
  qualify contributions for the annual exclusion; note the three-year rule for transferred policies (§2035(a)).
- **Family limited partnerships/LLCs** with valuation discounts for lack of control and
  marketability; require genuine non-tax purpose, formalities, and no retained enjoyment, or
  assets get pulled back into the estate.
- **Generation-skipping:** allocate GST exemption deliberately to dynasty trusts.

## 4. Valuation
Qualified appraisals for closely held interests, real estate and art; adequate disclosure on
gift returns starts the limitation clock. Aggressive discounts invite audit.

## 5. Returns and compliance
Gift tax returns (US Form 709) for gifts over the annual exclusion or to elect split gifts or
allocate GST exemption, due 15 April after the year of the gift (§6075(b)); estate return (Form 706) within
9 months of death (§6075(a)). UK IHT is payable by the end of the sixth month after the person dies, and
interest runs on tax paid later (gov.uk).

## Gotchas
- Retained interests (living in a gifted house rent-free) pulling assets back into the estate.
- Missing the portability election.
- Non-citizen spouse and cross-border situs rules.
- Planning that leaves no liquidity to pay the tax.

## Verify
- [ ] Current thresholds confirmed for every jurisdiction involved.
- [ ] Exposure modelled now and projected, including income-tax effects.
- [ ] Free exemptions used before complex structures.
- [ ] Each instrument's formalities and non-tax purpose documented.
- [ ] Returns, elections and appraisals calendared.

## Checked

Checked 2026-10-24. Jurisdiction: US federal transfer taxes and UK inheritance tax. Sources: IRS "What's New - Estate and gift tax"; Cornell LII text of 26 U.S.C. §§2035, 2056, 2503 and 6075; gov.uk Inheritance Tax, gifts and payment pages.

Confirmed: 2026 basic exclusion USD 15,000,000; annual exclusion USD 19,000; direct-payment condition for tuition and medical exclusion; QDOT rule; three-year rule; Form 709 and Form 706 due dates; UK nil-rate band GBP 325,000 to 5 April 2031, 40% rate, seven-year rule with taper, 250 GBP and 3,000 GBP exemptions, IHT payment deadline. Removed as unconfirmed: wedding gifts, the extendable Form 706 remark and the statement that many countries have no estate tax.

Method: documentation only; no commands were run.
